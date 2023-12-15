from django.urls import path
from task_manager.users import views

urlpatterns = [
    path(
        '',
        views.UsersIndexView.as_view(),
        name='users_index'),
    path(
        'create',
        views.UsersCreateFormView.as_view(),
        name='users_create'),
    path(
        '<int:pk>/update/',
        views.UsersUpdateFormView.as_view(),
        name='users_update'),
    path(
        '<int:pk>/delete/',
        views.UsersDeleteFormView.as_view(),
        name='users_delete'),
]
