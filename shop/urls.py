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
    path('<id>/get_product_average_rating_of_specific_shop/', views.get_product_average_rating_of_specific_shop), 
    path('<id>/get_order_amount_of_specific_shop/', views.get_order_amount_of_specific_shop), 
    path('<id>/get_notification_setting_of_specific_shop/', views.get_notification_setting_of_specific_shop), 
    path('<id>/get_order_amount_of_specific_shop/', views.get_order_amount_of_specific_shop), 
    path('<id>/get_shop_address/', views.get_shop_address),
    path('<id>/createShopAddress/', views.createShopAddress),
    path('updateShopAddress_isDefault/', views.updateShopAddress_isDefault),
    path('updateShopAddress/', views.updateShopAddress),
    path('updateShopAddress_isAddressShow/', views.updateShopAddress_isAddressShow),
    path('<id>/update_notification_setting_of_specific_shop/', views.update_notification_setting_of_specific_shop)
]