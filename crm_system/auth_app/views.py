from django.http.response import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):
    """Представление login"""

    template_name = "auth_app/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """Представление logout"""

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs) -> HttpResponseRedirect:
        """Logout выполняется через GET."""
        logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            # Redirect to target page once the session has been cleared.
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)
