from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.db.models import Q
from hkshopu import models
import re

# Create your views here.

# 取得產品分類清單
def index(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'product_category_list': []
    }

    if request.method == 'GET':
        if response_data['status'] == 0:
            product_category_list = models.Product_Category.objects.all().order_by('product_category_seq')
            if len(product_category_list) == 0:
                response_data['status'] = 1
                response_data['ret_val'] = '您尚未新增任何產品分類!'

        if response_data['status'] == 0:
            for product_category in product_category_list:
                product_category_info = {
                    'id': product_category.id, 
                    'c_product_category': product_category.c_product_category, 
                    'e_product_category': product_category.e_product_category, 
                    'unselected_product_category_icon': product_category.unselected_product_category_icon, 
                    'selected_product_category_icon': product_category.selected_product_category_icon, 
                    'product_category_background_color': product_category.product_category_background_color, 
                    'product_category_seq': product_category.product_category_seq, 
                    'is_delete': product_category.is_delete, 
                    'created_at': product_category.created_at, 
                    'updated_at': product_category.updated_at
                }
                response_data['product_category_list'].append(product_category_info)
            response_data['ret_val'] = '已取得產品分類清單!'
    return JsonResponse(response_data)
# 取得單一商品分類
def show(request, id):
    pass
# 取得單一產品分類子分類清單
def get_product_sub_category_list_of_specific_product_category(request, id):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'product_sub_category_list': []
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            product_sub_categories = models.Product_Sub_Category.objects.filter(product_category_id=id).order_by('product_sub_category_seq')
            if len(product_sub_categories) == 0:
                response_data['status'] = 1
                response_data['ret_val'] = '此商品分類尚未建立子分類!'

        if response_data['status'] == 0:
            for product_sub_category in product_sub_categories:
                product_sub_category_info = {
                    'id': product_sub_category.id, 
                    'product_category_id': product_sub_category.product_category_id, 
                    'c_product_sub_category': product_sub_category.c_product_sub_category, 
                    'e_product_sub_category': product_sub_category.e_product_sub_category, 
                    'unselected_product_sub_category_icon': product_sub_category.unselected_product_sub_category_icon, 
                    'selected_product_sub_category_icon': product_sub_category.selected_product_sub_category_icon, 
                    'product_sub_category_background_color': product_sub_category.product_sub_category_background_color, 
                    'product_sub_category_seq': product_sub_category.product_sub_category_seq, 
                    'is_delete': product_sub_category.is_delete, 
                    'created_at': product_sub_category.created_at, 
                    'updated_at': product_sub_category.updated_at
                }
                response_data['product_sub_category_list'].append(product_sub_category_info)
            response_data['ret_val'] = '取得單一產品分類子分類清單成功!'
    return JsonResponse(response_data)