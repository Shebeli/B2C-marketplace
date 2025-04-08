from django.db.models import prefetch_related_objects
from ecom_user.models import EcomUser
from order.models import Order
from rest_framework import serializers

from feedback.models import ProductComment, ProductReview, SellerReview


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcomUser
        fields = ["id", "full_name", "profile_picture"]


class ProductReviewSerializer(serializers.ModelSerializer):
    non_updatable_fields = ["order", "product"]

    class Meta:
        model = ProductReview
        exclude = ["reviewed_by"]
        extra_kwargs = {
            "order": {"write_only": True},
            "product": {"write_only": True},
        }

    def to_internal_value(self, data):
        if self.instance:
            data["product"] = getattr(self.instance, "product").id
            data["order"] = getattr(self.instance, "order").id
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["reviewed_by"] = {}
        user = instance.reviewed_by
        ret["reviewed_by"]["id"] = user.id
        ret["reviewed_by"]["full_name"] = user.full_name
        ret["reviewed_by"]["profile_picture"] = (
            user.profile_picture.url if user.profile_picture else None
        )
        return ret

    def validate(self, data):
        "Validate that the given product exists within given user's order, and the order is completed."
        if data["order"].status not in [Order.COMPLETED, Order.DELIVERED]:
            raise serializers.ValidationError(
                "The order should be either in COMPLETED or DELIVERED status."
            )
        prefetch_related_objects([data["order"]], "items__product_variant__product")
        order_products = [
            item.product_variant.product.id for item in data["order"].items.all()
        ]
        if data["product"].id not in order_products:
            raise serializers.ValidationError(
                "The given product doesn't exist in the given order"
            )
        return data

    def create(self, validated_data):
        if not validated_data.get("reviewed_by"):
            raise serializers.ValidationError(
                "An instance of current authenticated user should be passed through .save() via the kwarg 'reviewed_by'"
            )
        return ProductReview.objects.create(**validated_data)


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        exclude = ["commented_by"]
        extra_kwargs = {"product": {"write_only": True}}

    def to_internal_value(self, data):
        if self.instance:
            data["product"] = getattr(self.instance, "product").id
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.commented_by:
            ret["commented_by"] = {
                "id": instance.commented_by.id,
                "full_name": instance.commented_by.full_name,
                "profile_picture": (
                    instance.commented_by.profile_picture.url
                    if instance.commented_by.profile_picture
                    else None
                ),
            }
        return ret

    def create(self, validated_data):
        if not validated_data.get("commented_by"):
            raise RuntimeError(
                "An instance of user should be provided using the keyword 'commented_by' when calling save()"
            )
        return ProductComment.objects.create(**validated_data)


class SellerReviewSerializer(serializers.ModelSerializer):
    non_updatable_fields = ["order", "seller"]

    class Meta:
        model = SellerReview
        exclude = ["reviewed_by"]
        extra_kwargs = {
            "order": {"write_only": True},
        }

    def to_internal_value(self, data):
        if self.instance:
            data["seller"] = getattr(self.instance, "seller").id
            data["order"] = getattr(self.instance, "order").id
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["reviewed_by"] = {}
        user = instance.reviewed_by
        ret["reviewed_by"]["id"] = user.id
        ret["reviewed_by"]["full_name"] = user.full_name
        ret["reviewed_by"]["profile_picture"] = (
            user.profile_picture.url if user.profile_picture else None
        )
        return ret

    def validate(self, data):
        "Validate that the given seller exists within given user's order, and the order is completed."
        if data["order"].status not in [Order.COMPLETED, Order.DELIVERED]:
            raise serializers.ValidationError(
                "The order should be either in COMPLETED or DELIVERED status."
            )
        if data["order"].seller != data["seller"]:
            raise serializers.ValidationError(
                "The given order doesn't belong to given seller"
            )
        return data
