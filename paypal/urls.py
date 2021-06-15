from django.urls import path
from . import views

urlpatterns = [
    path('createPayment/', views.createPayment),
    path('executePayment/', views.executePayment),
    path('getPaymentDetails/', views.getPaymentDetails)
]