from django.urls import path
from .views import HomePageView, UserCreateView, ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('register', UserCreateView.as_view(), name='register'),
    path('profile/<str:username>', ProfileDetailView.as_view(),
         name='profile'),
    path('profile/<str:username>/edit', ProfileUpdateView.as_view(),
         name='profile-edit'),
]

app_name = "useraccounts"