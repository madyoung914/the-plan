from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, Track, Workspace
from .forms import TodoForm, TrackForm
from useraccounts.models import Profile


class TodoListView(ListView):
    model = Task
    template_name = "planner/todo.html"
    
    def get_context_data(self, **kwargs):
        user = Profile.objects.get(user=self.request.user)
        self.object_list = self.get_queryset()
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = TodoForm
        all_todo = Task.objects.filter(owner=user, track=None, workspace=None)
        priority_todo = Task.objects.filter(owner=user, track=None, workspace=None, priority=True)
        nonpriority_todo = Task.objects.filter(owner=user, track=None, workspace=None, priority=False)
        ctx['todos'] = all_todo
        ctx['priority'] = priority_todo
        ctx['nonpriority'] = nonpriority_todo

        pending_tasks = Task.objects.filter(Q(owner=user, track__isnull=False) |  Q(workspace__isnull=False), Q(status='S') | Q(status='NS'), days_left__gte=0).order_by('-deadline')
        completed_tasks = Task.objects.filter(Q(owner=user, track__isnull=False) |  Q(workspace__isnull=False), status='D', days_left__gte=0)
        missed_tasks = Task.objects.filter(Q(owner=user, track__isnull=False) |  Q(workspace__isnull=False), Q(status='S') | Q(status='NS'), days_left__lt=0).order_by('-deadline')
        
        ctx['pending_tasks'] = pending_tasks
        ctx['completed_tasks'] = completed_tasks
        ctx['missed_tasks'] = missed_tasks
        
        return ctx

    def post(self,request, *args, **kwargs):
        if "delete_task_id" in request.POST:
            task_id = request.POST.get("delete_task_id")  
            obj = get_object_or_404(Task, pk=task_id)
            obj.delete()
            return redirect(reverse('planner:to-do')) 

        if "complete_task_id" in request.POST:
            task_id = request.POST.get("complete_task_id")  
            obj = get_object_or_404(Task, pk=task_id)
            if obj.status == 'D':
                obj.status = 'ND'
            else:
                obj.status = 'D'

            obj.save()
            return redirect(reverse('planner:to-do')) 

        if "edit_task_id" in request.POST:
            task_id = request.POST.get("edit_task_id")  
            obj = get_object_or_404(Task, pk=task_id)
            obj.name = request.POST.get('entry', obj.name)
            obj.save()
            return redirect(reverse('planner:to-do'))

        if "priority_task_id" in request.POST:
            task_id = request.POST.get("priority_task_id")  
            obj = get_object_or_404(Task, pk=task_id)
            if obj.priority == False:
                obj.priority = True
            else:
                obj.priority = False

            obj.save()
            return redirect(reverse('planner:to-do')) 

        form = TodoForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if request.user.is_authenticated:
                task.owner = request.user.profile 
            
            task.save()
            return redirect(reverse('planner:to-do'))
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


    def get_success_url(self):
        return redirect(reverse('planner:to-do'))



class TrackCreateView(LoginRequiredMixin, CreateView):
    model = Track
    form_class = TrackForm
    template_name = "planner/track_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Create new track'

        return ctx

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("planner:track-detail",
                            kwargs={"pk": self.object.pk})


class TrackUpdateView(LoginRequiredMixin, UpdateView):
    model = Track
    form_class = TrackForm
    emplate_name = "planner/track_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit my track'

        return ctx

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("planner:track-detail",
                            kwargs={"pk": self.object.pk})


class TrackListView(ListView):
    model = Track
    template_name = "planner/track_list.html"

    def get_context_data(self, **kwargs):
        user = Profile.objects.get(user=self.request.user)
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            ctx['current_tracks'] = Track.objects.filter(owner=user, archived=False)
            ctx['past_tracks'] = Track.objects.filter(owner=user, archived=True)

        return ctx


class TrackDetailView(DetailView):
    model = Track
    fields = '__all__'
    template_name = "planner/track_detail.html"


'''
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "planner/planner_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = TaskForm()
        ctx['title'] = 'Create new task'

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        

        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("planner:task",
                            kwargs={"pk": self.object.pk})

class WorkspaceCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "planner/planner_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = WorkspaceForm()
        ctx['title'] = 'Create new workspace'

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        

        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("planner:workspace",
                            kwargs={"pk": self.object.pk})

'''






