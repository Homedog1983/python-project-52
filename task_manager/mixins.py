from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib import messages


class LoginRequiredRedirectMixin:
    """
    Requared login (if not - redirect to 'login'
    with message
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
    Add a success message on successful form submission.
    Redirect to reverse(url_name)
    """
    url_name = "main_page"
    success_message = _("All you wanted is succefully happened!")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response

    def get_success_url(self):
        return reverse(self.url_name)
