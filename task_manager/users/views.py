from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import (
    TaskUnusedRequaredDeletionMixin)
from .mixins import (
    CommonUserDetailMixin, ChangeUserRedirectMixin)


class UserIndexView(ListView):
    model = User
    template_name = 'users/index.html'


class UserCreateView(
        CommonUserDetailMixin,
        SuccessMessageMixin,
        CreateView):
    form_class = CustomUserCreationForm
    extra_context = {
        'header': _('Registration'),
        'button_value': _('Register')}
    success_url = reverse_lazy("login")
    success_message = _("User is registered successfully")


class UserUpdateView(
        ChangeUserRedirectMixin,
        SuccessMessageMixin,
        UpdateView):
    form_class = CustomUserCreationForm
    extra_context = {
        'header': _('User update'),
        'button_value': _('Update')}
    success_message = _("User is updated successfully")


class UserDeleteView(
        ChangeUserRedirectMixin,
        TaskUnusedRequaredDeletionMixin,
        SuccessMessageMixin,
        DeleteView):
    template_name = 'users/delete.html'
    success_message = _("User is deleted successfully")
    url_name_success, url_name_object_used = 'users_index', 'users_index'
