from django.contrib import admin

from ecom_admin.models import EcomAdmin

from .admin_views import EcomAdminLoginView

admin.site.login = EcomAdminLoginView.as_view()
print("EcomAdminLoginView registered as login view")

original_has_permission = admin.site.has_permission


def custom_has_permission(request):
    if request.user.is_authenticated:
        return request.user.is_admin
    return False


admin.site.has_permission = custom_has_permission


class CustomDjangoAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")


admin.site.register(EcomAdmin, CustomDjangoAdmin)
