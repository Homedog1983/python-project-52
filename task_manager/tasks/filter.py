from django_filters import FilterSet, BooleanFilter
from django.forms import CheckboxInput
from .models import Task
from django.utils.translation import gettext_lazy as _


class CustomBooleanFilter(BooleanFilter):

    def filter(self, qs, value):
        # there is access to value, but not access to request.user,
        # therefore only able pass-filter with use request.GET["self_tasks"]
        # in @property qs later.
        return qs


class TaskFilterSet(FilterSet):

    self_tasks = CustomBooleanFilter(
        label=_("Self tasks only"),
        widget=CheckboxInput(attrs={'checked': False}))

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
        labels = {
            "status": _("Status"),
            "executor": _("Executor"),
            "labels": _("Labels")
        }

    @property
    def qs(self):
        parent = super().qs
        is_self_tasks = self.request.GET.get("self_tasks", False)
        if is_self_tasks:
            user = self.request.user
            return parent.filter(creator=user)
        return parent
