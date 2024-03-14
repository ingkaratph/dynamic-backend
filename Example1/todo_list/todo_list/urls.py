from django.urls import path
from .views import TaskListCreate, TaskRetrieveUpdateDestroy, ToDoItemDetail

urlpatterns = [
    path('tasks/', TaskListCreate.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroy.as_view(), name='task-retrieve-update-destroy'),
    path('todo/<int:pk>/', ToDoItemDetail.as_view()),
]