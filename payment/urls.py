from django.urls import path
from . import views

urlpatterns = [
    path('method/', views.method),
    path('confirmFPSOrderTransaction/', views.confirmFPSOrderTransaction),
    path('paymentProcess/', views.paymentProcess),
    path('paypalWebHooks/', views.paypalWebHooks),
    path('paypalWebHooks_COC/', views.paypalWebHooks_COC),
    path('paypalWebHooks_COA/', views.paypalWebHooks_COA),
    path('paypalWebHooks_PSC/', views.paypalWebHooks_PSC),
    path('paypalWebHooks_POC/', views.paypalWebHooks_POC),    
    path('paypal/createPayment/', views.paypal_createPayment),
    path('paypal/executePayment/', views.paypal_executePayment),
    path('paypal/cancelPayment/', views.paypal_cancelPayment),
    path('paypal/getPaymentDetails/', views.paypal_getPaymentDetails),
    path('fps/fps_setting/', views.fps_setting)
]