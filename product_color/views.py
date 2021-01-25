from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.db.models import Q
from hkshopu import models
import re

# Create your views here.

# 取得商品顏色
def index(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'product_color_list': []
    }

    if request.method == 'GET':
        if responseData['status'] == 0:
            productColors = models.Product_Color.objects.all()
            if len(productColors) == 0:
                responseData['status'] = 1
                responseData['ret_val'] = '您尚未建立任何商品顏色!'
            else:
                for productColor in productColors:
                    productColorInfo = {
                        'id': productColor.id, 
                        'c_product_color': productColor.c_product_color, 
                        'e_product_color': productColor.e_product_color, 
                        'created_at': productColor.created_at, 
                        'updated_at': productColor.updated_at
                    }
                    responseData['product_color_list'].append(productColorInfo)
                responseData['ret_val'] = '已取得商品顏色!'
    return JsonResponse(responseData) 