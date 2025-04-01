from django.core.cache import cache
from django.db.models import Avg, Count
from ecom_user_profile.models import SellerProfile
from rest_framework import serializers

from product.models import Product, ProductVariant
from product.serializers.base import (
    ProductVariantImageSerializer,
    TechnicalDetailSerializer,
)


class ProductVariantSerializerForAny(serializers.ModelSerializer):
    images = ProductVariantImageSerializer(many=True)

    class Meta:
        model = ProductVariant
        fields = ["id", "name", "price", "images", "color"]


class ProductSellerSerializer(serializers.ModelSerializer):
    """Only used for nested representation in other serializers."""

    class Meta:
        model = SellerProfile
        fields = ["id", "store_name", "store_image"]


class ProductSerializerForAny(serializers.ModelSerializer):
    "Only used for representation"

    technical_details = TechnicalDetailSerializer(many=True, read_only=True)
    variants = ProductVariantSerializerForAny(many=True, read_only=True)
    owner = ProductSellerSerializer(read_only=True)
    rating_avg = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["view_count", "created_at", "main_variant"]

    def to_representation(self, product_instance):
        ret = super().to_representation(product_instance)
        ret["subcategory"] = product_instance.subcategory.name
        ret["tags"] = [tag.name for tag in product_instance.tags.all()]
        return ret

    def get_rating_avg(self, product_obj):
        return cache.get_or_set(
            f"product:{product_obj.id}:rating_avg",
            lambda: product_obj.reviews.aggregate(avg=Avg("rating"))["avg"] or 0,
            10 * 60,
        )

    def get_rating_count(self, product_obj):
        return cache.get_or_set(
            f"product:{product_obj.id}:rating_count",
            lambda: product_obj.reviews.aggregate(count=Count("id"))["count"] or 0,
            10 * 60,
        )
