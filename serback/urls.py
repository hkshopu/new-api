from django.urls import path
from . import views

urlpatterns = [
    path('audit_logs/', views.get_all_audit_logs)
]