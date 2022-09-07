from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/edit/', views.edit, name='profile-edit'),
    path('user/<str:action>/<int:pk>/', views.toggle_follow, name='toggle_follow'),
    path('profile/password/change', views.change_password, name='change-password'),
    path('<str:username>/', views.profile, name='profile')
]