from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib import messages


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
    message_success: str, url_name_success: str
    '''
    message_used_object = _('Unable to delete because it is used in task!')
    url_name_object_used = "main_page"
    message_success = _("Object is deleted successfully!")
    url_name_success = "main_page"

    def is_task_used(self):
        model_name = self.object.__class__.__name__
        if model_name in ["Label", "Status"]:
            return True if self.object.task_set.all() else False
        # User had two related managers, both differ from task_set
        if self.object.task_creator_set.all():
            return True
        if self.object.task_executor_set.all():
            return True
        return False

    def form_valid(self, form):
        if self.is_task_used():
            messages.warning(self.request, self.message_used_object)
            return redirect(self.url_name_object_used)
        messages.success(self.request, self.message_success)
        self.object.delete()
        return redirect(self.url_name_success)
