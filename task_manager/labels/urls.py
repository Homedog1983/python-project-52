from django.urls import path
# from task_manager. import views
from task_manager import views

urlpatterns = [
    path(
        '',
        views.IndexView.as_view(),
        name='labels_index'),
    path(
        'create',
        views.IndexView.as_view(),
        name='labels_create'),
    path(
        '<int:pk>/update/',
        views.IndexView.as_view(),
        name='labels_update'),
    path(
        '<int:pk>/delete/',
        views.IndexView.as_view(),
        name='labels_delete'),
]
