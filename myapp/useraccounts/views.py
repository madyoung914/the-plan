from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Profile
from .forms import CreateUserForm, ProfileEditForm


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


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'useraccounts/profile.html'

    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        ctx['profile_user'] = get_object_or_404(User, username=username)
        return ctx


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'useraccounts/profile_edit.html'

    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    def get_success_url(self):
        return reverse_lazy(
            'useraccounts:profile',
            kwargs={'username': self.object.user.username}
        )

