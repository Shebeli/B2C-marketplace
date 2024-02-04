from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class MyUserManager(BaseUserManager):
    pass

class EcomUser(AbstractBaseUser):
    pass