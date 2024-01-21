from .models import Status
from task_manager.mixins import LoginRequiredRedirectMixin


class CommonStatusMixin(
        LoginRequiredRedirectMixin):
    model = Status
    template_name = 'statuses/detail.html'
    url_name_success = 'statuses_index'
