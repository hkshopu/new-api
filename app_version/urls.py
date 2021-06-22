from django.urls import path
from . import views

urlpatterns = [
    path('get_latest_app_version_number/', views.get_latest_app_version_number)
]