from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from task_manager.tasks.models import Task
from django_filters.views import FilterView
from .forms import TaskForm
from .filter import TaskFilterSet
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import (
    LoginRequiredRedirectMixin, CreatorRequaredMixin)


class FilterIndexView(LoginRequiredRedirectMixin, FilterView):
    filterset_class = TaskFilterSet
    template_name = 'tasks/index_filter.html'


class TaskCreateView(
        LoginRequiredRedirectMixin,
        SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    extra_context = {
        'header': _('Task creation'),
        'button_text': _('Create')}
    success_message = _("Task is created successfully!")
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks_index')

    def form_valid(self, form):
        if self.request.method == 'POST':
            task = form.save(commit=False)
            task.creator = self.request.user
        return super().form_valid(form)


class TaskUpdateView(
        LoginRequiredRedirectMixin,
        SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    extra_context = {
        'header': _('Task update'),
        'button_text': _('Update')}
    success_message = _("Task is updated successfully")
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks_index')


class TaskDeleteView(
        LoginRequiredRedirectMixin, CreatorRequaredMixin,
        SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_message = _("Task is deleted successfully")
    url_name_not_creator = "tasks_index"
    message_not_creator = _(
        "Task is possible to delete for its creator only!")
    success_url = reverse_lazy('tasks_index')
