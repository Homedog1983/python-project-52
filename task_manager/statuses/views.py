from django.utils.translation import gettext as _
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from .models import Status
from .forms import StatusForm
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import (
    LoginRequiredRedirectMixin,
    ObjectUnusedRequaredMixin)
from .mixins import CommonStatusMixin


class StatusIndexView(LoginRequiredRedirectMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'


class StatusCreateView(
        CommonStatusMixin, SuccessMessageMixin, CreateView):
    form_class = StatusForm
    extra_context = {
        'header': _('Status creation'),
        'button_value': _('Create')}
    success_message = _("Status is created successfully")


class StatusUpdateView(
        CommonStatusMixin, SuccessMessageMixin, UpdateView):
    form_class = StatusForm
    extra_context = {
        'header': _('Status update'),
        'button_value': _('Update')}
    success_message = _("Status is updated successfully")


class StatusDeleteView(
        CommonStatusMixin, ObjectUnusedRequaredMixin,
        SuccessMessageMixin, DeleteView):

    template_name = 'statuses/delete.html'
    success_message = _("Status is deleted successfully")
    url_name_object_used = 'statuses_index'
