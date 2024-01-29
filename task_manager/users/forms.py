from django.utils.translation import gettext as _
from django import forms
from task_manager.users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=_("Input more then 3 symbols, please."),
    )

    class Meta(UserCreationForm.Meta):
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

    def clean_username(self):
        """Reject usernames that differ only in case
        and allow to use same username"""

        if 'username' in self.changed_data:
            return super().clean_username()
        return self.cleaned_data.get("username")
