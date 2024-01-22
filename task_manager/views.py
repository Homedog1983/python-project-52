from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin


class IndexView(TemplateView):
    template_name = "index.html"


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    success_message = _("You are logged in")


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        messages.info(request, _("You are logged out"))
        return redirect(reverse("main_page"))
