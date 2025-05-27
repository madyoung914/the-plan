from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .models import Profile
from .forms import CreateUserForm


class HomePageView(TemplateView):
    template_name = "useraccounts/homepage.html"


class UserCreateView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = "useraccounts/register.html"

    def form_valid(self, form):
        new_user = form.save()
        display_name = form.cleaned_data['display_name']
        Profile.objects.create(
            user=new_user, name=display_name)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("login")
