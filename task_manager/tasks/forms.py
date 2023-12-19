from django.forms import ModelForm, Textarea
from .models import Task


class TaskForm(ModelForm):

    class Meta:
        model = Task
        exclude = ["creator", "creation_date"]
        widgets = {
            "description": Textarea(attrs={"cols": 40, "rows": 10}),
        }

    def save_with_creator(self, authenticated_user):
        task = self.save(commit=False)
        try:
            task.creator
        except Task.creator.RelatedObjectDoesNotExist:
            task.creator = authenticated_user
        finally:
            task.save()
