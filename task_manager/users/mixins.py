from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from task_manager.mixins import LoginRequiredRedirectMixin


class CommonUserDetailMixin:
    """
    Common attrs for all instead IndexView.
    Use attr 'success_message' to define non-default message
    """
    model = User
    template_name = 'users/detail.html'


class CreatorRequaredRedirectMixin:
    """ Same user requared (if not - redirect with message). """
    message_not_creator = _(
        'You are have not permission to change other user!')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        requared_user = get_object_or_404(User, id=kwargs['pk'])
        if user.username != requared_user.username:
            messages.warning(request, self.message_not_creator)
            return redirect(reverse("users_index"))
        return super().dispatch(request, *args, **kwargs)


class ChangeUserRedirectMixin(
        LoginRequiredRedirectMixin,
        CreatorRequaredRedirectMixin,
        CommonUserDetailMixin):
    """ Required common mixin's sequence for user's update and delete."""
    success_url = reverse_lazy('users_index')
