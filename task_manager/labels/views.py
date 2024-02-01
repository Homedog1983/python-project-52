from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from .models import Label
from .forms import LabelForm
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import (
    LoginRequiredRedirectMixin, ObjectUnusedRequaredMixin)


class LabelIndexView(LoginRequiredRedirectMixin, ListView):
    model = Label
    template_name = 'labels/index.html'


class LabelCreateView(
        LoginRequiredRedirectMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/form.html'
    extra_context = {
        'header': _('Label creation'),
        'button_text': _('Create')}
    success_message = _("Label is created successfully")
    success_url = reverse_lazy('labels_index')


class LabelUpdateView(
        LoginRequiredRedirectMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/form.html'
    extra_context = {
        'header': _('Label update'),
        'button_text': _('Update')}
    success_message = _("Label is updated successfully")
    success_url = reverse_lazy('labels_index')


class LabelDeleteView(
        LoginRequiredRedirectMixin, ObjectUnusedRequaredMixin,
        SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_message = _("Label is deleted successfully")
    url_name_object_used = 'labels_index'
    success_url = reverse_lazy('labels_index')
