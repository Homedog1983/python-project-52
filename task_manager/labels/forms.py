from django.forms import ModelForm
from .models import Label
from django.utils.translation import gettext_lazy as _


class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = [
            'name',
        ]
        labels = {
            "name": _("Name")
        }
