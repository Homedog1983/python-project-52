from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib import messages
# from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# import rollbar
# rollbar.init('POST_SERVER_ITEM_ACCESS_TOKEN', 'dev')


class LoginRequiredRedirectMixin(LoginRequiredMixin):
    message_not_authenticated = _(
        'You are not login. Please, login')

    def handle_no_permission(self):
        messages.warning(self.request, self.message_not_authenticated)
        return redirect(reverse('login'))


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
    __rollbar_message = _("Object has not attr is_object_in_use")

    def form_valid(self, form):
        try:
            getattr(self.object, 'is_object_in_use')
            if self.object.is_object_in_use():
                messages.warning(self.request, self.message_used_object)
                return redirect(reverse(self.url_name_object_used))
            return super().form_valid(form)
        except AttributeError:
            # rollbar.report_message(__rollbar_message, 'fatal')
            messages.warning(self.request, self.__message_object_has_not_attr)
            return redirect(reverse(self.url_name_object_used))


class CreatorRequaredMixin:
    """ Creator requared (if not - redirect with message). """
    message_not_creator = _(
        'Object is possible to change for its creator only!')
    url_name_not_creator = "main_page"

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            object = get_object_or_404(self.model, id=kwargs['pk'])
            if request.user.username != object.get_creator_username():
                messages.warning(request, self.message_not_creator)
                return redirect(reverse(self.url_name_not_creator))
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
