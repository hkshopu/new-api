from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.db.models import Q
from hkshopu import models
import re

# Create your views here.

# 取得產品產地清單
def index(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'product_origin_list': []
    }

    if request.method == 'GET':
        if response_data['status'] == 0:
            product_origin_list = models.Product_Origin.objects.all()
            if len(product_origin_list) == 0:
                response_data['status'] = 1
                response_data['ret_val'] = '您尚未新增任何產品產地清單!'

        if response_data['status'] == 0:
            for product_origin in product_origin_list:
                product_origin_info = {
                    'id': product_origin.id, 
                    'c_product_origin': product_origin.c_product_origin, 
                    'e_product_origin': product_origin.e_product_origin, 
                    'created_at': product_origin.created_at, 
                    'updated_at': product_origin.updated_at
                }
                response_data['product_origin_list'].append(product_origin_info)
            response_data['ret_val'] = '已取得產品產地清單!'
    return JsonResponse(response_data)