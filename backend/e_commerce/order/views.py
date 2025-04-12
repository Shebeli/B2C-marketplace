import logging

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from financeops.models import Payment
from product.permissions import IsSellerVerified
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from zibal.utils import to_snake_case_dict

from order.models import Cart, CartItem, Order
from order.permissions import IsCartItemOwner, IsSellerOfOrder
from order.serializers import (
    CartItemSerializer,
    CartSerializerForCustomer,
    IPGStatusSerializer,
    OrderPaymentSerializer,
    OrderSerializerForCustomer,
    OrderSerializerForSeller,
    ZibalCallbackSerializer,
)

logger = logging.getLogger("order")


# class IPGStatus(APIView):
#     """
#     For displaying the list of available IPGs.
#     """

#     permission_classes = [AllowAny]

#     def get(self, request, *args, **kwargs):
#         available_ipg_ids = cache.get("available_ipgs")
#         ipgs = IPG.objects.filter(pk__in=available_ipg_ids)
#         serializer = IPGStatusSerializer(ipgs, many=True)
#         return Response(serializer.data)


class CartItemDetail(GenericAPIView, UpdateModelMixin, DestroyModelMixin):
    """
    Allows a customer to delete or modify one of their cart items
    """

    permission_classes = [IsCartItemOwner, IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartDetail(APIView):
    """
    Allows a customer to inspect their current cart and its items.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart_obj, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer = CartSerializerForCustomer(cart_obj)
        return Response(serializer.data)


# class CustomerOrderCreation(APIView):
#     """
#     For creating an order based off the current cart.

#     An address should be selected.
#     """

#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         serializer = OrderSerializerForCustomer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(user=self.request.user)
#         return Response(serializer.data)


class CustomerOrderList(ListCreateAPIView):
    """
    For listing customer orders, or creating an order, based off on customer's
    current cart.

    Note that this endpoint is not responsible for handling the payment when
    creating an order.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializerForCustomer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomerOrderPayment(APIView):
    """
    For selecting the payment method after an order is created.

    Note that an UNPAID order should already exist.

    If an order is not attempted to be paid after 20 minutes of
    its creation, then its cancelled.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = OrderPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SellerOrderList(ListAPIView):
    """
    For listing all the orders which the current authenticated user is
    the seller of the orders.
    """

    permission_classes = [IsAuthenticated, IsSellerVerified]
    queryset = Order.objects.all()
    serializer_class = OrderSerializerForSeller

    def get_queryset(self):
        return self.queryset.filter(seller=self.request.user)


class SellerOrderDetail(RetrieveUpdateAPIView):
    """
    For inspecting an order, or updating an order.

    Note that there are limitations on how an order is updated,
    such as only certain order status updates are applicable with
    related required fields.

    Only associated fields will be used to update the order (depending
    on the new order status). e.g. when updating the order to SHIPPED,
    other unnecessary fields such as cancel_reason will be ignored.
    """

    permission_classes = [IsSellerOfOrder, IsAuthenticated, IsSellerVerified]
    queryset = Order.objects.all()
    serializer_class = OrderSerializerForSeller


class ZibalCallbackView(APIView):
    """The callbackURL specified for requesting a new payment for zibal
    should ensure that Zibal's payment service does a call to this endpoint."""

    def get(self, request, *args, **kwargs):
        ip_address = request.META.get("REMOTE_ADDR")
        if ip_address not in settings.IPG_IPGS:
            logger.error(
                "An unallowed request was made to Zibal's callback endpoint"
                f"with IP of {request.META.get('REMOTE_ADDR')}"
            )
            raise PermissionDenied("Unauthorized request.")
        payment_data = to_snake_case_dict(self.request.query_params)
        serializer = ZibalCallbackSerializer(payment_data)

        # validate the data and try to retrieve the payment instance
        if not serializer.is_valid():
            logger.error(
                "Data recieved from the Zibal IPG doesn't have the expected "
                "data structure. "
                f"Data validation errors: {serializer.errors}"
                f"Recieved initial data: {payment_data}"
            )
            return Response(
                {"error": "Unexpected data structure recieved from the IPG"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        try:
            payment_obj = Payment.objects.get(track_id=serializer.data["track_id"])
        except ObjectDoesNotExist:
            logger.error(
                f"The given track id {serializer.data['track_id']} from IPG's"
                "callback request wasn't associated with any `Payment` objects."
            )
            return Response(
                {"error": "No Payment instances were found with the given track_id"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # update the payment instance
        if serializer.data["success"] == 0:
            payment_obj.status = Payment.CANCELLED
            logger.warning(
                f"The payment with track id of {serializer.data['track_id']} was unsuccesful."
                f"Result code: {serializer.data['status']}"
            )
            return Response(
                {"error": "The payment was unsuccesful"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            payment_obj.status = Payment.PAID
            logger.info(
                f"The payment instance with id of {payment_obj.id} was updated"
                "to PAID due to successful callback request from Zibal's IPG."
            )

        payment_obj.save()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
