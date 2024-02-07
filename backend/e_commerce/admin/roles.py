from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

class AdminRoles(TextChoices):
    SUPERVISOR = "SV", _("Supervisor")
    MANAGER = "MG", _("Manager")
    SUPERADMIN = "SA", _("Superadmin")
    