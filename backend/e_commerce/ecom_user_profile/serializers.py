from django.urls import reverse
from rest_framework import serializers

from ecom_user_profile.models import (
    BankCard,
    CustomerAddress,
    CustomerProfile,
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


class SellerBriefProfileSerializer(serializers.ModelSerializer):
    """
    Used in other serializers or when a brief introduction of seller is required.
    for representing/serialization only
    """

    store_url = serializers.SerializerMethodField()

    class Meta:
        model = SellerProfile
        fields = ["id", "store_name", "store_image", "store_url"]

    def get_store_url(self, obj):
        return reverse("seller-public-profile", kwargs={"pk": obj.id})


class SellerPublicProfileSerializer(serializers.ModelSerializer):
    """
    Used only for representation/serialization of seller's public information comprehensivly.
    """

    class Meta:
        model = SellerProfile
        fields = [
            "id",
            "store_name",
            "store_address",
            "store_description",
            "store_image",
            "website",
            "minimum_order_amount",
        ]


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
