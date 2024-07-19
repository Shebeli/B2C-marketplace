from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

from product import views

urlpatterns = [
    path("<int:pk>/", views.ProductDetail.as_view(), name="product-detail"),
    path("", views.ProductList.as_view(), name="product-list"),
    path(
        "<int:product_pk>/variants",
        views.ProductVariantDetail.as_view(),
        name="variant-list",
    ),
    path(
        "<int:product_pk>/variants/<int:variant_pk>",
        views.ProductVariantList.as_view(),
        name="variants-detail",
    ),
    path(
        "<int:product_pk>/technical-infos/",
        views.ProductTechnicalInfoList.as_view(),
        name="technical-info-list",
    ),
    path(
        "<int:product_pk>/technical-infos/<int:technical_pk>",
        views.ProductTechnicalInfoDetail.as_view(),
        name="technical-info-detail",
    ),
]
urlpatterns = format_suffix_patterns(urlpatterns)
