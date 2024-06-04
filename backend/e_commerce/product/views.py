from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.decorators import action

from product.models import Product, Category, Tag
from product.serializers import (
    ProductSerializer,
    ProductListSerializer,
    CategorySerializer,
    TagSerializer,
    TechnicalDetailSerializer
)
from product.permissions import IsAdminOrReadOnly


class CategoryProductsViewSet(GenericViewSet, ListModelMixin):
    "For listing all products belonging to a certain category."
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_category_name_or_400(self):
        category_name = self.request.query_params.get("category")
        if not category_name:
            raise ParseError("Query parameter 'category' should be provided")
        return category_name

    def get_queryset(self):
        category_name = self.get_category_name_or_400()
        products = self.queryset.filter(category__name__iexact=category_name)
        if not products:
            raise NotFound("No products were found with the inputted category name")
        return products


class TagProductsViewSet(GenericViewSet, ListModelMixin):
    "For listing all products belonging to a certain tag or list of tags"
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_tag_names_or_400(self):
        tag_names = self.request.query_params.getlist("tag")
        if not tag_names:
            raise ParseError("Query parameter 'tag' should be provided")
        return tag_names

    def get_queryset(self):
        tag_names = self.get_tag_names_or_400()
        products = self.queryset.filter(tags__name__in=tag_names)
        if not products:
            raise NotFound("No products were found with the inputted tag name(s)")
        return products


class ProductViewSet(ModelViewSet):
    """
    Admins can modify or delete existing products and create new products.
    Non-admin users can only retrieve the information of a product.
    """

    permission_classes = [IsAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ProductsTechnicalDetailViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = TechnicalDetailSerializer

    # def 