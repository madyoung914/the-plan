from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.list import ListView
from django.http import HttpResponseForbidden
from django.db.models import Q

from .models import Task
from .forms import TodoForm
from useraccounts.models import Profile


class TodoListView(ListView):
    model = Task
    template_name = "planner/todo.html"
    
    def get_context_data(self, **kwargs):
        user = Profile.objects.get(user=self.request.user)
        self.object_list = self.get_queryset()
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = TodoForm()
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

        
        







