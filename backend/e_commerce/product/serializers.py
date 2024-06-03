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


# Abstract
class TechnicalDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = TechnicalDetail
        fields = "__all__"

    def to_representation(self, instance):
        ret = OrderedDict()
        attribute = instance.attribute.name
        value = instance.value
        ret[attribute] = value
        return ret


# Abstract
class VariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantImage
        fields = ["image", "product_variant"]
        extra_kwargs = {"product_variant": {"write_only": True}}

    # def to_representation(self, instance):
    #     ret = OrderedDict()
    #     return super().to_representation(instance)


# Abstract
class VariantSerializer(serializers.ModelSerializer):
    images = VariantImageSerializer(many=True)

    class Meta:
        model = ProductVariant
        fields = "__all__"
        extra_kwargs = {"product": {"write_only": True}}


class ProductSerializer(serializers.ModelSerializer):
    technical_details = TechnicalDetailSerializer(many=True, read_only=True)
    variants = VariantSerializer(many=True, read_only=True)
    # tags = serializers.StringRelatedField(many=True) # read only by default
    # category = serializers.CharField(source="category.name", read_only=True)

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
        ret['category'] = instance.category.name
        ret['tags'] = [tag.name for tag in instance.tags.all()]
        return ret

    def create(self, validated_data):
        return super().create(validated_data)


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "image"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
