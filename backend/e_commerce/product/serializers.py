from rest_framework import serializers
from product.models import Product, ProductImage, ProductVariant, Tag, Category


# Abstract
class VariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ["product_variation"]


# Abstract
class VariantSerializer(serializers.ModelSerializer):
    images = VariantImageSerializer(many=True)

    class Meta:
        model = ProductVariant
        exclude = ["product"]


class ProductSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "description",
            "technical_detail",
            "image",
            "variants",
        ]


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "image"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'