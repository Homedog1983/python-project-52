from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError


class LoginRequiredRedirectMixin:
    """
    Requared login on dispath.
    If not returns redirect('login') with message.
    Attrs: message_not_authenticated: str
    """
    message_not_authenticated = _(
        'You are not login. Please, login!')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(request, self.message_not_authenticated)
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class SuccessMessageRedirectMixin:
    """
    Add a success message after successful form submission.
    Attrs: message_success: str, url_name_success: str
    """
    url_name_success = "main_page"
    message_success = _("All you wanted is succefully happened!")

    def form_valid(self, form):
        super().form_valid(form)
        if self.message_success:
            messages.success(self.request, self.message_success)
        return redirect(self.url_name_success)

    def get_success_url(self):
        return reverse(self.url_name_success)


class TaskUnusedRequaredDeletionMixin:
    '''
    Check object's usage in some task.
    If is used - prevent delete (redirect with message).
    If isn't used - delete (redirect with message)
    Attrs: message_used_object: str, url_name_object_used,
    message_success: str, url_name_success: str,
    You can set only url_name:str for both redirects
    '''
    url_name = 'main_page'
    message_used_object = _('Unable to delete! This object is bounded!')
    url_name_object_used = url_name
    message_success = _("Object is deleted successfully!")
    url_name_success = url_name

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, self.message_success)
        except IntegrityError:
            messages.warning(self.request, self.message_used_object)
            redirect(self.url_name_object_used)
        return redirect(self.url_name_success)

    # def form_valid(self, form):
    #     print('task_set: ', self.object.task_set)
    #     if self.object.task_set.all():
    #         messages.warning(self.request, self.message_used_object)
    #         redirect(self.url_name_object_used)
    #     self.object.delete()
    #     messages.success(self.request, self.message_success)
    #     return redirect(self.url_name_success)
