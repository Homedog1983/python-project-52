from django.utils.translation import gettext as _
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from .models import Status
from .forms import StatusForm
from task_manager.mixins import (
    LoginRequiredRedirectMixin, SuccessMessageRedirectMixin)


class StatusIndexView(LoginRequiredRedirectMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'


class CommonStatusMixin(
        LoginRequiredRedirectMixin,
        SuccessMessageRedirectMixin):
    model = Status
    template_name = 'statuses/detail.html'
    url_name = 'statuses_index'


class StatusCreateView(CommonStatusMixin, CreateView):
    form_class = StatusForm
    extra_context = {
        'h1_value': _('Status creation'),
        'button_value': _('Create'),
        }
    success_message = _("Status is created successfully!")


class StatusUpdateView(CommonStatusMixin, UpdateView):
    form_class = StatusForm
    extra_context = {
        'h1_value': _('Status update'),
        'button_value': _('Update'),
        }
    success_message = _("Status is updated successfully!")


class StatusDeleteView(CommonStatusMixin, DeleteView):

    # В диспатч ввести проверку в обратную сторону if not task_set
    # редирект с warning сообщением

    template_name = 'statuses/delete.html'
    success_message = _("User was deleted successfully!")
