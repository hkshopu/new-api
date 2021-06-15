from django.shortcuts import render
from django.db.models import Q, Avg, Min, Max, Count, Sum
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.contrib.auth.hashers import make_password
from passlib.handlers.django import django_pbkdf2_sha256
from django.core import mail
from django.utils.html import strip_tags
from hkshopu import models
import uuid
import datetime
import re
import random

# Create your views here.

# Audit_log 首頁
def get_all_audit_logs_page(request):
    template = get_template('audit_log/index.html')
    html = template.render()
    return HttpResponse(html)
# 取得 Audit_log 資料
def get_all_audit_logs(request):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            audit_logs = models.Audit_Log.objects.all()
            if len(audit_logs) == 0:
                response_data['status'] = -1
                response_data['ret_val'] = '暫無資料!'

        if response_data['status'] == 0:
            for audit_log in audit_logs:
                response_data['data'].append({
                    'id': audit_log.id, 
                    'user_id': audit_log.user_id, 
                    'action': audit_log.action, 
                    'parameter_in': audit_log.parameter_in, 
                    'parameter_out': audit_log.parameter_out, 
                    'created_at': audit_log.created_at, 
                    'updated_at': audit_log.updated_at
                })
            response_data['ret_val'] = '取得 Audit_log 資料成功!'
    return JsonResponse(response_data)