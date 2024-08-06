from typing import Union

from rest_framework import serializers
from order.models import Order, CartItem, Cart, CartItem
from ecom_user_profile.models import CustomerAddress, SellerProfile
from product.models import ProductVariant


class CartItemSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(source="product_variant.price", read_only=True)
    name = serializers.IntegerField(source="product_variant.name", read_only=True)
    image = serializers.ImageField(source="product_variant.image", read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "price", "name", "image", "quantity"]
        extra_kwargs = {
            "cart": {"read_only": True},
            "product_variant": {"required": True},
        }

    def _validate_variant_has_same_owner(self, attrs: dict) -> None:
        """
        Validate the passed in product variant to checks if it has the same
        owner as other existing cart item objects.
        """
        cart_item = CartItem.objects.filter(cart_id=attrs["cart"]).first()
        if cart_item:
            referenced_variant = ProductVariant.objects.get(id=attrs["product_variant"])
            if referenced_variant.owner != cart_item.product_variant.owner:
                raise serializers.ValidationError(
                    "Cart items should belong to only one seller"
                )

    def validate(self, attrs):
        if not self.context.get("cart"):
            raise serializers.ValidationError("Order must be provided through context")
        self._validate_variant_has_same_owner(attrs)
        return attrs


class CartSerializerForCustomer(serializers.ModelSerializer):
    """
    A cart object is never going to be created/updated directly, so
    this serializer is intended for read only operations.
    """

    items = CartItemSerializer(many=True, read_only=True)
    seller = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "items"]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def get_seller(self, cart_obj: Cart) -> Union[int, None]:
        cart_item = cart_obj.items.first()
        if cart_item:
            return cart_item.owner

    def validate(self, attrs):
        user = self.context.get("user")
        if not user:
            raise serializers.ValidationError(
                "The user must passed through the context"
            )
        return attrs


# Order and order item serializers are quite similar to cart and cart item serializers.


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Order creation and handling should be done by the server and not the client.
    Thus the order object should be passed to serializer using .save(order=) method.
    """

    price = serializers.IntegerField(source="product_variant.price", read_only=True)
    name = serializers.IntegerField(source="product_variant.name", read_only=True)
    image = serializers.ImageField(source="product_variant.image", read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "order",
            "price",
            "name",
            "image",
            "product_variant",
            "quantity",
        ]
        extra_kwargs = {
            "order": {"read_only": True},
            "product_variant": {"required": True},
        }

    def _validate_variant_has_same_owner(self, attrs: dict) -> None:
        """
        Validate the passed in product variant to checks if it has the same
        owner as other existing order item objects in the database.
        """
        order_item = CartItem.objects.filter(order_id=attrs["order"]).first()
        if order_item:
            referenced_variant = ProductVariant.objects.get(id=attrs["product_variant"])
            if referenced_variant.owner != order_item.product_variant.owner:
                raise serializers.ValidationError(
                    "Order items should belong to one seller only"
                )

    def validate(self, attrs):
        if not self.context.get("order"):
            raise serializers.ValidationError("Order must be provided through context")
        self._validate_variant_has_same_owner(attrs)
        return attrs


class OrderSerializerForCustomer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    seller = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "user", "items", "status", "customer_address", "notes"]
        extra_kwargs = {
            "status": {"read_only": True},
            "user": {"read_only": True},
        }

    def get_seller(self, order_obj: Order) -> Union[int, None]:
        order_item = order_obj.items.first()
        if order_item:
            return order_item.owner

    def validate(self, attrs):
        request_method = self.context["request"].method
        if request_method in ["PUT", "PATCH"] and attrs["status"] != Order.PENDING:
            raise serializers.ValidationError(
                "This order cannot be modified since its not in PENDING state."
            )
        user = self.context.get("user")
        if not user:
            raise serializers.ValidationError(
                "The user must passed through the context"
            )
        customer_address_obj = CustomerAddress.objects.get(attrs["customer_address"])
        if not customer_address_obj.user.id != attrs["user"]:
            raise serializers.ValidationError(
                "The given customer address does not belong to this user"
            )
        return attrs
