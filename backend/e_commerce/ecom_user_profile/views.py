from ecom_core.permissions import IsOwner
from ecom_user.authentication import EcomUserJWTAuthentication
from rest_framework import mixins, status
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ecom_user_profile.models import (
    CustomerAddress,
    CustomerProfile,
    BankCard,
    SellerBusinessLicense,
    SellerProfile,
)
from ecom_user_profile.serializers import (
    CustomerAddressSerializer,
    CustomerProfileSerializer,
    SellerBankAccountSerializer,
    SellerBusinessLicenseSerializer,
    SellerProfileSerializer,
)


class CustomerProfileAPIView(
    GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin
):
    "Retrieve or update current authenticated user's customer profile"
    authentication_classes = [EcomUserJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileSerializer
    queryset = CustomerProfile.objects.all()

    def get_object(self):
        return self.get_queryset().get_or_create(user=self.request.user)[0]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CustomerAddressList(ListCreateAPIView):
    """
    Note that if a request is made to create more than 5 addresses,
    the request gets prohibited by a 400 response.
    """

    authentication_classes = [EcomUserJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = CustomerAddress.objects.all()
    serializer_class = CustomerAddressSerializer

    # since the queryset is filtered by current user, the permission class 'IsOwner' seems to
    # be redundent, however, it adds a level of security with a small overhead.
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("id")

    def create(self, request, *args, **kwargs):
        if self.request.user.has_reached_address_limit():
            return Response(
                {"limit count": "this user cannot create more than 5 addresses"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomerAddressDetail(RetrieveUpdateDestroyAPIView):
    authentication_classes = [EcomUserJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = CustomerAddress.objects.all()
    serializer_class = CustomerAddressSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class SellerProfileAPIView(
    GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin
):
    "Retrieve or update current authenticated user's seller profile"
    authentication_classes = [EcomUserJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SellerProfileSerializer
    queryset = SellerProfile.objects.all()

    def get_object(self):
        return self.get_queryset().get_or_create(user=self.request.user)[0]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class SellerBusinessLicenseList(ListCreateAPIView):
    authentication_classes = [EcomUserJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = SellerBusinessLicense.objects.all()
    serializer_class = SellerBusinessLicenseSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SellerBusinessLicenseDetail(RetrieveUpdateDestroyAPIView):
    authentication_classes = [EcomUserJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = SellerBusinessLicense.objects.all()
    serializer_class = SellerBusinessLicenseSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class SellerBankAccountList(ListCreateAPIView):
    authentication_classes = [EcomUserJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = BankCard.objects.all()
    serializer_class = SellerBankAccountSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SellerBankAccountDetail(RetrieveUpdateDestroyAPIView):
    authentication_classes = [EcomUserJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = BankCard.objects.all()
    serializer_class = SellerBankAccountSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
