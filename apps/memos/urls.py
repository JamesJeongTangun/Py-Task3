from django.urls import path
from . import views

app_name = 'memos'

urlpatterns = [
    path('', views.memo_list, name='list'),
    path('create/', views.memo_create, name='create'),
    path('<int:pk>/', views.memo_detail, name='detail'),
    path('<int:pk>/edit/', views.memo_edit, name='edit'),
    path('<int:pk>/delete/', views.memo_delete, name='delete'),
]
