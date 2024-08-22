from django.contrib.auth.management.commands import createsuperuser

from ecom_admin.models import EcomAdmin


class Command(createsuperuser.Command):
    help = "Create an admin with superadmin role"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = EcomAdmin
        