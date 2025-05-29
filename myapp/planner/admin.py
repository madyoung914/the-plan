from django.contrib import admin
from .models import Task, Track, Workspace

class TaskAdmin(admin.ModelAdmin):
    model = Task


class TaskInline(admin.StackedInline):
    model = Task
    can_delete = True


class TrackAdmin(admin.ModelAdmin):
    model = Track
    inlines = [TaskInline, ]


class WorkspaceAdmin(admin.ModelAdmin):
    model = Workspace
    inlines = [TaskInline, ]


admin.site.register(Task, TaskAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Workspace, WorkspaceAdmin)



