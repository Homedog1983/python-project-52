from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from task_manager.mixins import SuccessMessageRedirectMixin


class UsersDetailMixin:
    """
    Add common user detail.
    """
    template_name = 'users/detail.html'
    form_class = CustomUserCreationForm


class SameLoginUserRequaredMixin:
    """
    1. Authenticate requared.
    2. Same user requared.
    If not - return redirect with message (changed for 1 and 2 ways)
    """
    message_not_authenticated = _(
        'You are not login. Please, login!')
    message_not_same_user = _(
        'You are have not permission to change other user!')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(request, self.message_not_authenticated)
            return redirect("login")
        requared_user = get_object_or_404(User, id=kwargs['pk'])
        if user.username != requared_user.username:
            messages.warning(request, self.message_not_same_user)
            return redirect("users_index")
        return super().dispatch(request, *args, **kwargs)


class UsersIndexView(ListView):
    model = User
    template_name = 'users/index.html'


class UsersCreateFormView(
        SuccessMessageRedirectMixin,
        UsersDetailMixin,
        CreateView):
    extra_context = {
        'h1_value': _('Registration'),
        'button_value': _('Register'),
        }
    url_name = "login"
    success_message = _("User is registered successfully!")


class UsersUpdateFormView(
        SameLoginUserRequaredMixin,
        SuccessMessageRedirectMixin,
        UsersDetailMixin,
        UpdateView):
    model = User
    extra_context = {
        'h1_value': _('User update'),
        'button_value': _('Update'),
        }
    url_name = 'users_index'
    success_message = _("User is updated successfully!")


class UsersDeleteFormView(
        SameLoginUserRequaredMixin,
        SuccessMessageRedirectMixin,
        DeleteView):
    model = User
    template_name = 'users/delete.html'
    url_name = 'users_index'
    success_message = _("User was deleted successfully!")
