from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class AdminManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not username or not email:
            raise ValueError(_("Username and email should be provided"))
        if extra_fields.get("role") == self.model.SUPERADMIN.value:
            raise ValueError(_("Superadmin cannot be created this way. use the command createsuperadmin instead."))
        extra_fields.set("is_active", False)
        admin = self.model(
            username=self.model.normalize_username(username),
            email=self.normalize_email(email),
            **extra_fields
        )
        admin.set_password(password)
        admin.save()
        return admin

    def create_superuser(self, email, username, password):
        if not username or not email:
            raise ValueError(_("Username and email should be provided"))
        admin = self.model(
            username=self.model.normalize_username(username),
            email=self.normalize_email(email),
            is_active=True,
            role= self.model.SUPERADMIN.value
        )
        admin.set_password(password)
        admin.save()
        return admin