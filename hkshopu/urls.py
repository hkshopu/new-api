from django.urls import path
from . import views

urlpatterns = [
    # user
    path('user/register/', views.register),
    path('user/registerProcess/', views.registerProcess),
    path('user/loginProcess/', views.loginProcess),
    path('user/socialLoginProcess/', views.socialLoginProcess),
    path('user/forgetPasswordProcess/', views.forgetPasswordProcess),
    path('user/<id>/shop/', views.getShopListProcess), 
    # shop
    path('shop/create/', views.create), 
    path('shop/save/', views.save), 
    path('shop/<id>/update/', views.update), 
    path('shop/<id>/show/', views.show), 
]