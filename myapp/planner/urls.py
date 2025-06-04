from django.urls import path
from .views import TodoListView, TrackCreateView, TrackUpdateView, TrackListView, TrackDetailView, TaskUpdateView
from . import views

urlpatterns = [
    path('to-do', TodoListView.as_view(), name="to-do"),
    #path('streams', )
    #path('task/<int:pk>', TaskCreateView.as_view(), name="task"), #this might be wrong url
    path('tracks', TrackListView.as_view(), name="track-list"),
    path('track/<int:pk>', TrackDetailView.as_view(), name="track-detail"),
    path('track/add', TrackCreateView.as_view(), name="track-create"),
    path('track/<int:pk>/edit', TrackUpdateView.as_view(), name="track-update"),
    path('tracks/<int:pk>/task/edit', TaskUpdateView.as_view(), name="task-update"),
    #path('workspace/<int:pk>', WorkspaceCreateView.as_view(), name="workspace"),

    #so list, detail create and updateview for both track and workspace first
    #worry ab tasks nad workspace in track later
]

app_name = "planner"