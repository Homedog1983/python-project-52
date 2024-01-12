from django_filters import FilterSet, BooleanFilter, ModelChoiceFilter
from django.forms import CheckboxInput
from django_filters.fields import ModelChoiceField
from task_manager.mixins import UserFullNameMixin
from .models import Task
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _


class CustomBooleanFilter(BooleanFilter):

    def filter(self, qs, value):
        # there is access to value, but not access to request.user,
        # therefore only able pass-filter with later use
        # request.GET["self_tasks"] in @property qs
        return qs


class UserFullNameModelChoiceField(UserFullNameMixin, ModelChoiceField):
    pass


class UserFullNameModelChoiceFilter(ModelChoiceFilter):
    field_class = UserFullNameModelChoiceField


class TaskFilterSet(FilterSet):
    status = ModelChoiceFilter(
        field_name='status',
        label=_('Status'),
        queryset=Status.objects.all())

    executor = UserFullNameModelChoiceFilter(
        field_name='executor',
        label=_('Executor'),
        queryset=User.objects.all())

    label = ModelChoiceFilter(
        field_name='labels',
        label=_('Label'),
        queryset=Label.objects.all())

    self_tasks = CustomBooleanFilter(
        label=_("Self tasks only"),
        widget=CheckboxInput(attrs={'checked': False}))

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']

    @property
    def qs(self):
        parent = super().qs
        is_self_tasks = self.request.GET.get("self_tasks", False)
        if is_self_tasks:
            user = self.request.user
            return parent.filter(creator=user)
        return parent
