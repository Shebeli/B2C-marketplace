from collections import OrderedDict

from rest_framework import serializers
from product.models import (
    Product,
    ProductVariantImage,
    ProductVariant,
    Tag,
    Category,
    TechnicalDetail,
    TechnicalDetailAttribute,
)


# Abstract, nest serializer
class ProductTechnicalDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = TechnicalDetail
        exclude = ["id", "product"]

    def to_representation(self, instance):
        ret = OrderedDict()
        attribute = instance.attribute.name
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
    """
    Create and update methods for nested serializer fields
    'technical_details' and 'variants' are not supported for this serializer,
    as that would make the serializer more complicated to work with.
    """

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
            "category",
            "tags",
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["category"] = instance.category.name
        ret["tags"] = [tag.name for tag in instance.tags.all()]
        return ret


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
        fields = ["id", "name", "main_price", "image"]


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
