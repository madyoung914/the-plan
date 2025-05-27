from django.urls import path
from .views import HomePageView, UserCreateView

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('/register', UserCreateView.as_view(), name='register')
]

app_name = "useraccounts"