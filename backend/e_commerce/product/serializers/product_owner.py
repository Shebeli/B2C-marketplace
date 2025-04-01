from django.core.cache import cache
from rest_framework import serializers

from product.models import Product, ProductVariant
from product.serializers.base import (
    ProductVariantImageSerializer,
    TechnicalDetailSerializer,
)


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
    """
    Note that main variant assignment is handled via signals. and the conditional expression
    on the field `is_valid` ensures that as long as either the field `owner` or `main_variant`
    are null, then the `is_valid` field would be false, otherwise true.
    """

    variants = ProductVariantSerializerForOwner(
        many=True, read_only=True
    )  # creation/update in different serializer
    technical_details = TechnicalDetailSerializer(many=True, read_only=True)
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
    rating_avg = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    total_revenue = serializers.SerializerMethodField()
    total_orders = serializers.SerializerMethodField()
    total_units_sold = serializers.SerializerMethodField()

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
            "is_valid",
            "is_enabled",
            "on_hand_stock",
            "reserved_stock",
            "available_stock",
            "view_count",
            "number_sold",
            "rating_avg",
            "rating_count",
            "total_revenue",
            "total_orders",
            "total_units_sold",
        ]
        extra_kwargs = {"subcategory": {"required": True}}
        read_only_fields = ["is_enabled", "is_valid"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["subcategory"] = {
            "id": instance.subcategory.id,
            "name": instance.subcategory.name,
        }
        return rep

    def validate_main_variant(self, pk):
        if self.instance:  # update method
            try:
                variant = ProductVariant.objects.get(id=pk)
            except ProductVariant.DoesNotExist:
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

    def get_rating_avg(self, product_obj):
        return cache.get_or_set(
            f"product:{product_obj.id}:rating_avg",
            product_obj.get_rating_avg(),
            10 * 60,
        )

    def get_rating_count(self, product_obj):
        return cache.get_or_set(
            f"product:{product_obj.id}:rating_count",
            product_obj.get_rating_count(),
            10 * 60,
        )

    def get_total_revenue(self, product_obj):
        return cache.get_or_set(
            f"product:{product_obj.id}:total_revenue",
            product_obj.get_total_revenue(),
            5 * 60,  # 5 mins
        )

    def get_total_orders(self, product_obj):
        return cache.get_or_set(
            f"product:{product_obj.id}:total_orders",
            product_obj.get_total_orders(),
            5 * 60,
        )

    def get_total_units_sold(self, product_obj):
        return cache.get_or_set(
            f"product:{product_obj.id}:total_units_sold",
            product_obj.get_total_units_sold(),
            5 * 60,
        )
