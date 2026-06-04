from django.urls import path
from .import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    
    path('profile/<int:user_id>/', views.profile_detail, name='profile_detail'),
]