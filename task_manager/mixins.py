from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredRedirectMixin(LoginRequiredMixin):
    message_not_authenticated = _(
        'You are not login. Please, login')
    redirect_url_name = 'login'

    def handle_no_permission(self):
        messages.warning(self.request, self.message_not_authenticated)
        return redirect(reverse(self.redirect_url_name))


class ObjectUnusedRequaredMixin:
    '''
    Check object's usage in some task.
    If is used - redirect with message.
    Attrs: message_used_object: str, url_name_object_used,
    message_success: str, url_name_success: str
    '''
    message_used_object = _('Unable to delete because it is used in task!')
    url_name_object_used = "main_page"
    message_object_has_not_attr = _(
        'Enternal error: Unable to delete object!')
    report_message = _("Object has not attr is_object_in_use")

    def form_valid(self, form):
        if not hasattr(self.object, 'is_object_in_use'):
            return super().form_valid(form)
        if self.object.is_object_in_use():
            messages.warning(self.request, self.message_used_object)
            return redirect(reverse(self.url_name_object_used))
        return super().form_valid(form)
