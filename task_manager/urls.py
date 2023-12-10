from django.contrib import admin
from django.urls import path
from task_manager import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='main_page'),
    path('admin/', admin.site.urls),
]
