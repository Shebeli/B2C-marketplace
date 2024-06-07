from rest_framework import serializers

from ecom_user_profile.models import (
    SellerProfile,
    SellerProfileBankAccount,
    SellerProfileBusinessLicense,
    CustomerProfile,
    CustomerProfileAddress,
)


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = "__all__"
        read_only_fields = ["wallet"]


class CustomerProfileAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfileAddress
        fields = "__all__"


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


class SellerProfileBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfileBusinessLicense
        fields = "__all__"


class SellerProfileBankAccount(serializers.ModelSerializer):
    class Meta:
        model = SellerProfileBankAccount
        fields = "__all__"
