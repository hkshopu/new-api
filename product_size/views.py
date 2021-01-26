from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.db.models import Q
from hkshopu import models
import re

# Create your views here.

# 取得產品尺寸清單
def index(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'product_size_list': []
    }

    if request.method == 'GET':
        if response_data['status'] == 0:
            product_size_list = models.Product_Size.objects.all()
            if len(product_size_list) == 0:
                response_data['status'] = 1
                response_data['ret_val'] = '您尚未新增任何產品尺寸!'

        if response_data['status'] == 0:
            for product_size in product_size_list:
                product_size_info = {
                    'id': product_size.id, 
                    'c_product_size': product_size.c_product_size, 
                    'e_product_size': product_size.e_product_size, 
                    'created_at': product_size.created_at, 
                    'updated_at': product_size.updated_at
                }
                response_data['product_size_list'].append(product_size_info)
            response_data['ret_val'] = '已取得產品尺寸清單!'
    return JsonResponse(response_data)