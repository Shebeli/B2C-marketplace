import django_filters
from product.models import Product

# class ProductFilter(django_filters.FilterSet):
#     price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
#     price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
#     in_stock = django_filters
    
#     class Meta:
#         model = Product
