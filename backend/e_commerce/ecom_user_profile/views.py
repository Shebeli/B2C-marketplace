from rest_framework.generics import (
    get_object_or_404,
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins

from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ecom_user_profile.permissions import IsOwner
from ecom_user_profile.models import (
    CustomerProfile,
    CustomerAddress,
    SellerBankAccount,
    SellerBusinessLicense,
    SellerProfile,
)
from ecom_user_profile.serializers import (
    CustomerProfileSerializer,
    CustomerAddressSerializer,
    SellerBankAccountSerializer,
    SellerProfileSerializer,
    SellerBusinessLicenseSerializer,
)
from ecom_user.authentication import EcomUserJWTAuthentication


class CustomerProfileAPIView(
    GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin
):
    "Retrieve or update current authenticated user's customer profile"
    authentication_classes = [EcomUserJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileSerializer
    queryset = CustomerProfile.objects.all()
    # lookup_field = ""

    def get_object(self):
        return self.get_queryset().get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CustomerAddressList(ListCreateAPIView):
    authentication_classes = [EcomUserJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = CustomerAddress.objects.all()
    serializer_class = CustomerAddressSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def check_address_limit(self):
        addresses_count = self.get_queryset().count()
        if addresses_count >= 5:
            return Response(
                {"limit count": "this user cannot create more than 5 addresses"},
                status.HTTP_400_BAD_REQUEST,
            )

    def create(self, request, *args, **kwargs):
        self.check_address_limit()
        return super().create(request, *args, **kwargs)


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
        return self.get_queryset().get(user=self.request.user)

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
        return self.queryset.filter(user=self.request.user)


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
    queryset = SellerBankAccount.objects.all()
    serializer_class = SellerBankAccountSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class SellerBankAccountDetail(RetrieveUpdateDestroyAPIView):
    authentication_classes = [EcomUserJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = SellerBankAccount.objects.all()
    serializer_class = SellerBankAccountSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
