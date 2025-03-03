from django.core.exceptions import ObjectDoesNotExist
from ecom_user_profile.serializers import SellerBriefProfileSerializer
from rest_framework import serializers

from product.models import (
    Category,
    MainCategory,
    Product,
    ProductVariant,
    ProductVariantImage,
    SubCategory,
    Tag,
    TechnicalDetail,
)


class ProductTechnicalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalDetail
        exclude = ["product"]


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
    "Intended only for read operations"

    technical_details = ProductTechnicalDetailSerializer(many=True, read_only=True)
    variants = ProductVariantSerializerForAny(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ["view_count", "created_at", "main_variant"]

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
                "Product instance should be passed as keyword argument when calling serializer.save()"
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
    main_price = serializers.IntegerField(source="main_variant.price", read_only=True)
    main_image = serializers.ImageField(source="main_variant.image", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "created_at",
            "description",
            "main_variant",
            "main_price",
            "main_image",
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

    def validate_main_variant(self, pk):
        if self.instance:  # update method
            try:
                variant = ProductVariant.objects.get(id=pk)
            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    "The referenced ProductVariant object via id does not exist"
                )
            if variant.product != self.instance:
                raise serializers.ValidationError(
                    "The referenced ProductVariant object via id doesn't belong to this product"
                )
        else:  # create method
            raise serializers.ValidationError(
                "main_variant field shouldn't be provided for a create operation"
            )
        return pk

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
    """
    Used only for representing/serializing a list of products
    with each product's owner .
    """

    main_price = serializers.IntegerField(read_only=True)
    main_image = serializers.ImageField(read_only=True)
    seller = SellerBriefProfileSerializer(read_only=True, source="owner.seller_profile")

    class Meta:
        model = Product
        fields = ["id", "name", "main_price", "main_image", "seller"]


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


class CategoryBreadcrumbSerializer(serializers.Serializer):
    "Only used for representation"

    def to_representation(self, instance: SubCategory):
        ret = {}
        ret["subcategory"] = instance.name
        ret["category"] = instance.category.name
        ret["main_category"] = instance.category.main_category.name
        return super().to_representation(instance)


# class SubCategoryNameSerializer(serializers.ListSerializer):
#     def to_representation(self, data):
#         return list(data.values_list("name", flat=True))


# class SubCategoryListSerialzier(serializers.Serializer):
#     subcategories = SubCategoryNameSerializer(source="*", read_only=True)
