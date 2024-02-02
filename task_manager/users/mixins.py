from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import UserPassesTestMixin


class OwnerRequaredMixin(UserPassesTestMixin):
    message_not_owner = _(
        'You are have not permission to change other user!')
    url_name_not_owner = "users_index"

    def test_func(self):
        return self.request.user == self.get_object()

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            messages.warning(self.request, self.message_not_owner)
            return redirect(reverse(self.url_name_not_owner))
        return super().dispatch(request, *args, **kwargs)
