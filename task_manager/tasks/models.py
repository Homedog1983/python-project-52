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



# class TimestampedModel(models.Model):
#     """An abstract model with a pair of timestamps."""

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True


# class User(TimestampedModel):
#     """A blog user."""

#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=100, null=True)
#     last_name = models.CharField(max_length=100, null=True)


# class Tag(TimestampedModel):
#     """A tag for the group of posts."""

#     title = models.CharField(max_length=100)


# class Post(TimestampedModel):
#     """A blog post."""

#     title = models.CharField(max_length=200)
#     body = models.TextField()
#     creator = models.ForeignKey(User, on_delete=models.CASCADE)
#     tags = models.ManyToManyField(Tag)


# class PostComment(TimestampedModel):
#     """A commentary to the blog post."""

#     body = models.TextField()
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     response_to = models.ForeignKey(
#         'PostComment', on_delete=models.SET_NULL, null=True,
#     )
#     creator = models.ForeignKey(User, on_delete=models.CASCADE)


# class PostLike(TimestampedModel):
#     """A positive reaction to the blog post."""

#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     creator = models.ForeignKey(User, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ['post', 'creator']