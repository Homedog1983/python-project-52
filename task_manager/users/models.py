from django.contrib.auth.models import User


class CustomUser(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.get_full_name()

    def is_object_in_use(self):
        if self.task_creator_set.exists() or self.task_executor_set.exists():
            return True
        return False

    def get_creator_username(self):
        return self.username
