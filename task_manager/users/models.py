from django.contrib.auth.models import User


class CustomUser(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.get_full_name()

    def is_used_in_task(self):
        if self.task_creator_set.all():
            return True
        if self.task_executor_set.all():
            return True
        return False

    def get_creator_username(self):
        return self.username
