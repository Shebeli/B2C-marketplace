from order.models import Order
from rest_framework import serializers
from django.db.models import prefetch_related_objects
from feedback.models import ProductComment, ProductReview


class ProductReviewSerializer(serializers.ModelSerializer):
    non_updatable_fields = ["order", "product"]

    class Meta:
        model = ProductReview
        fields = "__all__"
        extra_kwargs = {"order": {"write_only": True}}

    def to_internal_value(self, data):
        "If the process is an update method, keep the old fields 'order' and 'product'"
        new_data = dict(data)
        if self.instance:
            for field in self.non_updatable_fields:
                new_data[field] = getattr(self.instance, field).id
        return super().to_internal_value(new_data)

    def validate(self, data):
        "Validate that the given product exists within given user's order."
        prefetch_related_objects([data["order"]], "items__product_variant__product")
        order_products = [
            item.product_variant.product.id for item in data["order"].items.all()
        ]
        if data["product"].id not in order_products:
            raise serializers.ValidationError(
                "The given product doesn't exist in the given order"
            )

        return data


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = "__all__"

    def to_internal_value(self, data):
        new_data = dict(data)
        if self.instance:
            new_data["product"] = getattr(self.instance, "product").id
        return super().to_internal_value(data)
