from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from ecom_admin.models import EcomAdmin


# for django authentication
class AdminBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        if (username is None and email is None) or password is None:
            return
        try: 
            ecom_admin = EcomAdmin.objects.get(Q(username=username) | Q(email=email))
        except EcomAdmin.DoesNotExist:
            return None
        else:
            if ecom_admin.check_password(password) and self.user_can_authenticate(ecom_admin):
                return ecom_admin

    def get_user(self, user_id):
        try:
            return EcomAdmin.objects.get(pk=user_id)
        except EcomAdmin.DoesNotExist:
            return None

# rest API authentication  
class EcomAdminJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_model = EcomAdmin
