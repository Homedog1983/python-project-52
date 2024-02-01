from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from task_manager.users.models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import ObjectUnusedRequaredMixin
from .mixins import ChangeUserMixin


class UserIndexView(ListView):
    model = CustomUser
    template_name = 'users/index.html'


class UserCreateView(
        SuccessMessageMixin,
        CreateView):
    model = CustomUser
    template_name = 'users/form.html'
    form_class = CustomUserCreationForm
    extra_context = {
        'header': _('Registration'),
        'button_text': _('Register')}
    success_url = reverse_lazy("login")
    success_message = _("User is registered successfully")


class UserUpdateView(
        ChangeUserMixin,
        SuccessMessageMixin,
        UpdateView):
    model = CustomUser
    template_name = 'users/form.html'
    form_class = CustomUserCreationForm
    extra_context = {
        'header': _('User update'),
        'button_text': _('Update')}
    success_message = _("User is updated successfully")


class UserDeleteView(
        ChangeUserMixin,
        ObjectUnusedRequaredMixin,
        SuccessMessageMixin,
        DeleteView):
    model = CustomUser
    template_name = 'users/delete.html'
    success_message = _("User is deleted successfully")
    url_name_object_used = 'users_index'
