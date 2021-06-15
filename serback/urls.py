from django.urls import path
from . import views

urlpatterns = [
    path('get_all_audit_logs_page/', views.get_all_audit_logs_page),
    path('get_all_audit_logs/', views.get_all_audit_logs)
]