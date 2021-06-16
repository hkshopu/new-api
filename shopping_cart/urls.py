from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('add/', views.add),
    path('<user_id>/shopping_cart_item/', views.shopping_cart_item)
    
]