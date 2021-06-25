from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.db.models import Q
from hkshopu import models
import re
import uuid

# Create your views here.

# 新增選擇商店分類
def save(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        shop_id = request.POST.get('shop_id', '')
        shop_category_id = request.POST.getlist('shop_category_id', [])
        # 檢查欄位是否填寫
        if response_data['status'] == 0:
            if not(shop_id):
                response_data['status'] = -1
                response_data['ret_val'] = '未填寫商店編號!'

        if response_data['status'] == 0:
            if not(shop_category_id):
                response_data['status'] = -2
                response_data['ret_val'] = '未填寫商店分類編號!'
        # 檢查欄位格式是否正確
        if response_data['status'] == 0:
            if not(re.match('^\d+$', shop_id)):
                response_data['status'] = -3
                response_data['ret_val'] = '商店編號格式錯誤!'

        if response_data['status'] == 0:
            for value in shop_category_id:
                if not(re.match('^\d+$', value)):
                    response_data['status'] = -4
                    response_data['ret_val'] = '商店分類編號格式錯誤!'
                    break

        if response_data['status'] == 0:
            to_delete_selected_shop_categories = models.Selected_Shop_Category.objects.filter(shop_id=shop_id).exclude(shop_category_id__in=shop_category_id)
            if len(to_delete_selected_shop_categories) > 0:
                to_delete_selected_shop_categories.delete()

            for value in shop_category_id:
                selected_shop_categories = models.Selected_Shop_Category.objects.filter(shop_id=shop_id, shop_category_id=value)
                if len(selected_shop_categories) == 0:
                    models.Selected_Shop_Category.objects.create(
                        id=uuid.uuid4(),
                        shop_id=shop_id, 
                        shop_category_id=value
                    )
            response_data['ret_val'] = '新增選擇商店分類成功!'
    return JsonResponse(response_data)