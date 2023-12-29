from django.db import models
from django.contrib.auth.models import User
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(unique=True, max_length=150)
    description = models.TextField(blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT)
    creator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='creator')
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor',
        null=True,
        blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return {
            "creator": self.creator.get_full_name(),
            "executor": self.executor.get_full_name() if self.executor else ''
        }
