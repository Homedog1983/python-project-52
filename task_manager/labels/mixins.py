from django.urls import reverse_lazy
from .models import Label
from task_manager.mixins import LoginRequiredMixin


class CommonLabelMixin(LoginRequiredMixin):
    model = Label
    template_name = 'labels/detail.html'
    success_url = reverse_lazy('labels_index')
