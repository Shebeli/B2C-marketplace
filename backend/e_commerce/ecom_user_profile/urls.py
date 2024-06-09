from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter
from django.urls import path

from ecom_user_profile import views

# router = SimpleRouter()

# router.register(r'customer-profile', CustomerProfileViewSet, basename='customer-profile')
urlpatterns = [
    path("customer-profile/", views.CustomerProfileAPIView.as_view(), name='customer-profile'),
    path("customer-addresses/", views.CustomerAddressList.as_view(), name='customer-addresses-list'),
    path("customer-addresses/<int:pk>/", views.CustomerAddressDetail.as_view(), name='customer-addresses-detail'),
    path("seller-profile/", views.SellerProfileAPIView.as_view(), name='seller-profile'),
    path("seller-business-licenses/", views.SellerBusinessLicenseList.as_view(), name='seller-business-licenses-list'),
    path("seller-business-licenses/<int:pk>/", views.SellerBusinessLicenseDetail.as_view(), name='seller-business-licenses-detail'),
    path("seller-bank-accounts/", views.SellerBankAccountList.as_view(), name='seller-bank-accounts-list'),
    path("seller-bank-accounts/<int:pk>/", views.SellerBankAccountDetail.as_view(), name='seller-bank-accounts-detail'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
