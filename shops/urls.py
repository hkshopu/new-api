from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create), 
    path('createProcess/', views.createProcess), 
]