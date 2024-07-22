from collections import OrderedDict

from django.db.models import QuerySet
from rest_framework import serializers
from product.models import (
    Product,
    ProductVariantImage,
    ProductVariant,
    Tag,
    Category,
    TechnicalDetail,
)


class ProductTechnicalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalDetail
        exclude = ['product']


class ProductVariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantImage
        fields = ["image"]


# Product serializers for any kind of user.


class ProductVariantSerializerForAny(serializers.ModelSerializer):
    images = ProductVariantImageSerializer(many=True)

    class Meta:
        model = ProductVariant
        fields = ["id", "name", "price", "images"]


class ProductSerializerForAny(serializers.ModelSerializer):
    "This serializer is only intenteded to be used for representing data"

    technical_details = ProductTechnicalDetailSerializer(many=True, read_only=True)
    variants = ProductVariantSerializerForAny(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ["view_count", "created_at"]

    def to_representation(self, product_instance):
        ret = super().to_representation(product_instance)
        ret["subcategory"] = product_instance.subcategory.name
        ret["tags"] = [tag.name for tag in product_instance.tags.all()]
        return ret


# Product serializers for owners.


class ProductVariantSerializerForOwner(serializers.ModelSerializer):
    images = ProductVariantImageSerializer(many=True, required=False)

    class Meta:
        model = ProductVariant
        exclude = ["product"]

    def create(self, validated_data):
        if not validated_data.get("product"):
            raise serializers.ValidationError(
                "Product instance should be passed as keyword argument with serializer.save()"
            )
        return super().create(validated_data)


class ProductSerializerForOwner(serializers.ModelSerializer):
    variants = ProductVariantSerializerForOwner(many=True, read_only=True)
    technical_details = ProductTechnicalDetailSerializer(many=True, read_only=True)
    on_hand_stock = serializers.IntegerField(source="get_on_hand_stock", read_only=True)
    reserved_stock = serializers.IntegerField(
        source="get_reserved_stock", read_only=True
    )
    available_stock = serializers.IntegerField(
        source="get_available_stock", read_only=True
    )
    number_sold = serializers.IntegerField(source="get_number_sold", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "created_at",
            "description",
            "main_image",
            "main_price",
            "technical_details",
            "subcategory",
            "tags",
            "variants",
            "rating",
            "on_hand_stock",
            "reserved_stock",
            "available_stock",
            "view_count",
            "number_sold",
        ]
        extra_kwargs = {"subcategory": {"required": True}}

    def validate_tags(self, tags):
        if not (3 <= len(tags) <= 10):
            raise serializers.ValidationError(
                "At least 3 tags should be provided and at most, 10 tags can be provided."
            )
        return tags


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "main_price", "main_image"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TechnicalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalDetail
        exclude = ["product"]

    def create(self, validated_data):
        if not validated_data.get("product"):
            raise serializers.ValidationError(
                "Product instance should be passed as keyword argument with serializer.save()"
            )
        return super().create(validated_data)
