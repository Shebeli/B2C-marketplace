from django import forms
from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.utils.text import capfirst

from ecom_admin.models import EcomAdmin


class EcomAdminAuthenticationForm(AdminAuthenticationForm):
    username = forms.CharField(label="Username or Email", widget=forms.TextInput(attrs={"autofocus": True}))

    
    def __init__(self, request=..., *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        self.username_field = EcomAdmin._meta.get_field(EcomAdmin.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length
        if self.fields["username"].label is None:
            self.fields["username"].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get("username")  # might be email
        password = self.cleaned_data.get("password")

        if username and password:
            from django.contrib.auth import authenticate

            # identify whether the input is email or username.
            if "@" in username:
                self.user_cache = authenticate(email=username, password=password)
            else:
                self.user_cache = authenticate(username=username, password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                )
            # technically, the admin panel should be accessable only from inside the org
            elif not isinstance(self.user_cache, EcomAdmin):
                raise forms.ValidationError(
                    "Only admin users may use this portal", code="invalid_login"
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages["Inactive"], code="inactive"
                )
        return self.cleaned_data


class EcomAdminLoginView(LoginView):
    template_name = "admin/login.html"
    form_class = EcomAdminAuthenticationForm

    def get_success_url(self):
        return self.get_redirect_url() or admin.site.index(self.request)
