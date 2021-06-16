from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('add_shopping_cart/', views.add_shopping_cart),
    path('<user_id>/shopping_cart_item/', views.shopping_cart_item)
    
]