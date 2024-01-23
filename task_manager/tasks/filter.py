from django_filters import FilterSet, BooleanFilter, ModelChoiceFilter
from django.forms import CheckboxInput
from .models import Task
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _


class TaskFilterSet(FilterSet):

    label = ModelChoiceFilter(
        field_name='labels',
        label=_('Label'),
        queryset=Label.objects.all())

    def self_tasks_filter(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(creator=user)
        return queryset

    self_tasks = BooleanFilter(
        field_name="creator",
        method='self_tasks_filter',
        label=_("Self tasks only"),
        widget=CheckboxInput(attrs={'checked': False}))

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']
