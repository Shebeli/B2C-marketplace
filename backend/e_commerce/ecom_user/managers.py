from typing import Any

import phonenumbers
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .exceptions import CommandNotAllowedException


class EcomUserManager(BaseUserManager):

    def create_user(self, username="", phone="", email="", password=""):
        if not username and not phone:
            raise ValueError("Either username or phone should be provided")
        UserModel = get_user_model()
        if username:
            username = UserModel.normalize_username(username)
        if phone:
            phone = self.normalize_phone(phone)
        email = self.normalize_email(email)
        user = self.model(
            username=username, phone=phone, email=email
        )  # either username or phone can be blank here
        user.set_password(password)
        user.save(using=self._db)
        return user

    def normalize_phone(self, phone) -> str:
        if phone:
            parsed_phone = phonenumbers.parse(phone, "IR")
            phone = phonenumbers.format_number(
                parsed_phone, phonenumbers.PhoneNumberFormat.NATIONAL
            ).replace(
                " ", ""
            )  # eg: 09377954148
        return phone

    def create_superuser(self):
        raise CommandNotAllowedException(
            _(
                """
                The application user model doesn't allow staff or superuser object to be created 
                on the EcomUser model. Use the command createsuperadmin instead to create an 
                instance of the model EcomAdmin, which is a seperate user model.
                """
            )
        )
