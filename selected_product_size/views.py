from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.db.models import Q
from hkshopu import models
import re
import uuid
# Create your views here.

def save(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': ''
    }

    if request.method == 'POST':
        # 欄位資料
        product_id = request.POST.get('product_id', '')
        size_id_list = request.POST.getlist('size_id', [])

        if response_data['status'] == 0:
            if not(product_id):
                response_data['status'] = -1
                response_data['ret_val'] = '未填寫產品編號!'

        if response_data['status'] == 0:
            if not(size_id_list):
                response_data['status'] = -2
                response_data['ret_val'] = '未填寫產品尺寸編號!'

        if response_data['status'] == 0:
            try:
                models.Product.objects.get(id=product_id)
            except:
                response_data['status'] = -3
                response_data['ret_val'] = '產品編號格式錯誤!'

        if response_data['status'] == 0:
            for size_id in size_id_list:
                try:
                    models.Product_Size.objects.get(id=size_id)
                except:
                    response_data['status'] = -4
                    response_data['ret_val'] = '產品尺寸編號格式錯誤!'
                    break

        if response_data['status'] == 0:
            try:
                product = models.Product.objects.get(id=product_id)
            except:
                response_data['status'] = -5
                response_data['ret_val'] = '產品編號錯誤或不存在!'

        if response_data['status'] == 0:
            for size_id in size_id_list:
                try:
                    product = models.Product_Size.objects.get(id=size_id)
                except:
                    response_data['status'] = -6
                    response_data['ret_val'] = '產品尺寸編號錯誤或不存在!'
                    break

        if response_data['status'] == 0:
            for size_id in size_id_list:
                same_selected_product_size = models.Selected_Product_Size.objects.filter(product_id=product_id, size_id=size_id)
                if len(same_selected_product_size) > 0:
                    response_data['status'] = -7
                    response_data['ret_val'] = '您選擇的產品尺寸編號已存在!'
                    break

        if response_data['status'] == 0:
            for size_id in size_id_list:
                models.Selected_Product_Size.objects.create(
                    id=uuid.uuid4(),
                    product_id=product_id, 
                    size_id=size_id
                )
            response_data['ret_val'] = '產品尺寸新增成功!'
    return JsonResponse(response_data)
