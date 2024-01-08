from django.forms import ModelForm, Textarea
from .models import Task
from django.utils.translation import gettext_lazy as _


class TaskForm(ModelForm):

    class Meta:
        model = Task
        exclude = ["creator", "creation_date"]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "status": _("Status"),
            "executor": _("Executor"),
            "cretor": _("Creator")
        }
        widgets = {
            "description": Textarea(attrs={"cols": 40, "rows": 10}),
        }
