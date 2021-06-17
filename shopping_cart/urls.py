from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('add/', views.add),
    path('<user_id>/shopping_cart_item/', views.shopping_cart_item),
    path('<user_id>/count/', views.count),
    path('update/', views.update),
    path('<product_id>/product_shipment/', views.product_shipment),
    path('delete/', views.delete),
]