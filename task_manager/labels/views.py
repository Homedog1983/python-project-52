from django.utils.translation import gettext as _
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from .models import Label
from .forms import LabelForm
from task_manager.mixins import (
    LoginRequiredRedirectMixin, SuccessMessageRedirectMixin)


class LabelIndexView(LoginRequiredRedirectMixin, ListView):
    model = Label
    template_name = 'labels/index.html'


class CommonLabelMixin(
        LoginRequiredRedirectMixin,
        SuccessMessageRedirectMixin):
    model = Label
    template_name = 'labels/detail.html'
    success_url_name = 'labels_index'


class LabelCreateView(CommonLabelMixin, CreateView):
    form_class = LabelForm
    extra_context = {
        'h1_value': _('Label creation'),
        'button_value': _('Create'),
        }
    success_message = _("Label is created successfully!")


class LabelUpdateView(CommonLabelMixin, UpdateView):
    form_class = LabelForm
    extra_context = {
        'h1_value': _('Label update'),
        'button_value': _('Update'),
        }
    success_message = _("Label is updated successfully!")


class LabelDeleteView(CommonLabelMixin, DeleteView):

    # В диспатч ввести проверку в обратную сторону if not task_set
    # редирект с warning сообщением. Возможно сделать общий миксин
    # для статусов и лэйблов.

    template_name = 'labels/delete.html'
    success_message = _("Label is deleted successfully!")