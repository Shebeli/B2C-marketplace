from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

class EcomUserManager(BaseUserManager):

    def create_user(self, username, phone, password=None, **extra_fields):
        if not username and not phone:
            raise ValueError("Username or phone should be provided")
        UserModel = get_user_model()
        if username:
            username = UserModel.normalize_username(username)
        if phone:
            phone = self.normalize_phone(phone)

        user = self.model(username=username, phone=phone, **extra_fields) # either username or phone can be null here
        user.set_password(password)
        user.save(using=self._db)
        return user

    
        
