from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

from product import views

urlpatterns = [
    path("<int:pk>/", views.ProductDetail.as_view(), name="product-detail"),
    path("", views.ProductList.as_view(), name="product-list"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
