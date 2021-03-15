from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.db.models import Q
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
                        'shop_category_icon': shopCategory.shop_category_icon, 
                        'created_at': shopCategory.created_at, 
                        'updated_at': shopCategory.updated_at
                    }
                    responseData['shop_category_list'].append(shopCategoryInfo)
                responseData['ret_val'] = '已取得商店清單!'
    return JsonResponse(responseData)