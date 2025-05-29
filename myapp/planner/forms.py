from django import forms
from .models import Task, Track, Workspace


class TodoForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'priority']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['owner', 'days_left', 'track', 'workspace', ]


class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = '__all__'
        exclude = ['owner', ]


class WorkspaceForm(forms.ModelForm):
    class Meta:
        model = Workspace
        fields = '__all__'
        exclude = ['owner', 'track', ]