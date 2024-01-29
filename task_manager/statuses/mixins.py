from django.urls import reverse_lazy
from .models import Status
from task_manager.mixins import LoginRequiredRedirectMixin


class CommonStatusMixin(LoginRequiredRedirectMixin):
    model = Status
    template_name = 'statuses/detail.html'
    success_url = reverse_lazy('statuses_index')
