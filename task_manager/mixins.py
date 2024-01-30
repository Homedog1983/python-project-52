from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
# from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.functions import (
    redirect_with_warning_message,
    redirect_with_send_report_and_warning_message)


class LoginRequiredRedirectMixin(LoginRequiredMixin):
    message_not_authenticated = _(
        'You are not login. Please, login')
    __redirect_url_name = 'login'

    def handle_no_permission(self):
        return redirect_with_warning_message(
            self.request, self.message_not_authenticated,
            self.__redirect_url_name)


class ObjectUnusedRequaredMixin:
    '''
    Check object's usage in some task.
    If is used - redirect with message.
    Attrs: message_used_object: str, url_name_object_used,
    message_success: str, url_name_success: str
    '''
    message_used_object = _('Unable to delete because it is used in task!')
    url_name_object_used = "main_page"
    __message_object_has_not_attr = _(
        'Enternal error: Unable to delete object!')
    __report_message = _("Object has not attr is_object_in_use")

    def form_valid(self, form):
        try:
            getattr(self.object, 'is_object_in_use')
            if self.object.is_object_in_use():
                return redirect_with_warning_message(
                    self.request, self.message_used_object,
                    self.url_name_object_used)
            return super().form_valid(form)
        except AttributeError:
            return redirect_with_send_report_and_warning_message(
                self.__report_message, self.request,
                self.__message_object_has_not_attr,
                self.url_name_object_used)


class CreatorRequaredMixin:
    """ Creator requared (if not - redirect with message). """
    message_not_creator = _(
        'Object is possible to change for its creator only!')
    url_name_not_creator = "main_page"

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            object = get_object_or_404(self.model, id=kwargs['pk'])
            if request.user.username != object.get_creator_username():
                return redirect_with_warning_message(
                    request, self.message_not_creator,
                    self.url_name_not_creator)
        return super().dispatch(request, *args, **kwargs)


# class CreatorRequaredMixin(UserPassesTestMixin):
#     message_not_creator = _(
#         'Object is possible to change for its creator only!')
#     url_name_not_creator = "main_page"

#     def test_func(self):
#         print('test func: request method: ', self.request.method)
#         object = get_object_or_404(self.model, id=kwargs['pk'])
#         return True

#     def dispatch(self, request, *args: Any, **kwargs: Any):
#         if request.method == "GET":
#             print("request method: ", self.request.method)
#             if not self.test_func():
#                 messages.warning(request, self.message_not_creator)
#                 return redirect(reverse(self.url_name_not_creator))
#         return super().dispatch(request, *args, **kwargs)
