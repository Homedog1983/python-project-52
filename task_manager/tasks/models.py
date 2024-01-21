from django.db import models
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.mixins import UserFullNameMixin
from django.utils.translation import gettext_lazy as _


class Task(UserFullNameMixin, models.Model):
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
        User,
        on_delete=models.PROTECT,
        related_name='task_creator_set',
        verbose_name=_('Creator'))
    executor = models.ForeignKey(
        User,
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
    self_tasks = False

    def __str__(self):
        return self.name

    def full_names(self):
        return {
            "creator": self.creator.get_full_name(),
            "executor": self.executor.get_full_name() if self.executor else ''
        }
