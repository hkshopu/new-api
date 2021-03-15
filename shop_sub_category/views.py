from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.db.models import Q
from hkshopu import models
import re

# Create your views here.

# 取得商店子分類清單
def index(request):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'shop_sub_category_list': []
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            shop_sub_categories = models.Shop_Sub_Category.objects.all()
            if len(shop_sub_categories) == 0:
                response_data['status'] = 1
                response_data['ret_val'] = '您尚未建立任何商店子分類!'

        if response_data['status'] == 0:
            for shop_sub_category in shop_sub_categories:
                shop_sub_category_info = {
                    'id': shop_sub_category.id, 
                    'shop_category_id': shop_sub_category.shop_category_id, 
                    'c_shop_sub_category': shop_sub_category.c_shop_sub_category, 
                    'e_shop_sub_category': shop_sub_category.e_shop_sub_category, 
                    'shop_sub_category_icon': shop_sub_category.shop_sub_category_icon, 
                    'created_at': shop_sub_category.created_at, 
                    'updated_at': shop_sub_category.updated_at
                }
                response_data['shop_sub_category_list'].append(shop_sub_category_info)
            response_data['ret_val'] = '已取得商店子分類清單!'
    return JsonResponse(response_data)