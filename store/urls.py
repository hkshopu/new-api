"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('user/', include('user.urls')), 
    path('shop/', include('shop.urls')), 
    path('shop_category/', include('shop_category.urls')),
    path('shop_sub_category/', include('shop_sub_category.urls')), 
    path('product/', include('product.urls')), 
    path('product_color/', include('product_color.urls')), 
    path('product_size/', include('product_size.urls')), 
    path('product_category/', include('product_category.urls')), 
    path('product_sub_category/', include('product_sub_category.urls')), 
    path('product_origin/', include('product_origin.urls')), 
    path('selected_product_color/', include('selected_product_color.urls')), 
    path('selected_product_size/', include('selected_product_size.urls')), 
    path('selected_product_pic/', include('selected_product_pic.urls')), 
    path('selected_shop_category/', include('selected_shop_category.urls')),
    path('shop_sub_category/', include('shop_sub_category.urls')),
    path('serback/', include('serback.urls')),
    path('shopping_cart/', include('shopping_cart.urls')),
    path('payment/', include('payment.urls')),
    path('general/', include('general.urls')), 
    path('app_version/', include('app_version.urls')), 
    path('shop_order/', include('shop_order.urls')), 
    path('user_detail/', include('user_detail.urls'))
]
