from django.core.cache import cache
from django_filters import rest_framework as filters
from ipware import get_client_ip
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.response import Response

from product.filters import ProductFilter
from product.models import Product, ProductVariant, SubCategory, TechnicalDetail
from product.permissions import IsOwner, IsSellerVerified
from product.serializers import (
    ProductListSerializer,
    ProductSerializerForAny,
    ProductSerializerForOwner,
    ProductTechnicalDetailSerializer,
    ProductVariantSerializerForOwner,
)


class ProductList(ListCreateAPIView):
    """
    GET method:
    Providing a subcategory via query parameter in the URL is required.
    ordering field options: main_price, rating, created_at, view_count.
    if you want the ordering to be descending, use - in front of the field.
    example: ?ordering=-view_count
    tags provided by the query parameter should be seperated by comma.
    example: ?tags=tag1,tag2
    POST method:
    Only for authenticated users and admins. users also should have their
    seller profile verified, otherwise, they will get a 403 error.
    """

    permission_classes = [IsSellerVerified]
    queryset = Product.objects.filter(is_valid=True).with_in_stock()
    serializer_class = ProductListSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = ProductFilter
    ordering_fields = ["main_price", "rating", "created_at", "view_count", "in_stock"]
    ordering = ["-created_at", "in_stock"]

    def _validate_subcategory(self) -> None:
        subcategory_name = self.request.query_params.get("subcategory")
        if not subcategory_name:
            raise ValidationError(
                "query parameter 'subcategory' should be provided", "no_query_param"
            )
        if not SubCategory.objects.filter(name__iexact=subcategory_name).exists():
            raise ValidationError("subcategory does not exist", "subcategory_not_found")

    def get_queryset(self):
        self._validate_subcategory()
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner & IsSellerVerified]
    queryset = Product.objects.all()
    _cached_object = None

    def get_object(self):
        if not self._cached_object:
            self._cached_object = super().get_object()
        return self._cached_object

    def get_serializer_class(self):
        product = self.get_object()
        if self.request.user == product.owner:
            return ProductSerializerForOwner
        else:
            return ProductSerializerForAny

    def get(self, request, *args, **kwargs):
        """
        Increase the view count of a product but with the constraint of having a cooldown
        period of one day for each client, which is handled by caching the client's IP.
        """
        product_obj = self.get_object()
        serializer = self.get_serializer(product_obj)
        user_ip, _ = get_client_ip(self.request)
        if not user_ip:
            return Response(serializer.data)
        self._cache_client_ip(product_obj, user_ip)
        return Response(serializer.data)

    def _cache_client_ip(self, product_obj, user_ip):
        redis_key = f"product:{product_obj.id}:ip:{user_ip}"
        redis_client = cache.client.get_client()
        if redis_client.exists(redis_key) == 0:
            product_obj.increase_view_count()
            cooldown_period = 3600 * 24  # one hour in seconds * number of hours
            redis_client.setex(redis_key, cooldown_period, 1)  # 1 is a dummy value


class ProductVariantDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner & IsSellerVerified]
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializerForOwner
    lookup_url_kwarg = "variant_pk"


class ProductVariantList(ListCreateAPIView):
    permission_classes = [IsSellerVerified]
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializerForOwner

    def get_product(self):
        product_pk = self.kwargs.get("product_pk")
        return get_object_or_404(Product, id=product_pk)

    def get_queryset(self):
        product_obj = self.get_product()
        return super().get_queryset().filter(product=product_obj).order_by("id")

    def perform_create(self, serializer):
        product_obj = self.get_product()
        serializer.save(product=product_obj)


class ProductTechnicalInfoDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSellerVerified]
    queryset = TechnicalDetail.objects.all()
    serializer_class = ProductTechnicalDetailSerializer
    lookup_url_kwarg = "technical_pk"


class ProductTechnicalInfoList(ListCreateAPIView):
    permission_classes = [IsSellerVerified]
    queryset = TechnicalDetail.objects.all()
    serializer_class = ProductTechnicalDetailSerializer

    def get_product(self):
        product_pk = self.kwargs.get("product_pk")
        return get_object_or_404(Product, id=product_pk)

    def get_queryset(self):
        product_obj = self.get_product()
        return super().get_queryset().filter(product=product_obj).order_by("id")

    def perform_create(self, serializer):
        product_obj = self.get_product()
        serializer.save(product=product_obj)

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, list):  # bulk
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            data=serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ShopProductList(ListAPIView):
    "Lists all products belonging to current authenticated seller"

    permission_classes = [IsSellerVerified]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
