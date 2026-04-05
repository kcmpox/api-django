from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.get_users, name='get_users'),
    path('user/<str:nick>', views.get_by_nick, name='get_by_nick'),
    path('data/', views.user_manager, name='user_manager'),
]
