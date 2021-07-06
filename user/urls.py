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
    path('send_invitation_testing_mail_page/', views.send_invitation_testing_mail_page, name='user.send_invitation_testing_mail_page'), 
    path('send_invitation_testing_mail/', views.send_invitation_testing_mail, name='user.send_invitation_testing_mail'),
    path('<user_id>/followShop/<shop_id>/', views.followShop),
    path('<user_id>/topProductDetail/<product_id>/', views.topProductDetail),
    path('/topProductDetail/<product_id>/', views.topProductDetail), # if user_id=''
    path('<user_id>/auditLog/', views.auditLog),
    path('/auditLog/', views.auditLog), # if user_id=''
    path('user_id_validation/', views.user_id_validation),
    path('<user_id>/addPaymentAccount/', views.addPaymentAccount),
    path('<user_id>/addPaymentAccount/<id>/', views.addPaymentAccount),
    path('addPaymentAccount/<id>/', views.addPaymentAccount),
    path('<user_id>/adSetting/<ad_category>/<ad_type>/', views.adSetting),
    path('updateAdSetting/<ad_category>/<ad_type>/<ad_setting_header_id>/', views.updateAdSetting),
    path('adSettingRanking/<ad_category>/<ad_type>/', views.adSettingRanking)
]
