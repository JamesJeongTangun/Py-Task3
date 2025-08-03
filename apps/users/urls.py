from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('logout/quick/', views.quick_logout, name='quick_logout'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('profile/', views.profile_view, name='profile'),
]
