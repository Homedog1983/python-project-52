from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from .models import Status
from .forms import StatusForm
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import (
    LoginRequiredRedirectMixin, ObjectUnusedRequaredMixin)


class StatusIndexView(LoginRequiredRedirectMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'


class StatusCreateView(
        LoginRequiredRedirectMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    extra_context = {
        'header': _('Status creation'),
        'button_text': _('Create')}
    success_message = _("Status is created successfully")
    template_name = 'statuses/detail.html'
    success_url = reverse_lazy('statuses_index')


class StatusUpdateView(
        LoginRequiredRedirectMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    extra_context = {
        'header': _('Status update'),
        'button_text': _('Update')}
    success_message = _("Status is updated successfully")
    template_name = 'statuses/detail.html'
    success_url = reverse_lazy('statuses_index')


class StatusDeleteView(
        LoginRequiredRedirectMixin, ObjectUnusedRequaredMixin,
        SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_message = _("Status is deleted successfully")
    url_name_object_used = 'statuses_index'
    success_url = reverse_lazy('statuses_index')
