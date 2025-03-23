from backend.e_commerce.order.models import Order
from rest_framework import serializers

from feedback.models import ProductComment, ProductReview


class ProductReviewSerializer(serializers.ModelSerializer):
    non_updatable_fields = ["order", "product"]

    class Meta:
        model = ProductReview
        fields = "__all__"
        extra_kwargs = {"order": {"write_only": True}}

    def to_internal_value(self, data):
        "If the process is an update method, ignore the fields 'order' and 'product'"
        if self.instance:
            for field in self.non_updatable_fields:
                data.pop(field, None)
        return super().to_internal_value(data)

    def validate(self, data):
        "Validate that the given product exists within given user's order."
        try:
            order = Order.objects.prefetch_related(
                "items__product_variant__product"
            ).get(id=data["order"])
        except Order.DoesNotExist:
            raise serializers.ValidationError("Given order id does not exist")
        order_products = (item.product_variant.product.id for item in order.items.all())
        if data["product"] not in order_products:
            raise serializers.ValidationError(
                "The given product doesn't exist in the given order"
            )
        return data


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = "__all__"

    def to_internal_value(self, data):
        if self.instance:
            self.data.pop("product", None)
        return super().to_internal_value(data)
