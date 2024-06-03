from rest_framework.routers import DefaultRouter

from product.views import ProductViewSet, CategoryViewSet, CategoryProductsViewSet

router = DefaultRouter()

router.register(r"category-products", CategoryProductsViewSet, basename="category-products")
router.register(r"product", ProductViewSet, basename="product")
router.register(r"category", CategoryViewSet, basename="category")