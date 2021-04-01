from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index), 
    path('<id>/show/', views.show), 
    path('<id>/product_sub_category/', views.get_product_sub_category_list_of_specific_product_category)
]