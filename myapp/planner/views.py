from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.list import ListView

from .models import Task
from .forms import TodoForm


class TodoListView(ListView):
    model = Task
    template_name = "planner/todo.html"
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = TodoForm()
        all_todo = Task.objects.filter(track=None, workspace=None)
        priority_todo = Task.objects.filter(track=None, workspace=None, priority=True)
        nonpriority_todo = Task.objects.filter(track=None, workspace=None, priority=False)
        ctx['todos'] = all_todo
        ctx['priority'] = priority_todo
        ctx['nonpriority'] = nonpriority_todo
        return ctx

    def post(self,request, *args, **kwargs):
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




