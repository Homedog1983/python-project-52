from django.utils.translation import gettext as _
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from .models import Label
from .forms import LabelForm
from task_manager.mixins import (
        LoginRequiredRedirectMixin,
        SuccessMessageRedirectMixin,
        TaskUnusedRequaredDeletionMixin)


class LabelIndexView(LoginRequiredRedirectMixin, ListView):
    model = Label
    template_name = 'labels/index.html'


class CommonLabelMixin(
        LoginRequiredRedirectMixin):
    model = Label
    template_name = 'labels/detail.html'
    url_name_success = 'labels_index'


class LabelCreateView(
        CommonLabelMixin, SuccessMessageRedirectMixin, CreateView):
    form_class = LabelForm
    extra_context = {
        'h1_value': _('Label creation'),
        'button_value': _('Create'),
        }
    message_success = _("Label is created successfully!")


class LabelUpdateView(
        CommonLabelMixin, SuccessMessageRedirectMixin, UpdateView):
    form_class = LabelForm
    extra_context = {
        'h1_value': _('Label update'),
        'button_value': _('Update'),
        }
    message_success = _("Label is updated successfully!")


class LabelDeleteView(
        CommonLabelMixin, TaskUnusedRequaredDeletionMixin, DeleteView):

    template_name = 'labels/delete.html'
    message_success = _("Label is deleted successfully!")
    url_name_success, url_name_object_used = 'labels_index', 'labels_index'
