from django.forms import ModelForm, Textarea
from .models import Task
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.forms import ModelChoiceField
from task_manager.mixins import UserFullNameMixin


class UserFullNameModelChoiceField(UserFullNameMixin, ModelChoiceField):
    pass


class TaskForm(ModelForm):
    executor = UserFullNameModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Task
        exclude = ["creator", "creation_date"]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "status": _("Status"),
            "executor": _("Executor"),
            "labels": _("Labels"),
            "cretor": _("Creator")
        }
        widgets = {
            "description": Textarea(attrs={"cols": 40, "rows": 10}),
        }
