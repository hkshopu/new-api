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
# Shop_Clicked 首頁
def get_all_shop_clicked_page(request):
    template = get_template('shop_clicked/index.html')
    html = template.render()
    return HttpResponse(html)
# 取得 Shop_Clicked 資料
def get_all_shop_clicked(request):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            datas_of_shop_clicked = models.Shop_Clicked.objects.all()
            if len(datas_of_shop_clicked) == 0:
                response_data['status'] = -1
                response_data['ret_val'] = '暫無資料!'

        if response_data['status'] == 0:
            for data in datas_of_shop_clicked:
                response_data['data'].append({
                    'id': data.id, 
                    'shop_id': data.shop_id, 
                    'user_id': data.user_id, 
                    'created_at': data.created_at, 
                    'updated_at': data.updated_at
                })
            response_data['ret_val'] = '取得 Shop_Clicked 資料成功!'
    return JsonResponse(response_data)
# Product_Clicked 首頁
def get_all_product_clicked_page(request):
    template = get_template('product_clicked/index.html')
    html = template.render()
    return HttpResponse(html)
# 取得 Product_Clicked 資料
def get_all_product_clicked(request):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            datas_of_product_clicked = models.Product_Clicked.objects.all()
            if len(datas_of_product_clicked) == 0:
                response_data['status'] = -1
                response_data['ret_val'] = '暫無資料!'

        if response_data['status'] == 0:
            for data in datas_of_product_clicked:
                response_data['data'].append({
                    'id': data.id, 
                    'product_id': data.product_id, 
                    'user_id': data.user_id, 
                    'created_at': data.created_at, 
                    'updated_at': data.updated_at
                })
            response_data['ret_val'] = '取得 Product_Clicked 資料成功!'
    return JsonResponse(response_data)
# Shop_Browsed 首頁
def get_all_shop_browsed_page(request):
    template = get_template('shop_browsed/index.html')
    html = template.render()
    return HttpResponse(html)
# 取得 Shop_Browsed 資料
def get_all_shop_browsed(request):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            datas_of_shop_browsed = models.Shop_Browsed.objects.all()
            if len(datas_of_shop_browsed) == 0:
                response_data['status'] = -1
                response_data['ret_val'] = '暫無資料!'

        if response_data['status'] == 0:
            for data in datas_of_shop_browsed:
                response_data['data'].append({
                    'id': data.id, 
                    'shop_id': data.shop_id, 
                    'user_id': data.user_id, 
                    'created_at': data.created_at, 
                    'updated_at': data.updated_at
                })
            response_data['ret_val'] = '取得 Shop_Browsed 資料成功!'
    return JsonResponse(response_data)
# Product_Browsed 首頁
def get_all_product_browsed_page(request):
    template = get_template('product_browsed/index.html')
    html = template.render()
    return HttpResponse(html)
# 取得 Product_Browsed 資料
def get_all_product_browsed(request):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            datas_of_product_browsed = models.Product_Browsed.objects.all()
            if len(datas_of_product_browsed) == 0:
                response_data['status'] = -1
                response_data['ret_val'] = '暫無資料!'

        if response_data['status'] == 0:
            for data in datas_of_product_browsed:
                response_data['data'].append({
                    'id': data.id, 
                    'product_id': data.product_id, 
                    'user_id': data.user_id, 
                    'created_at': data.created_at, 
                    'updated_at': data.updated_at
                })
            response_data['ret_val'] = '取得 Product_Browsed 資料成功!'
    return JsonResponse(response_data)