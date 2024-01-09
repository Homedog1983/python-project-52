from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.contrib import messages
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django_filters.views import FilterView
from .models import Task
from .forms import TaskForm
from .filter import TaskFilterSet
from task_manager.mixins import (
    LoginRequiredRedirectMixin, SuccessMessageRedirectMixin)


class FilterIndexView(LoginRequiredRedirectMixin, FilterView):
    filterset_class = TaskFilterSet
    template_name = 'tasks/index_filter.html'


class CommonTaskMixin(
        LoginRequiredRedirectMixin,
        SuccessMessageRedirectMixin
        ):
    model = Task
    template_name = 'tasks/detail.html'
    url_name_success = 'tasks_index'


class AutoAddCreatorMixin:
    """
    Add authenticated user as task.creator
    in creation, not change in updating.
    After creator's saving it is proceed parent method
    (allow save many2many relations by generic editing views)
    ! Use after is_authenticated = True check !
    """
    def form_valid(self, form):
        if self.request.method == 'POST':
            task = form.save(commit=False)
            try:
                task.creator
            except Task.creator.RelatedObjectDoesNotExist:
                task.creator = self.request.user
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


class TaskDeleteView(SuccessMessageRedirectMixin, DeleteView):

    model = Task
    template_name = 'tasks/delete.html'
    url_name_success = "tasks_index"
    message_success = _("Task is deleted successfully!")
    message_not_authenticated = _(
        'You are not login. Please, login!')
    message_not_creator = _(
        'Task is possible to delete for its creator only!')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(request, self.message_not_authenticated)
            return redirect('login')
        task = get_object_or_404(Task, id=kwargs['pk'])
        if user != task.creator:
            messages.warning(request, self.message_not_creator)
            return redirect("tasks_index")
        return super().dispatch(request, *args, **kwargs)
