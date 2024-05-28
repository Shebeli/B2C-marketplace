from rest_framework import serializers
from product.models import Product, ProductImage, ProductVariant, Tag, Category


# Abstract
class ProductVariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ["product_variation"]


# Abstract
class ProductVariantSerializer(serializers.ModelSerializer):
    images = ProductVariantImageSerializer(many=True)

    class Meta:
        model = ProductVariant
        exclude = ["product"]


class ProductSerializer(serializers.ModelSerializer):
    "For listing all associated information for a single product"
    variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "technical_detail", "variants"]


class ProductListSerializer(serializers.ModelSerializer):
    "For listing all available products, but with limited information for each product"

    class Meta:
        model = Product
        fields = ["id", "name", "price", "image"]
