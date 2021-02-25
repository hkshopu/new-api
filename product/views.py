from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.db.models import Q
from hkshopu import models
import re

# Create your views here.

# 新增產品
def save(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': ''
    }

    if request.method == 'POST':
        # 欄位資料
        shop_id = request.POST.get('shop_id', '')
        product_category_id = request.POST.get('product_category_id', '')
        product_sub_category_id = request.POST.get('product_sub_category_id', '')
        product_title = request.POST.get('product_title', '')
        quantity = request.POST.get('quantity', 0)
        product_description = request.POST.get('product_description', '')
        product_country_code = request.POST.get('product_country_code', '')
        product_price = request.POST.get('product_price', 0)
        shipping_fee = request.POST.get('shipping_fee', 0)
        weight = request.POST.get('weight', 0)
        # 檢查各欄位是否填寫
        if response_data['status'] == 0:
            if not(shop_id):
                response_data['status'] = -1
                response_data['ret_val'] = '未填寫商店編號!'
        
        if response_data['status'] == 0:
            if not(product_category_id):
                response_data['status'] = -2
                response_data['ret_val'] = '未填寫產品分類編號!'

        if response_data['status'] == 0:
            if not(product_sub_category_id):
                response_data['status'] = -3
                response_data['ret_val'] = '未填寫產品子分類編號!'

        if response_data['status'] == 0:
            if not(product_title):
                response_data['status'] = -4
                response_data['ret_val'] = '未填寫產品標題!'

        if response_data['status'] == 0:
            if not(product_description):
                response_data['status'] = -5
                response_data['ret_val'] = '未填寫產品描述!'

        if response_data['status'] == 0:
            if not(product_price):
                response_data['status'] = -6
                response_data['ret_val'] = '未填寫產品單價!'

        if response_data['status'] == 0:
            if not(shipping_fee):
                response_data['status'] = -7
                response_data['ret_val'] = '未填寫產品運費!'
        # 驗證各欄位格式是否正確
        if response_data['status'] == 0:
            if not(re.match('^\d+$', shop_id)):
                response_data['status'] = -8
                response_data['ret_val'] = '商店編號格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^\d+$', product_category_id)):
                response_data['status'] = -9
                response_data['ret_val'] = '產品分類編號格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^\d+$', product_sub_category_id)):
                response_data['status'] = -10
                response_data['ret_val'] = '產品子分類編號格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^\w+$', product_title)):
                response_data['status'] = -11
                response_data['ret_val'] = '產品標題格式錯誤!'

        if response_data['status'] == 0:
            if quantity:
                if not(re.match('^\d+$', quantity)):
                    response_data['status'] = -12
                    response_data['ret_val'] = '產品庫存數量格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^\w+$', product_description)):
                response_data['status'] = -13
                response_data['ret_val'] = '產品描述格式錯誤!'

        if response_data['status'] == 0:
            if product_country_code:
                if not(re.match('^\d+$', product_country_code)):
                    response_data['status'] = -14
                    response_data['ret_val'] = '產品產地代碼格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^\d+$', product_price)):
                response_data['status'] = -15
                response_data['ret_val'] = '產品價格格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^\d+$', shipping_fee)):
                response_data['status'] = -16
                response_data['ret_val'] = '產品運費格式錯誤!'

        if response_data['status'] == 0:
            if weight:
                if not(re.match('^\d+$', weight)):
                    response_data['status'] = -17
                    response_data['ret_val'] = '產品重量格式錯誤!'
        # 檢查商店編號是否存在
        if response_data['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=shop_id)
            except:
                response_data['status'] = -18
                response_data['ret_val'] = '商店編號不存在!'
        # 檢查產品分類編號是否正確
        if response_data['status'] == 0:
            try:
                product_category = models.Product_Category.objects.get(id=product_category_id)
            except:
                response_data['status'] = -19
                response_data['ret_val'] = '產品分類編號不存在!'
        # 檢查產品子分類編號是否正確
        if response_data['status'] == 0:
            try:
                product_sub_category = models.Product_Sub_Category.objects.get(id=product_sub_category_id)
            except:
                response_data['status'] = -20
                response_data['ret_val'] = '產品子分類編號不存在!'

        if response_data['status'] == 0:
            models.Product.objects.create(
                shop_id=shop_id, 
                product_category_id=product_category_id, 
                product_sub_category_id=product_sub_category_id, 
                product_title=product_title, 
                quantity=quantity, 
                product_description=product_description, 
                product_country_code=product_country_code, 
                product_price=product_price, 
                shipping_fee=shipping_fee, 
                weight=weight
            )
            response_data['ret_val'] = '產品新增成功!'
    return JsonResponse(response_data)