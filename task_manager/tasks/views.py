from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.contrib import messages
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from .models import Task
from .forms import TaskForm
from task_manager.mixins import (
    LoginRequiredRedirectMixin, SuccessMessageRedirectMixin)


class TaskIndexView(LoginRequiredRedirectMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'


class CommonTaskMixin(
        LoginRequiredRedirectMixin,
        SuccessMessageRedirectMixin
        ):
    model = Task
    template_name = 'tasks/detail.html'
    url_name_success = 'tasks_index'


class AutoAddCreatorMixin:
    """
    Add authenticated user as self.form.creator.
    Used save_with_creator custom form method.
     ! Use after is_authenticated check !
    """
    def form_valid(self, form):
        if self.request.method == 'POST':
            form.save_with_creator(self.request.user)
            return redirect(self.get_success_url())
        else:
            super().form_valid(form)


class TaskCreateView(CommonTaskMixin, AutoAddCreatorMixin, CreateView):
    form_class = TaskForm
    extra_context = {
        'h1_value': _('Task creation'),
        'button_value': _('Create'),
        }
    message_success = _("Task is created successfully!")


class TaskUpdateView(CommonTaskMixin, AutoAddCreatorMixin, UpdateView):
    form_class = TaskForm
    extra_context = {
        'h1_value': _('Task update'),
        'button_value': _('Update'),
        }
    message_success = _("Task is updated successfully!")


class TaskDeleteView(CommonTaskMixin, DeleteView):

    template_name = 'tasks/delete.html'
    message_success = _("Task is deleted successfully!")
    message_not_creator = _(
        'Task is possible to delete for its creator only!')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        task = get_object_or_404(Task, id=kwargs['pk'])
        if user != task.creator:
            messages.warning(request, self.message_not_creator)
            return redirect("tasks_index")
        return super().dispatch(request, *args, **kwargs)

