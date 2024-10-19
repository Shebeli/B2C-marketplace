from product.models import ProductVariant


def is_available(selected_variant: ProductVariant) -> bool:
    """Does product have available stocks"""
    if not selected_variant.is_available:
        return False
    return True


def is_quantity_valid(selected_variant: ProductVariant, quantity: int) -> bool:
    """Is the given quantity valid relative to available stock"""
    if quantity > selected_variant.available_stock:
        return False
    return True


def is_seller_active(selected_variant: ProductVariant) -> bool:
    """Is seller's account flagged as active or not"""
    if not selected_variant.owner.is_verified:
        return False
    return True


def is_product_enabled(selected_variant: ProductVariant) -> bool:
    """Is the product or the variant marked as enabled"""
    if not selected_variant.is_enabled or not selected_variant.product.is_enabled:
        return False
    return True
