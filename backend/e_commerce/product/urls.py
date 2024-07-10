from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

from product import views

urlpatterns = [
    path("<int:pk>/", views.ProductDetail.as_view()),
    path("", views.ProductList.as_view()),
    path("tags/", views.TagProductsList.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
