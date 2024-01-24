from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib import messages


class LoginRequiredRedirectMixin:
    """
    Requared login on dispath.
    If not - returns redirect('login') with message.
    Attrs: message_not_authenticated: str
    """
    message_not_authenticated = _(
        'You are not login. Please, login')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(request, self.message_not_authenticated)
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)


def is_object_used_in_task(object):
    model_name = object.__class__.__name__
    if model_name in ["Label", "Status"]:
        return True if object.task_set.all() else False
    # User had two related managers, both differ from task_set
    if object.task_creator_set.all():
        return True
    if object.task_executor_set.all():
        return True
    return False


class ObjectUnusedRequaredMixin:
    '''
    Check object's usage in some task.
    If is used - redirect with message.
    Attrs: message_used_object: str, url_name_object_used,
    message_success: str, url_name_success: str
    '''
    message_used_object = _('Unable to delete because it is used in task!')
    url_name_object_used = "main_page"

    def form_valid(self, form):
        if is_object_used_in_task(self.object):
            messages.warning(self.request, self.message_used_object)
            return redirect(reverse(self.url_name_object_used))
        return super().form_valid(form)


class CreatorRequaredRedirectMixin:
    """ Creator requared (if not - redirect with message). """
    message_not_creator = _(
        'Object is possible to change for its creator only!')
    url_name_not_creator = "main_page"

    def dispatch(self, request, *args, **kwargs):
        object = get_object_or_404(self.model, id=kwargs['pk'])
        if self.model.__name__ == 'CustomUser':
            requared_username = object.username
        else:
            requared_username = object.creator.username
        if request.user.username != requared_username:
            messages.warning(request, self.message_not_creator)
            return redirect(reverse(self.url_name_not_creator))
        return super().dispatch(request, *args, **kwargs)
