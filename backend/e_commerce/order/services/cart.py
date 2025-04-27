
from ecom_user.models import EcomUser
from product.models import ProductVariant

from order.exceptions.errors import (
    ResponseBaseError,
)
from order.models import Cart, CartItem
from order.services.validators import (
    run_cart_item_creation_validations,
    run_cart_validations,
)


class CartService:
    @staticmethod
    def add_item_to_cart(user: EcomUser, variant_id: int, quantity: int) -> Cart:
        product_variant = ProductVariant.objects.get(id=variant_id)
        run_cart_item_creation_validations(product_variant, user, quantity)

        return CartItem.objects.create(
            cart=user.cart,
            product_variant=variant_id,
            quantity=quantity,
        )

    @staticmethod
    def get_user_cart_errors(user: EcomUser) -> dict[int, str]:
        errors = {}
        for item in user.cart.items.all():
            item_errors = []
            try:
                run_cart_validations(item.product_variant)
            except ResponseBaseError as exc:
                item_errors.append(exc.message)
            errors[item.variant.id] = item_errors
        return errors
