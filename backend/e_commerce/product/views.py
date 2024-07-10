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
from ecom_core.permissions import IsOwner


class ProductList(ListCreateAPIView):
    """
    Providing a subcategory via query parameter in the URL is required and the
    provided subcategory name should already exist in the database, since the
    products belonging to the provided subcategory are retrieved.
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
        return super().get_queryset(self)


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


class TagProductsList(ListAPIView):
    "For listing all products belonging to a certain tag or list of tags"
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_tag_names_or_400(self):
        tag_names = self.request.query_params.getlist("tags")
        if not tag_names:
            raise ValidationError(
                "query parameter 'tag' should be provided", "no_query_param"
            )
        return tag_names

    def get_queryset(self):
        tag_names = self.get_tag_names_or_400()
        products = self.queryset.filter(tags__name__in=tag_names)
        if not products:
            raise NotFound("No products were found with the given tag name(s)")
        return products


# class CategoryViewSet(ModelViewSet):
#     permission_classes = [IsAdminOrReadOnly]
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# class TagViewSet(ModelViewSet):
#     permission_classes = [IsAdminOrReadOnly]
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer


# class ProductsTechnicalDetailViewSet(ModelViewSet):
#     permission_classes = [IsAdminUser]
#     queryset = Product.objects.all()
#     serializer_class = TechnicalDetailSerializer
