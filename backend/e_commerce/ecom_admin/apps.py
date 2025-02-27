from django.apps import AppConfig


class EcomAdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ecom_admin"

    def ready(self):
        from django.contrib import admin

        from .admin_views import admin
        
        # admin.site.login = EcomAdminLoginView.as_view()
        # print("EcomAdminLoginView registered as login view from appconfig")