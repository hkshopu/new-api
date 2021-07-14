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
    path('<user_id>/buyer_address/', views.buyer_address),
    path('add_buyer_address/', views.add_buyer_address),
    path('checkout/', views.checkout),
    path('covert_shopping_cart/', views.covert_shopping_cart),
    path('delete_user_address/', views.delete_user_address),
]