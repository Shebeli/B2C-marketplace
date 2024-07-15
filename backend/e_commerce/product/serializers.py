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


# Abstract, nest serializer
class ProductTechnicalDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = TechnicalDetail
        exclude = ["id", "product"]

    def to_representation(self, instance):
        ret = OrderedDict()
        attribute = instance.attribute
        value = instance.value
        ret[attribute] = value
        return ret


# Abstract, nested serializer, read only
class ProductVariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantImage
        fields = ["image"]


# Abstract, nested serializer, read only
class ProductVariantSerializer(serializers.ModelSerializer):
    images = ProductVariantImageSerializer(many=True)

    class Meta:
        model = ProductVariant
        exclude = ["id", "product"]


class ProductSerializer(serializers.ModelSerializer):
    "Creating or updating TechnicalDetail and ProductVariant for a product is not supported in this serializer"
    technical_details = ProductTechnicalDetailSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "main_price",
            "main_image",
            "description",
            "technical_details",
            "variants",
            "subcategory",
            "tags",
        ]

    def to_representation(self, product_instance):
        ret = super().to_representation(product_instance)
        ret["subcategory"] = product_instance.subcategory.name
        ret["tags"] = [tag.name for tag in product_instance.tags.all()]
        return ret

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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TechnicalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalDetail
        fields = "__all__"
