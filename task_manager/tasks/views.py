from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django_filters.views import FilterView
from .models import Task
from .forms import TaskForm
from .filter import TaskFilterSet
from django.contrib.messages.views import SuccessMessageMixin
from .mixins import CommonTaskMixin, AutoAddCreatorMixin
from task_manager.mixins import LoginRequiredRedirectMixin


class FilterIndexView(LoginRequiredRedirectMixin, FilterView):
    filterset_class = TaskFilterSet
    template_name = 'tasks/index_filter.html'


class TaskCreateView(
        CommonTaskMixin, AutoAddCreatorMixin,
        SuccessMessageMixin, CreateView):
    form_class = TaskForm
    extra_context = {
        'header': _('Task creation'),
        'button_value': _('Create')}
    success_message = _("Task is created successfully!")


class TaskUpdateView(
        CommonTaskMixin, AutoAddCreatorMixin,
        SuccessMessageMixin, UpdateView):
    form_class = TaskForm
    extra_context = {
        'header': _('Task update'),
        'button_value': _('Update')}
    success_message = _("Task is updated successfully")


class TaskDeleteView(SuccessMessageMixin, DeleteView):

    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy("tasks_index")
    success_message = _("Task is deleted successfully")
    message_not_authenticated = _(
        'You are not login. Please, login!')
    message_not_creator = _(
        'Task is possible to delete for its creator only!')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(request, self.message_not_authenticated)
            return redirect(reverse('login'))
        task = get_object_or_404(Task, id=kwargs['pk'])
        if user != task.creator:
            messages.warning(request, self.message_not_creator)
            return redirect(reverse("tasks_index"))
        return super().dispatch(request, *args, **kwargs)
