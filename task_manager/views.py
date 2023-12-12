# from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _


class IndexView(TemplateView):
    template_name = "index.html"


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    success_message = _("You are logged in!")


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    success_message = _("You are logged out!")
