from django.urls import path
from . import views

urlpatterns = [
    path('get_all_audit_logs_page/', views.get_all_audit_logs_page),
    path('get_all_audit_logs/', views.get_all_audit_logs), 
    path('get_all_shop_clicked_page/', views.get_all_shop_clicked_page), 
    path('get_all_shop_clicked/', views.get_all_shop_clicked), 
    path('get_all_product_clicked_page/', views.get_all_product_clicked_page), 
    path('get_all_product_clicked/', views.get_all_product_clicked), 
    path('get_all_shop_browsed_page/', views.get_all_shop_browsed_page), 
    path('get_all_shop_browsed/', views.get_all_shop_browsed), 
    path('get_all_product_browsed_page/', views.get_all_product_browsed_page), 
    path('get_all_product_browsed/', views.get_all_product_browsed)
]