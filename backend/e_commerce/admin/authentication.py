from django.db.models import Q
from django.contrib.auth.backends import ModelBackend

from .models import Admin


class AdminBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        if (username is None and email is None) or password is None:
            return
        try: 
            admin = Admin.objects.get(Q(username=username) | Q(email=email))
        except Admin.DoesNotExist:
            return None
        else:
            if admin.check_password(password) and self.user_can_authenticate(admin):
                return admin

    def get_user(self, user_id):
        try:
            return Admin.objects.get(pk=user_id)
        except Admin.DoesNotExist:
            return None
