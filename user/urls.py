from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('checkEmailExistsProcess/', views.checkEmailExistsProcess), 
    path('registerProcess/', views.registerProcess),
    path('loginProcess/', views.loginProcess),
    path('socialLoginProcess/', views.socialLoginProcess),
    path('forgetPasswordProcess/', views.forgetPasswordProcess),
    path('<id>/shop/', views.getUserShopListProcess),
    path('generateAndSendValidationCodeProcess/', views.generateAndSendValidationCodeProcess),
    path('validateEmailProcess/', views.validateEmailProcess), 
    path('resetPasswordProcess/', views.resetPasswordProcess), 
    path('checkEmailIsAllowedLoginProcess/', views.checkEmailIsAllowedLoginProcess), 
    path('getUserListProcess/', views.getUserListProcess), 
    path('<id>/show/', views.show),
    path('<id>/shopCount/', views.getUserShopCount), 
    path('sned_invitation_testing_mail/', views.sned_invitation_testing_mail)
]