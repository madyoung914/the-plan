from django.urls import path
from .views import TodoListView

urlpatterns = [
    path('to-do', TodoListView.as_view(), name="to-do")
]

app_name = "planner"