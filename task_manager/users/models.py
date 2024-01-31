from django.contrib.auth.models import User


class CustomUser(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.get_full_name()

    def is_object_in_use(self):
        return self.task_creator_set.exists() | self.task_executor_set.exists()

    def get_creator(self):
        return self
