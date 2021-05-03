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
    path('bankAccount/<id>/update/BankAccount/', views.updateBankAccount),
    path('bankAccount/<id>/delete/BankAccount/', views.delBankAccount),
    path('test/', views.testAPI)
]