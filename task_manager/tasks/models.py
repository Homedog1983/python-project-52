from django.db import models
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        unique=True,
        max_length=150)
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status'))
    creator = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='task_creator_set',
        verbose_name=_('Creator'))
    executor = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='task_executor_set',
        null=True,
        blank=True,
        verbose_name=_('Executor'))
    labels = models.ManyToManyField(
        Label,
        blank=True,
        verbose_name=_('Labels'))
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_creator_username(self):
        return self.creator.username
