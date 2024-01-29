from django.urls import reverse_lazy
from .models import Label
from task_manager.mixins import LoginRequiredRedirectMixin


class CommonLabelMixin(LoginRequiredRedirectMixin):
    model = Label
    template_name = 'labels/detail.html'
    success_url = reverse_lazy('labels_index')
