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
        
        # 檢查欄位是否填寫及格式是否正確
        
    return JsonResponse(response_data)
