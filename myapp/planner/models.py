from django.db import models
from useraccounts.models import Profile
from django.urls import reverse

class Track(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False, related_name='tracks')
    archived = models.BooleanField(default=False)

    #class related stuff 
    professor = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    syllabus = models.URLField(blank=True, null=True)
    course_code = models.CharField(max_length=255, blank=True, null=True)
    subject_name = models.CharField(max_length=255, blank=True, null=True)
    class_time_location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('planner:track-detail', args=[self.pk])


class Workspace(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False, related_name='workspaces')
    track = models.ForeignKey(Track, blank=True, null=True, on_delete=models.SET_NULL, related_name='workspace_track')
    members = models.ManyToManyField(Profile, related_name='members')
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('planner:workspace-detail', args=[self.pk])

class Task(models.Model):

    TASK_STATUS = (
        ('Done', 'Done'),
        ('Ongoing', 'Ongoing'),
        ('Not Started', 'Not Started'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, related_name='task')
    track = models.ForeignKey(Track, blank=True, null=True, on_delete=models.SET_NULL, related_name='task_track')
    workspace = models.ForeignKey(Workspace, blank=True, null=True, on_delete=models.SET_NULL, related_name='task_workspace')

    deadline = models.DateField(blank=True, null=True)
    days_left = models.IntegerField(blank=True, null=True)
    priority = models.BooleanField(default=False)
    status = models.CharField(max_length=15, choices=TASK_STATUS, default="Not Started")
    grade = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    #links?? shld this be its own model

    def __str__(self):
        return self.name

    class Meta:
        ordering =['deadline']

class Event(models.Model): 
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name



