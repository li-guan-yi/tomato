from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('todos/', views.todo_list, name='todo_list'),
    path('todos/create/', views.todo_create, name='todo_create'),
    path('todos/<int:pk>/update/', views.todo_update, name='todo_update'),
    path('todos/<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('todos/<int:pk>/toggle/', views.todo_toggle, name='todo_toggle'),
    path('pomodoro/settings/', views.pomodoro_settings, name='pomodoro_settings'),
    path('pomodoro/start/', views.pomodoro_start, name='pomodoro_start'),
    path('pomodoro/complete/', views.pomodoro_complete, name='pomodoro_complete'),
    path('pomodoro/history/', views.pomodoro_history, name='pomodoro_history'),
]
