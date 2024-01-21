from .models import Label
from task_manager.mixins import LoginRequiredRedirectMixin


class CommonLabelMixin(
        LoginRequiredRedirectMixin):
    model = Label
    template_name = 'labels/detail.html'
    url_name_success = 'labels_index'

# from django.contrib.messages.views import SuccessMessageMixin
