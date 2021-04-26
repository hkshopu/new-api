from django.urls import path
from . import views

urlpatterns = [
    path('save/', views.save), 
    path('index/', views.index),
    path('<id>/shop_product/', views.shop_product),    
]