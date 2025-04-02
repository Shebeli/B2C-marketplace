from ecom_user_profile.serializers import SellerBriefProfileSerializer
from rest_framework import serializers

from product.models import (
    Category,
    MainCategory,
    Product,
    ProductVariantImage,
    SubCategory,
    Tag,
    TechnicalDetail,
)


class TechnicalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalDetail
        exclude = ["id", "product"]

    def create(self, validated_data):
        if not validated_data.get("product"):
            raise serializers.ValidationError(
                "Product instance should be passed as keyword argument with serializer.save()"
            )
        return super().create(validated_data)


class ProductVariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantImage
        fields = ["image"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class ProductListSerializer(serializers.ModelSerializer):
    """
    Used only for representing/serializing a list of products
    with each product's owner .
    """

    main_price = serializers.IntegerField(read_only=True, source="main_variant.price")
    main_image = serializers.ImageField(read_only=True, source="main_variant.image")
    seller_profile = SellerBriefProfileSerializer(
        read_only=True, source="owner.seller_profile"
    )

    class Meta:
        model = Product
        fields = ["id", "name", "main_price", "main_image", "seller_profile"]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["name", "subcategories"]


class FullCategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = MainCategory
        fields = ["name", "categories"]


class BreadcrumbSerializer(serializers.Serializer):
    """
    Provides a breadcrumb through a passed instance of SubCategory by
    retrieving the associated category and main category.
    Only used for representation.
    """

    def to_representation(self, instance):
        if not isinstance(instance, SubCategory):
            raise TypeError(
                "The passed in instance to `BreadcrumbSerializer` should be an instance of model `SubCategory`"
            )
        ret = {}
        ret["sub_category"] = instance.name
        ret["category"] = instance.category.name
        ret["main_category"] = instance.category.main_category.name
        return ret
