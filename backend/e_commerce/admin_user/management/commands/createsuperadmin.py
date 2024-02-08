from admin.models import Admin
from django.contrib.auth.management.commands import createsuperuser

class Command(createsuperuser.Command):
    help = "Create an admin with superadmin role"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = Admin
        