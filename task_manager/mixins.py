from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
import rollbar


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
            rollbar.report_message(self.report_message, "fatal")
            messages.warning(self.request, self.message_object_has_not_attr)
            return redirect(reverse(self.url_name_object_used))
        if self.object.is_object_in_use():
            messages.warning(self.request, self.message_used_object)
            return redirect(reverse(self.url_name_object_used))
        return super().form_valid(form)


# class CreatorRequaredMixin:
#     """ Creator requared (if not - redirect with message). """
#     message_not_creator = _(
#         'Object is possible to change for its creator only!')
#     url_name_not_creator = "main_page"

#     def dispatch(self, request, *args, **kwargs):
#         print("request.method: ", self.request.method)
#         print("get object from DB")
#         object = self.get_object()
#         if request.user != object.get_creator():
#             messages.warning(self.request, self.message_not_creator)
#             return redirect(reverse(self.url_name_not_creator))
#         return super().dispatch(request, *args, **kwargs)


class CreatorRequaredMixin(UserPassesTestMixin):
    message_not_creator = _(
        'Object is possible to change for its creator only!')
    url_name_not_creator = "main_page"

    def test_func(self):
        print("use test func - get object from DB")
        object = self.get_object()
        return self.request.user == object.get_creator()

    def dispatch(self, request, *args, **kwargs):
        print("dispatch")
        print("request.method: ", self.request.method)
        if not self.test_func():
            messages.warning(self.request, self.message_not_creator)
            return redirect(reverse(self.url_name_not_creator))
        return super().dispatch(request, *args, **kwargs)
