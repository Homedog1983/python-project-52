from django.urls import path
from task_manager.tasks import views

urlpatterns = [
    path(
        '',
        views.FilterIndexView.as_view(),
        name='tasks_index'),
    path(
        'create/',
        views.TaskCreateView.as_view(),
        name='tasks_create'),
    path(
        '<int:pk>/update/',
        views.TaskUpdateView.as_view(),
        name='tasks_update'),
    path(
        '<int:pk>/delete/',
        views.TaskDeleteView.as_view(),
        name='tasks_delete'),
]
