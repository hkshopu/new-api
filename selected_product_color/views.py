from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.db.models import Q
from hkshopu import models
import re

# Create your views here.

# 新增選擇的產品顏色頁面
def create(request):
    template = get_template('selected_product_color/create.html')
    html = template.render()
    return HttpResponse(html)
# 新增選擇的產品顏色
def save(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': ''
    }

    if request.method == 'POST':
        # 欄位資料
        product_id = request.POST.get('product_id', '')
        color_id = request.POST.get('color_id', '')

        if response_data['status'] == 0:
            if not(product_id):
                response_data['status'] = -1
                response_data['ret_val'] = '未填寫產品編號!'

        if response_data['status'] == 0:
            if not(color_id):
                response_data['status'] = -2
                response_data['ret_val'] = '未填寫產品顏色編號!'

        if response_data['status'] == 0:
            if not(re.match('^\d+$', product_id)):
                response_data['status'] = -3
                response_data['ret_val'] = '產品編號格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^\d+$', color_id)):
                response_data['status'] = -4
                response_data['ret_val'] = '產品顏色編號格式錯誤!'

        if response_data['status'] == 0:
            try:
                product = models.Product.objects.get(id=product_id)
            except:
                response_data['status'] = -5
                response_data['ret_val'] = '該產品編號錯誤或不存在!'

        if response_data['status'] == 0:
            try:
                product_color = models.Product_Color.objects.get(id=color_id)
            except:
                response_data['status'] = -6
                response_data['ret_val'] = '該產品顏色編號錯誤或不存在!'

        if response_data['status'] == 0:
            same_selected_product_color = models.Selected_Product_Color.objects.filter(product_id=product_id, color_id=color_id)
            if len(same_selected_product_color) > 0:
                response_data['status'] = -7
                response_data['ret_val'] = '您選擇的產品與產品顏色已存在!'

        if response_data['status'] == 0:
            models.Selected_Product_Color.objects.create(
                product_id=product_id, 
                color_id=color_id
            )
            response_data['ret_val'] = '產品顏色新增成功!'
    return JsonResponse(response_data)