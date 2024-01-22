from django.urls import reverse_lazy
from .models import Task
from task_manager.mixins import LoginRequiredRedirectMixin


class CommonTaskMixin(LoginRequiredRedirectMixin):
    model = Task
    template_name = 'tasks/detail.html'
    success_url = reverse_lazy('tasks_index')


class AutoAddCreatorMixin:
    """
    Add authenticated user as task.creator
    for creation, not change for updating.
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
        return super().form_valid(form)
