from django.urls import path
from .views import TodoListView, TrackCreateView, TrackUpdateView, TrackListView, TrackDetailView, TaskUpdateView, WorkspaceCreateView, WorkspaceUpdateView, WorkspaceListView, WorkspaceDetailView
from . import views

urlpatterns = [
    path('to-do', TodoListView.as_view(), name="to-do"),

    path('tracks', TrackListView.as_view(), name="track-list"),
    path('track/<int:pk>', TrackDetailView.as_view(), name="track-detail"),
    path('track/add', TrackCreateView.as_view(), name="track-create"),
    path('track/<int:pk>/edit', TrackUpdateView.as_view(), name="track-update"),
    path('track/<int:pk>/task/edit', TaskUpdateView.as_view(), name="track-task-update"),
    
    path('workspaces', WorkspaceListView.as_view(), name="workspace-list"),
    path('workspace/<int:pk>', WorkspaceDetailView.as_view(), name="workspace-detail"),
    path('workspace/add', WorkspaceCreateView.as_view(), name="workspace-create"),
    path('workspace/<int:pk>/edit', WorkspaceUpdateView.as_view(), name="workspace-update"),
    path('workspace/<int:pk>/task/edit', TaskUpdateView.as_view(), name="workspace-task-update"),
    
]

app_name = "planner"