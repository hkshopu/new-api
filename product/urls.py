from django.urls import path
from . import views

urlpatterns = [
    path('save/', views.save), 
    path('index/', views.index),
    path('spec_test/', views.spec_test),
    # path('<id>/<keyword>/<product_status>/<quantity>/shop_product/', views.shop_product),
    path('<id>/shop_product/', views.shop_product),
    path('<id>/product_info/', views.product_info),
    path('<id>/product_info_forAndroid/', views.product_info_forAndroid),
    path('<id>/update/', views.update),  
    path('<id>/<keyword>/<product_status>/<quantity>/product_list/', views.product_list),
    path('update_product_status/', views.update_product_status),
    path('update_product_status_forAndroid/', views.update_product_status_forAndroid),
    path('<id>/delete_product/', views.delete_product),
    path('<id>/product_analytics/', views.product_analytics),
    path('like_product/', views.like_product),
    path('<shop_id>/<mode>/shop_product_analytics/', views.shop_product_analytics),
    path('<mode>/product_analytics_pages/', views.product_analytics_pages),
    path('<mode>/product_analytics_pages_keyword/', views.product_analytics_pages_keyword),
    path('similar_product_list/', views.similar_product_list),
    path('same_shop_product/', views.same_shop_product),
    path('add_shopping_cart/', views.add_shopping_cart),
    path('<user_id>/shopping_cart_item/', views.shopping_cart_item),
    path('<id>/get_product_rating_details_for_buyer/', views.get_product_rating_details_for_buyer), 
    path('<id>/get_specification_of_product/', views.get_specification_of_product)
]