from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/command/', views.handle_command, name='command'),
]
