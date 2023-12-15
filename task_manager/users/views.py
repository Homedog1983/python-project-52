from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from task_manager.mixins import (
    SuccessMessageRedirectMixin, LoginRequiredRedirectMixin)


class UserIndexView(ListView):
    model = User
    template_name = 'users/index.html'


class CommonUserDetailMixin(SuccessMessageRedirectMixin):
    """
    Common attrs for all views below.
    Use attr 'success_message' to define non-default message
    """
    model = User
    template_name = 'users/detail.html'


class UserCreateView(CommonUserDetailMixin, CreateView):
    form_class = CustomUserCreationForm
    extra_context = {
        'h1_value': _('Registration'),
        'button_value': _('Register'),
        }
    url_name = "login"
    success_message = _("User is registered successfully!")


class SameUserRequaredRedirectMixin:
    """ Same user requared (if not - redirect with message). """
    message_not_same_user = _(
        'You are have not permission to change other user!')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        requared_user = get_object_or_404(User, id=kwargs['pk'])
        if user.username != requared_user.username:
            messages.warning(request, self.message_not_same_user)
            return redirect("users_index")
        return super().dispatch(request, *args, **kwargs)


class ChangeUserRedirectMixin(
        LoginRequiredRedirectMixin,
        SameUserRequaredRedirectMixin,
        CommonUserDetailMixin):
    """ Required common mixin's sequence for user's update and delete."""
    url_name = 'users_index'


class UserUpdateView(ChangeUserRedirectMixin, UpdateView):
    form_class = CustomUserCreationForm
    extra_context = {
        'h1_value': _('User update'),
        'button_value': _('Update'),
        }
    success_message = _("User is updated successfully!")


class UserDeleteView(ChangeUserRedirectMixin, DeleteView):
    template_name = 'users/delete.html'
    success_message = _("User is deleted successfully!")
