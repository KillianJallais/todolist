from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createTask/", views.createTask, name="createTask"),
    path("addTask/", views.addTask, name="addTask"),
    path("<int:taskId>/", views.showTask, name="showTask"),
    path("<int:taskId>/delTask/", views.delTask, name="delTask"),
    path("<int:taskId>/editTask/", views.editTask, name="editTask"),
    path("<int:taskId>/updateTask/", views.updateTask, name="updateTask"),
    path("<int:taskId>/completeTask/", views.completeTask, name="completeTask"),
    path("completedTask/", views.completedTask, name="completedTask"),
    path("obsoleteTask/", views.obsoleteTask, name="obsoleteTask"),
]