from django.urls import path
from . import views

urlpatterns = [
    path('bankCode/', views.bankCode),
    path('keywordSearchCount/<keyword>/', views.keywordSearchCount),
    path('searchGmail/', views.searchGmail)
]