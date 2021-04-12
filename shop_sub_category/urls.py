from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index), 
    path('create/',views.create),
    path('save/', views.save), 
]