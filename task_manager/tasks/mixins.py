from .models import Task
from task_manager.mixins import (
    LoginRequiredRedirectMixin,
    SuccessMessageRedirectMixin)


class CommonTaskMixin(
        LoginRequiredRedirectMixin,
        SuccessMessageRedirectMixin):
    model = Task
    template_name = 'tasks/detail.html'
    url_name_success = 'tasks_index'
