from django.db.models import Q
from django.contrib.auth.backends import ModelBackend

from .models import AdminUser


class AdminBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        if (username is None and email is None) or password is None:
            return
        try: 
            admin_user = AdminUser.objects.get(Q(username=username) | Q(email=email))
        except AdminUser.DoesNotExist:
            return None
        else:
            if admin_user.check_password(password) and self.user_can_authenticate(admin_user    ):
                return admin_user

    def get_user(self, user_id):
        try:
            return AdminUser.objects.get(pk=user_id)
        except AdminUser.DoesNotExist:
            return None
