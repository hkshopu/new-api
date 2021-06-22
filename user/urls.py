from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('page_of_invitation_email/', views.page_of_invitation_email), 
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
    path('sned_invitation_testing_mail/', views.sned_invitation_testing_mail),
    path('<user_id>/followShop/<shop_id>/', views.followShop),
    path('<user_id>/topProductDetail/<product_id>/', views.topProductDetail),
    path('/topProductDetail/<product_id>/', views.topProductDetail), # if user_id=''
    path('<user_id>/auditLog/', views.auditLog),
    path('/auditLog/', views.auditLog), # if user_id=''
    path('<user_id>/addPaymentAccount/', views.addPaymentAccount), 
    path('user_id_validation/', views.user_id_validation),
    path('<user_id>/addPaymentAccount/', views.addPaymentAccount),
    path('<user_id>/addPaymentAccount/<id>/', views.addPaymentAccount)
]
