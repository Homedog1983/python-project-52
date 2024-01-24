from django.utils.translation import gettext as _
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django_filters.views import FilterView
from .forms import TaskForm
from .filter import TaskFilterSet
from django.contrib.messages.views import SuccessMessageMixin
from .mixins import CommonTaskMixin, AutoAddCreatorMixin
from task_manager.mixins import (
    LoginRequiredMixin, CreatorRequaredMixin)


class FilterIndexView(LoginRequiredMixin, FilterView):
    filterset_class = TaskFilterSet
    template_name = 'tasks/index_filter.html'


class TaskCreateView(
        CommonTaskMixin, AutoAddCreatorMixin,
        SuccessMessageMixin, CreateView):
    form_class = TaskForm
    extra_context = {
        'header': _('Task creation'),
        'button_text': _('Create')}
    success_message = _("Task is created successfully!")


class TaskUpdateView(
        CommonTaskMixin, AutoAddCreatorMixin,
        SuccessMessageMixin, UpdateView):
    form_class = TaskForm
    extra_context = {
        'header': _('Task update'),
        'button_text': _('Update')}
    success_message = _("Task is updated successfully")


class TaskDeleteView(
        CommonTaskMixin, CreatorRequaredMixin,
        SuccessMessageMixin, DeleteView):
    template_name = 'tasks/delete.html'
    success_message = _("Task is deleted successfully")
    url_name_not_creator = "tasks_index"
    message_not_creator = _(
        "Task is possible to delete for its creator only!")
