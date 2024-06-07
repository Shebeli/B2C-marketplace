from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

from .views import CustomerProfileAPIView

urlpatterns = [
    path('customer-profile/', CustomerProfileAPIView.as_view(), name='customer-profile'),
]