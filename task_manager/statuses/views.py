from django.utils.translation import gettext as _
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from .models import Status
from .forms import StatusForm
from task_manager.mixins import (
        LoginRequiredRedirectMixin,
        SuccessMessageRedirectMixin,
        TaskUnusedRequaredDeletionMixin)


class StatusIndexView(LoginRequiredRedirectMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'


class CommonStatusMixin(
        LoginRequiredRedirectMixin):
    model = Status
    template_name = 'statuses/detail.html'
    url_name_success = 'statuses_index'


class StatusCreateView(
        CommonStatusMixin, SuccessMessageRedirectMixin, CreateView):
    form_class = StatusForm
    extra_context = {
        'h1_value': _('Status creation'),
        'button_value': _('Create'),
        }
    message_success = _("Status is created successfully")


class StatusUpdateView(
        CommonStatusMixin, SuccessMessageRedirectMixin, UpdateView):
    form_class = StatusForm
    extra_context = {
        'h1_value': _('Status update'),
        'button_value': _('Update'),
        }
    message_success = _("Status is updated successfully")


class StatusDeleteView(
        CommonStatusMixin, TaskUnusedRequaredDeletionMixin, DeleteView):

    template_name = 'statuses/delete.html'
    message_success = _("Status is deleted successfully")
    url_name_success, url_name_object_used = 'statuses_index', 'statuses_index'
