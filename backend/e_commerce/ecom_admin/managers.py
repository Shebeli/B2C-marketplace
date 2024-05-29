from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class EcomAdminManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not username or not email:
            raise ValueError(_("Username and email should be provided"))
        if extra_fields.get("role") == self.model.SUPERADMIN.value:
            raise ValueError(_("Superadmin cannot be created this way. use the command createsuperadmin instead."))
        extra_fields.set("is_active", False)
        ecom_admin = self.model(
            username=self.model.normalize_username(username),
            email=self.normalize_email(email),
            **extra_fields
        )
        ecom_admin.set_password(password)
        ecom_admin.save()
        return ecom_admin

    def create_superuser(self, email, username, password):
        if not username or not email:
            raise ValueError(_("Username and email should be provided"))
        ecom_admin = self.model(
            username=self.model.normalize_username(username),
            email=self.normalize_email(email),
            is_active=True,
            role= self.model.SUPERADMIN.value
        )
        ecom_admin.set_password(password)
        ecom_admin.save()
        return ecom_admin