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
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    # path('admin/users/', views.all_users, name='all_users'),
    # path('manage/users/', views.all_users, name='all_users'),
]