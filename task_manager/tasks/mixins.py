from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import UserPassesTestMixin


class CreatorRequaredMixin(UserPassesTestMixin):
    message_not_creator = _(
        "Task is possible to delete for its creator only!")
    url_name_not_creator = "tasks_index"

    def test_func(self):
        return self.request.user == self.get_object().creator

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            messages.warning(self.request, self.message_not_creator)
            return redirect(reverse(self.url_name_not_creator))
        return super().dispatch(request, *args, **kwargs)
