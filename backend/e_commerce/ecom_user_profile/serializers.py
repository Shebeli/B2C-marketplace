from rest_framework import serializers

from ecom_user_profile.models import (
    CustomerAddress,
    CustomerProfile,
    BankCard,
    SellerBusinessLicense,
    SellerProfile,
)


class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Method 'create' is never going to be used, since this serializer is only
    used for update and retrieve operations.
    """

    class Meta:
        model = CustomerProfile
        exclude = ["user"]


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        exclude = ["user"]

    def create(self, validated_data):
        if not validated_data.get("user"):
            raise serializers.ValidationError(
                "An instance of user should be provided using the keyword 'user' when calling save()"
            )
        return CustomerAddress.objects.create(**validated_data)


class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        read_only_fields = [
            "is_verified",
            "rating",
            "products_sold",
            "established_date",
        ]
        exclude = ["user"]


class SellerBusinessLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerBusinessLicense
        exclude = ["user"]

    def create(self, validated_data):
        if not validated_data.get("user"):
            raise serializers.ValidationError(
                "An instance of user should be provided using the keyword 'user' when calling save()"
            )
        return SellerBusinessLicense.objects.create(**validated_data)


class SellerBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCard
        exclude = ["user"]

    def create(self, validated_data):
        if not validated_data.get("user"):
            raise RuntimeError(
                "An instance of user should be provided using the keyword 'user' when calling save()"
            )
        return BankCard.objects.create(**validated_data)
