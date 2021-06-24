from django.urls import path
from . import views

urlpatterns = [
    path('update_detail/', views.update_detail),   
    path('<user_id>/user_rate/', views.user_rate), 
    path('user_liked/', views.user_liked),  
    path('<user_id>/liked_count/', views.liked_count), 
    path('user_followed/', views.user_followed),  
]