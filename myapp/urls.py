from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name = 'signup'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('logout/', LoginView.as_view(), name = 'logout'),
    path('login/', LoginView.as_view(), name = 'login'),
]