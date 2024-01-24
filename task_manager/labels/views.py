from django.utils.translation import gettext as _
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from .models import Label
from .forms import LabelForm
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import (
    LoginRequiredMixin, ObjectUnusedRequaredMixin)
from .mixins import CommonLabelMixin


class LabelIndexView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'


class LabelCreateView(
        CommonLabelMixin, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    extra_context = {
        'header': _('Label creation'),
        'button_text': _('Create')}
    success_message = _("Label is created successfully")


class LabelUpdateView(
        CommonLabelMixin, SuccessMessageMixin, UpdateView):
    form_class = LabelForm
    extra_context = {
        'header': _('Label update'),
        'button_text': _('Update')}
    success_message = _("Label is updated successfully")


class LabelDeleteView(
        CommonLabelMixin, ObjectUnusedRequaredMixin,
        SuccessMessageMixin, DeleteView):

    template_name = 'labels/delete.html'
    success_message = _("Label is deleted successfully")
    url_name_object_used = 'labels_index'
