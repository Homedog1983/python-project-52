from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .mixins import SuccessMessageRedirectMixin


class IndexView(TemplateView):
    template_name = "index.html"


class CustomLoginView(SuccessMessageRedirectMixin, LoginView):
    template_name = "login.html"
    success_message = _("You are logged in!")


class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        messages.info(request, _("You are logged out!"))
        return redirect("main_page")
