from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from task_manager.users.models import CustomUser
from task_manager.mixins import (
    LoginRequiredRedirectMixin, CreatorRequaredMixin)


class CommonUserDetailMixin:
    """
    Common attrs for all instead IndexView.
    Use attr 'success_message' to define non-default message
    """
    model = CustomUser
    template_name = 'users/detail.html'


class ChangeUserMixin(
        LoginRequiredRedirectMixin,
        CreatorRequaredMixin,
        CommonUserDetailMixin):
    """ Required common mixin's sequence for user's update and delete."""
    success_url = reverse_lazy('users_index')
    url_name_not_creator = "users_index"
    message_not_creator = _(
        'You are have not permission to change other user!')
