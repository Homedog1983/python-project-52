from django.contrib.auth.models import User


User.add_to_class("__str__", User.get_full_name)

# Alternative (need to register new class user in settings.py etc)
#
# class CustomUser(User):
#     class Meta:
#         db_table = 'auth_user'
#
# def __str__(self):
#     return self.get_full_name
