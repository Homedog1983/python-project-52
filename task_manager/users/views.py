from django.utils.translation import gettext as _
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from task_manager.mixins import (
    SuccessMessageRedirectMixin,
    TaskUnusedRequaredDeletionMixin)
from .mixins import (
    CommonUserDetailMixin, ChangeUserRedirectMixin)


class UserIndexView(ListView):
    model = User
    template_name = 'users/index.html'


class UserCreateView(
        CommonUserDetailMixin,
        SuccessMessageRedirectMixin,
        CreateView):
    form_class = CustomUserCreationForm
    extra_context = {
        'h1_value': _('Registration'),
        'button_value': _('Register'),
    }
    url_name_success = "login"
    message_success = _("User is registered successfully")


class UserUpdateView(
        ChangeUserRedirectMixin,
        SuccessMessageRedirectMixin,
        UpdateView):
    form_class = CustomUserCreationForm
    extra_context = {
        'header': _('User update'),
        'button_value': _('Update'),
    }
    message_success = _("User is updated successfully")


class UserDeleteView(
        ChangeUserRedirectMixin,
        TaskUnusedRequaredDeletionMixin,
        DeleteView):
    template_name = 'users/delete.html'
    message_success = _("User is deleted successfully")
    url_name_success, url_name_object_used = 'users_index', 'users_index'
