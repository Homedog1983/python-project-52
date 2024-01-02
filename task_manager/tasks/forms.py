from django.forms import ModelForm, Textarea
from .models import Task


class TaskForm(ModelForm):

    class Meta:
        model = Task
        exclude = ["creator", "creation_date"]
        widgets = {
            "description": Textarea(attrs={"cols": 40, "rows": 10}),
        }
