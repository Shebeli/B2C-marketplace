from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from order import views

urlpatterns = [
    path("callback/", views.ZibalCallbackView.as_view(), name="zibal-callback"),
]
