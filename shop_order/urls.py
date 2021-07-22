from django.urls import path
from . import views

urlpatterns = [
    path('convert_shopping_cart_items_to_order/', views.convert_shopping_cart_items_to_order),
    path('confirmOrderShipmentDetail/<shop_order_id>/', views.confirmOrderShipmentDetail)
]