from django.contrib import admin
from django.urls import path, include
from task_manager import views

urlpatterns = [
    path(
        '',
        views.IndexView.as_view(),
        name='main_page'),
    path('users/', include('task_manager.users.urls')),
    path(
        'login/',
        views.IndexView.as_view(),
        name='login/'),
    path(
        'logout/',
        views.IndexView.as_view(),
        name='logout/'),

    path(
        'admin/',
        admin.site.urls),
]
