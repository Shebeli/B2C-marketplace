from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import phonenumbers
# this model does not contain any superuser or admin, as theres a seperate model for that purpose.
class EcomUser(AbstractBaseUser):
    first_name = models.CharField()
    last_name = models.CharField()
    username = models.CharField()
    
phonenumbers.parse()