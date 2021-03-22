from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index), 
    path('save/', views.save), 
    path('<id>/update/', views.update), 
    path('<id>/destroy/', views.destroy)
]