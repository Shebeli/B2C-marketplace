from admin_user.models import AdminUser
from django.contrib.auth.management.commands import createsuperuser

class Command(createsuperuser.Command):
    help = "Create an admin with superadmin role"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = AdminUser
        