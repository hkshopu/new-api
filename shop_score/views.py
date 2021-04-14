from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.db.models import Q
from hkshopu import models
import re

# Create your views here.

# 新增選擇的產品顏色頁面
# def create(request):
#     template = get_template('selected_product_color/create.html')
#     html = template.render()
#     return HttpResponse(html)
# 新增選擇的產品顏色
def save(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': ''
    }

    if request.method == 'POST':
        # 欄位資料
        shop_id = request.POST.get('shop_id', '')
        user_id = request.POST.get('user_id', '')
        score = request.POST.get('score', '')
        comment = request.POST.get('comment', '')

        if response_data['status'] == 0:
            if not(shop_id):
                response_data['status'] = -1
                response_data['ret_val'] = '未填寫商店編號!'

        if response_data['status'] == 0:
            if not(user_id):
                response_data['status'] = -2
                response_data['ret_val'] = '未填寫userID!'
        if response_data['status'] == 0:
            if not(score):
                response_data['status'] = -3
                response_data['ret_val'] = '未填寫評分!'
        if response_data['status'] == 0:
            if not(comment):
                response_data['status'] = -4
                response_data['ret_val'] = '未填寫評論!'
        
        # 等Data確定再取消
        
        # if response_data['status'] == 0:
        #     try:
        #         shop = models.Shop.objects.get(id=shop_id)
        #     except:
        #         response_data['status'] = -5
        #         response_data['ret_val'] = '該商店編號錯誤或不存在!'

        # if response_data['status'] == 0:
        #     try:
        #         user = models.User.objects.get(id=user_id)
        #     except:
        #         response_data['status'] = -6
        #         response_data['ret_val'] = '該商店編號錯誤或不存在!'

        if response_data['status'] == 0:
            models.Shop_Score.objects.create(
                shop_id=shop_id, 
                user_id=user_id,
                score=score,
                comment=comment
            )
            response_data['ret_val'] = '商店評分新增成功!'
    return JsonResponse(response_data)