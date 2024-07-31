from django_filters import rest_framework as filters
from product.models import Product


class ProductFilter(filters.FilterSet):
    """
    It is assumed that the 'Product' querysets that are used within this filter,
    and their 'is_valid' fields are true (the 'main_variant' and 'owner'
    fields are not null on the Product instance).
    """

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    subcategory = filters.CharFilter(
        field_name="subcategory__name", lookup_expr="iexact"
    )
    price_min = filters.NumberFilter(
        field_name="main_variant__price", lookup_expr="gte"
    )
    price_max = filters.NumberFilter(
        field_name="main_variant__price", lookup_expr="lte"
    )
    in_stock = filters.BooleanFilter()

    class Meta:
        model = Product
        fields = ["name", "subcategory", "tags"]
