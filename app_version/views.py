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

# 取得最新 App 版本編號
def get_latest_app_version_number(request):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': {}
    }
    if request.method == 'GET':
        # 欄位資料
        app_type = request.GET.get('app_type', '')

        if response_data['status'] == 0:
            app_versions = models.App_Version.objects.filter(app_type=app_type).values('version_number')
            if len(app_versions) == 0:
                response_data['data']['version_number'] = ''
                response_data['status'] = -1
                response_data['ret_val'] = '找不到該作業系統之 App 版本編號!'

        if response_data['status'] == 0:
            response_data['data']['version_number'] = app_versions[0]['version_number']
            response_data['ret_val'] = '取得最新 App 版本編號成功!'
    return JsonResponse(response_data)
