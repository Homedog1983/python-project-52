from django.forms import ModelForm
from .models import Status
from django.utils.translation import gettext_lazy as _


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = [
            'name',
        ]
        labels = {
            "name": _("Name")
        }
