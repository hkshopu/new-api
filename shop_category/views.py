from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from hkshopu import models
import re

# Create your views here.

# 取得商店分類清單
def index(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'shop_category_list': []
    }

    if request.method == 'GET':
        if responseData['status'] == 0:
            shopCategories = models.Shop_Category.objects.all()
            if len(shopCategories) == 0:
                responseData['status'] = 1
                responseData['ret_val'] = '未建立任何商店分類!'
            else:
                for shopCategory in shopCategories:
                    shopCategoryInfo = {
                        'id': shopCategory.id, 
                        'c_shop_category': shopCategory.c_shop_category, 
                        'e_shop_category': shopCategory.e_shop_category, 
                        'unselected_shop_category_icon': shopCategory.unselected_shop_category_icon,
                        'selected_shop_category_icon': shopCategory.selected_shop_category_icon, 
                        'c_shop_category_icon': shopCategory.c_shop_category_icon, 
                        'e_shop_category_icon': shopCategory.e_shop_category_icon, 
                        'shop_category_seq': shopCategory.shop_category_seq,  
                        'created_at': shopCategory.created_at, 
                        'updated_at': shopCategory.updated_at
                    }
                    responseData['shop_category_list'].append(shopCategoryInfo)
                responseData['ret_val'] = '已取得商店清單!'
    return JsonResponse(responseData)
# 新增商店分類
def save(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        c_shop_category = request.POST.get('c_shop_category', '')
        e_shop_category = request.POST.get('e_shop_category', '')
        unselected_shop_category_icon = request.FILES.get('unselected_shop_category_icon')
        selected_shop_category_icon = request.FILES.get('selected_shop_category_icon')
        shop_category_seq = request.POST.get('shop_category_seq', '')
        # 檢查欄位是否填寫
        if response_data['status'] == 0:
            if not(c_shop_category):
                response_data['status'] = -1
                response_data['ret_val'] = ''

        if response_data['status'] == 0:
            if not(e_shop_category):
                response_data['status'] = -2
                response_data['ret_val'] = ''

        if response_data['status'] == 0:
            if not(unselected_shop_category_icon):
                response_data['status'] = -3
                response_data['ret_val'] = ''

        if response_data['status'] == 0:
            if not(selected_shop_category_icon):
                response_data['status'] = -4
                response_data['ret_val'] = ''

        if response_data['status'] == 0:
            if not(shop_category_seq):
                response_data['status'] = -5
                response_data['ret_val'] = ''
        # 檢查欄位格式是否正確
        if response_data['status'] == 0:
            if not(re.match('^[\u4e00-\u9fa5]{1,50}$', c_shop_category)):
                response_data['status'] = -6
                response_data['ret_val'] = ''

        if response_data['status'] == 0:
            if not(re.match('^[A-Za-z]{1,50}$', e_shop_category)):
                response_data['status'] = -7
                response_data['ret_val'] = ''

        if response_data['status'] == 0:
            if not(re.match('^\w+\.(gif|png|jpg|jpeg)$', str(unselected_shop_category_icon.name))):
                response_data['status'] = -8
                response_data['ret_val'] = ''

        if response_data['status'] == 0:
            if not(re.match('^\w+\.(gif|png|jpg|jpeg)$', str(selected_shop_category_icon.name))):
                response_data['status'] = -9
                response_data['ret_val'] = ''

        if response_data['status'] == 0:
            if not(re.match('^\d+$', shop_category_seq)):
                response_data['status'] = -10
                response_data['ret_val'] = ''
    return JsonResponse(response_data)
