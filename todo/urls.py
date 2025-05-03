from django.urls import path

from . import views
app_name = 'todo' 

urlpatterns = [
    path('', views.home, name='home'),

    path('<int:todo_id>/todo_delete', views.todo_delete, name='todo_delete'),

    path('<int:todo_id>/todo_update', views.todo_update, name='todo_update'),
    
    path('todo_create/', views.todo_create, name='todo_create'),
    path('<int:todo_id>/todo_edit/', views.todo_edit, name = 'todo_edit'),
    path('<int:todo_id>/todo_edit_save/', views.todo_edit_save, name='todo_edit_save')
]

