from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import NotFound, ValidationError
from django.core import cache
from django_filters import rest_framework as filters
from ipware import get_client_ip

from product.models import Product, SubCategory, Tag
from product.serializers import (
    ProductSerializer,
    ProductListSerializer,
    CategorySerializer,
    TagSerializer,
    TechnicalDetailSerializer,
)
from product.permissions import IsAdminOrReadOnly
from product.filters import ProductFilter
from product.permissions import IsSellerVerified
from ecom_core.permissions import IsOwner


class ProductList(ListCreateAPIView):
    """
    Providing a subcategory via query parameter in the URL is required.
    ordering field options: main_price, rating, created_at, view_count.
    if you want the ordering to be descending, use - in front of the field.
    example: ?ordering=-view_count
    tags provided by the query parameter should be seperated by comma.
    example: ?tags=tag1,tag2 
    """

    permission_classes = [IsAdminOrReadOnly | IsOwner]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = ProductFilter
    ordering_fields = ["main_price", "rating", "created_at", "view_count"]
    ordering = ["-created_at"]

    def get_queryset(self):
        subcategory_name = self.request.query_params.get("subcategory")
        if not subcategory_name:
            raise ValidationError(
                "query parameter 'subcategory' should be provided", "no_query_param"
            )
        if not SubCategory.objects.filter(name__iexact=subcategory_name).exists():
            raise ValidationError("subcategory does not exist", "subcategory_not_found")
        return super().get_queryset()


class ProductDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly | IsOwner]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get(self, request, *args, **kwargs):
        """
        Increase the view count of a product but with the constraint of having a cooldown
        period of one day for each client, which is handled by caching the client's IP
        for one day.
        """
        product_instance = self.get_object()
        serializer = self.get_serializer(product_instance)
        user_ip, _ = get_client_ip(self.request)
        if not user_ip:
            return Response(serializer.data)
        redis_key = f"product:{product_instance.id}:ip:{user_ip}"
        redis_client = cache.client.get_client()
        if not redis_client.exists(redis_key):
            product_instance.increase_view_count()
            cooldown_period = 3600 * 24  # one hour in seconds * number of hours
            redis_client.setex(redis_key, cooldown_period, 1)  # 1 is a dummy value
        return Response(serializer.data)

class ShopProductList(ListAPIView):
    "Lists all products belonging to current authenticated seller"
    permission_classes = [IsSellerVerified]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)