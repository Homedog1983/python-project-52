from django.contrib.auth.models import User
from django.contrib.auth.forms import BaseUserCreationForm


class CustomUserCreationForm(BaseUserCreationForm):

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2']
