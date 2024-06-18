from rest_framework.routers import DefaultRouter

from product.views import ProductViewSet, CategoryViewSet, ProductList

router = DefaultRouter()

router.register(r"category-products", ProductList, basename="list-products")
router.register(r"product", ProductViewSet, basename="product")
router.register(r"category", CategoryViewSet, basename="category")