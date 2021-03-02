from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('registerProcess/', views.registerProcess),
    path('loginProcess/', views.loginProcess),
    path('socialLoginProcess/', views.socialLoginProcess),
    path('forgetPasswordProcess/', views.forgetPasswordProcess),
    path('<id>/shop/', views.getUserShopListProcess),
    path('<id>/generateAndSendValidationCodeProcess/', views.generateAndSendValidationCodeProcess),
    path('validateEmailProcess/', views.validateEmailProcess)
]