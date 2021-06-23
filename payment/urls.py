from django.urls import path
from . import views

urlpatterns = [
    path('method/', views.method),
    path('confirmFPSOrderTransaction/', views.confirmFPSOrderTransaction)
]