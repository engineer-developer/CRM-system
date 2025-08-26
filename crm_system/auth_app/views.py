from django.http.response import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):
    """Представление login"""

    template_name = "auth_app/login.html"
    redirect_authenticated_user = True


# Create your views here.
