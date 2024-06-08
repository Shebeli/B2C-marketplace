from rest_framework import serializers

from ecom_user_profile.models import (
    SellerProfile,
    SellerBankAccount,
    SellerBusinessLicense,
    CustomerProfile,
    CustomerAddress,
)


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = "__all__"
        read_only_fields = ["wallet"]


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = "__all__"
        # extra_kwargs = {"user": {"write_only": True}}


class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = "__all__"
        read_only_fields = [
            "is_verified",
            "rating",
            "products_sold",
            "established_date",
        ]


class SellerBusinessLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerBusinessLicense
        fields = "__all__"


class SellerBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerBankAccount
        fields = "__all__"
