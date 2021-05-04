from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create), 
    path('save/', views.save), 
    path('<id>/update/', views.update), 
    path('<id>/show/', views.show), 
    path('checkShopNameIsExistsProcess/', views.checkShopNameIsExistsProcess),
    path('<id>/shipmentSettings/', views.shipmentSettings),
    path('<id>/bankAccount/create/', views.createBankAccount),
    path('bankAccount/<id>/update/', views.updateBankAccount),
    path('bankAccount/<id>/delete/', views.delBankAccount),
    path('<id>/shipmentSettings/get', views.getShipmentSettings),
    path('<id>/shipmentSettings/set', views.setShipmnetSettings),
    path('test/', views.testAPI), 
    path('<id>/get_product_quantity_of_specific_shop/', views.get_product_quantity_of_specific_shop), 
    path('<id>/get_follower_quantity_of_specific_shop/', views.get_follower_quantity_of_specific_shop), 
    path('<id>/get_product_average_rating_of_specific_shop/', views.get_product_average_rating_of_specific_shop)
]