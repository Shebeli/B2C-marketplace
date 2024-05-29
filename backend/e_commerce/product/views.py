from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions 
from rest_framework_simplejwt.authentication import JWTAuthentication

from product.models import Product, Category
from product.serializers import ProductSerializer, ProductListSerializer, CategorySerializer
from product.permissions import IsAdminOrReadOnly


class CategoryProductsViewSet(GenericViewSet, ListModelMixin):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_category_name_or_400(self):
        category_name = self.request.query_params.get("category")
        if not category_name:
            raise exceptions.ParseError("Query parameter 'category' should be provided")
        return category_name

    def get_category_obj_or_404(self, category_name):
        category_obj = Category.objects.filter(name=category_name).first()
        if not category_obj:
            raise exceptions.NotFound("Given category name wasn't found")
        return category_obj

    def get_queryset(self):
        category_name = self.get_category_name_or_400()
        category_obj = self.get_category_obj_or_404(category_name)
        return self.queryset.filter(category=category_obj)


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

