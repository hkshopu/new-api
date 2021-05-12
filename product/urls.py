from django.urls import path
from . import views

urlpatterns = [
    path('save/', views.save), 
    path('index/', views.index),
    # path('<id>/<keyword>/<product_status>/<quantity>/shop_product/', views.shop_product),
    path('<id>/shop_product/', views.shop_product),
    path('<id>/product_info/', views.product_info),
    path('<id>/product_info_forAndroid/', views.product_info_forAndroid),
    path('<id>/update/', views.update),  
    path('<id>/<keyword>/<product_status>/<quantity>/product_list/', views.product_list),
    path('update_product_status/', views.update_product_status),
    path('update_product_status_forAndroid/', views.update_product_status),
]