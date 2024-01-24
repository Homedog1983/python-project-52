from django.utils.translation import gettext as _
from django import forms
# from django.contrib.auth.models import User
from task_manager.users.models import CustomUser
from django.contrib.auth.forms import BaseUserCreationForm


class CustomUserCreationForm(BaseUserCreationForm):

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=_("Input more then 3 symbols, please."),
    )

    class Meta(BaseUserCreationForm.Meta):
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
