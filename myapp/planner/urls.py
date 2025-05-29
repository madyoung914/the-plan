from django.urls import path
from .views import TodoListView
from . import views

urlpatterns = [
    path('to-do', TodoListView.as_view(), name="to-do"),
    
]

app_name = "planner"