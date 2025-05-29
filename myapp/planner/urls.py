from django.urls import path
from .views import TodoListView, TaskCreateView, TrackCreateView, WorkspaceCreateView
from . import views

urlpatterns = [
    path('to-do', TodoListView.as_view(), name="to-do"),
    path('task/<int:pk>', TaskCreateView.as_view(), name="task"),
    path('track/<int:pk>', TrackCreateView.as_view(), name="track"),
    path('workspace/<int:pk>', WorkspaceCreateView.as_view(), name="workspace"),
]

app_name = "planner"