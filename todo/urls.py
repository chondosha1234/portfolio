from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('new', views.new_list, name='new_list'),
    path('<list_id>', views.view_list, name='view_list'),
    path('user/<email>', views.todo_list, name='user_list'),
    path('delete_task', views.delete_task, name='delete_task'),
    path('edit_task', views.edit_task, name='edit_task'),
    path('completed_tasks', views.completed_tasks, name='completed_tasks'),
]
