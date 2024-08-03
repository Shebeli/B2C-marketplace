import os 
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULES", "ecom_core.settings")
app = Celery("ecom_core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()