from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from task_manager.mixins import (
    SuccessMessageRedirectMixin,
    LoginRequiredRedirectMixin,
    TaskUnusedRequaredDeletionMixin)


class UserIndexView(ListView):
    model = User
    template_name = 'users/index.html'


class CommonUserDetailMixin:
    """
    Common attrs for all views below.
    Use attr 'success_message' to define non-default message
    """
    model = User
    template_name = 'users/detail.html'


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
    message_success = _("User is registered successfully!")


class CreatorRequaredRedirectMixin:
    """ Same user requared (if not - redirect with message). """
    message_not_creator = _(
        'You are have not permission to change other user!')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        requared_user = get_object_or_404(User, id=kwargs['pk'])
        if user.username != requared_user.username:
            messages.warning(request, self.message_not_creator)
            return redirect("users_index")
        return super().dispatch(request, *args, **kwargs)


class ChangeUserRedirectMixin(
        LoginRequiredRedirectMixin,
        CreatorRequaredRedirectMixin,
        CommonUserDetailMixin):
    """ Required common mixin's sequence for user's update and delete."""
    url_name_success = 'users_index'


class UserUpdateView(
        ChangeUserRedirectMixin,
        SuccessMessageRedirectMixin,
        UpdateView):
    form_class = CustomUserCreationForm
    extra_context = {
        'h1_value': _('User update'),
        'button_value': _('Update'),
        }
    message_success = _("User is updated successfully!")


class UserDeleteView(
        ChangeUserRedirectMixin,
        TaskUnusedRequaredDeletionMixin,
        DeleteView):
    template_name = 'users/delete.html'
    message_success = _("User is deleted successfully!")
    url_name_success, url_name_object_used = 'users_index', 'users_index'
