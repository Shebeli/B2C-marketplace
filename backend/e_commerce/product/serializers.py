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
    """
    Create and update methods doesn't support nested serializer fields
    'technical_details' and 'variants' on this serializer, as that would
    make the serializer more complicated to work with.
    For providing tags, name of the tags should be provided rather than
    the ids of the tags.
    """

    technical_details = ProductTechnicalDetailSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    tags = serializers.ListSerializer(
        child=serializers.CharField(max_length=30), write_only=True
    )

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

    def to_representation(self, product):
        ret = super().to_representation(product)
        ret["subcategory"] = product.subcategory.name
        ret["tags"] = [tag.name for tag in product.tags.all()]
        return ret

    def validate_tags(self, tags):
        if 10 >= len(tags) >= 3:
            raise serializers.ValidationError(
                "At least 3 tags should be provided and at most, 10 tags can be provided."
            )
        if tags != set(tags):
            raise serializers.ValidationError("Duplicate tag names are not allowed")
        return tags

    def to_internal_value(self, data):
        tag_names = data.get("tags")
        tag_objs = []
        for tag_name in tag_names:
            tag_objs.append(Tag.objects.get_or_create(name=tag_name))
        data["tags"] = tag_objs
        return super().to_internal_value(data)

    def update(self, product_obj, validated_data):
        if not self.partial:  # replace the whole current tags
            product_obj.tags.clear()
        tag_objs = validated_data.pop("tags")
        product_obj.tags.add(tag_objs)  # tags here are instances, not ids.
        return super().update(product_obj, validated_data)


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
