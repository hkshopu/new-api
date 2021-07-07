from django.urls import path
from . import views

urlpatterns = [
    path('update_detail/', views.update_detail),   
    path('<user_id>/user_rate/', views.user_rate), 
    path('user_liked/', views.user_liked),  
    path('<user_id>/liked_count/', views.liked_count), 
    path('user_followed/', views.user_followed),  
    path('<user_id>/followed_count/', views.followed_count),
    path('<user_id>/browsed_count/', views.browsed_count),  
    path('user_browsed/', views.user_browsed),  
    path('<user_id>/show/', views.show),     
    path('add_pic/', views.add_pic), 
    path('userAddress_isDefault/', views.userAddress_isDefault), 
    path('<user_id>/profile/', views.profile),
    path('shopping_list/', views.shopping_list), 
    path('<order_id>/order_detail/', views.order_detail),
]