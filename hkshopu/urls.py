from django.urls import path
from . import views

urlpatterns = [
    # user
    path('user/register/', views.register),
    path('user/registerProcess/', views.registerProcess),
    path('user/loginProcess/', views.loginProcess),
    path('user/socialLoginProcess/', views.socialLoginProcess),
    path('user/forgetPasswordProcess/', views.forgetPasswordProcess),
    path('user/<id>/shop/', views.getUserShopListProcess), 
    # shop
    path('shop/create/', views.createShop), 
    path('shop/save/', views.saveShop), 
    path('shop/<id>/update/', views.updateShop), 
    path('shop/<id>/show/', views.showShop), 
    # shop_category
    path('shop_category/', views.getShopCategoryList), 
    # color
    path('color/', views.getProductColorList), 
]