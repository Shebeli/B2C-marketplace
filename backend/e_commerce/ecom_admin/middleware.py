from django.http import HttpResponseRedirect
from django.urls import reverse


class AdminPanelAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # if the path is an admin route, and the user is authenticated and the user is not an admin
        if request.path.startswith('/admin/') and request.user.is_authenticated:
            if not request.user.is_admin:
                # if the user tries to access a path on /admin/ route, redirect them to login
                if request.path != reverse("admin:login"):
                    return HttpResponseRedirect(reverse) 
        return self.get_response(request)