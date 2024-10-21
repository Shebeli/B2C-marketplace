from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)

from financeops.models import IPG
from django.core.cache import cache
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny

from order.permissions import IsCartItemOwner
from order.models import Order, Cart, CartItem
from order.serializers import (
    CartItemSerializer,
    CartSerializerForCustomer,
    OrderSerializerForCustomer,
    OrderSerializerForSeller,
    OrderPaymentSerializer,
    IPGStatusSerializer,
)
from product.permissions import IsSellerVerified
from order.permissions import IsSellerOfOrder

class IPGStatus(APIView):
    """
    For displaying the list of available IPGs.
    """

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        available_ipg_ids = cache.get("available_ipgs")
        ipgs = IPG.objects.filter(pk__in=available_ipg_ids)
        serializer = IPGStatusSerializer(ipgs, many=True)
        return Response(serializer.data)


class CartItemDetail(GenericAPIView, UpdateModelMixin, DestroyModelMixin):
    """
    Allows a customer to delete or modify one of their cart items
    (The only modification in this case would be the `quantity` field).
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
        obj = self.request.user.cart
        if not obj:
            obj = Cart.objects.create(user=self.request.user)
        serializer = CartSerializerForCustomer(obj)
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
    For selecting the payment method after an order is creatd.

    Note that a pending order should already exist.

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

    