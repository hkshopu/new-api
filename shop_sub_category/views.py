from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.db.models import Q
from hkshopu import models
import re
import datetime
import random
# Create your views here.

# 取得商店子分類清單
def index(request):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'shop_sub_category_list': []
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            shop_sub_categories = models.Shop_Sub_Category.objects.all()
            if len(shop_sub_categories) == 0:
                response_data['status'] = 1
                response_data['ret_val'] = '您尚未建立任何商店子分類!'

        if response_data['status'] == 0:
            for shop_sub_category in shop_sub_categories:
                shop_sub_category_info = {
                    'id': shop_sub_category.id, 
                    'shop_category_id': shop_sub_category.shop_category_id, 
                    'c_shop_sub_category': shop_sub_category.c_shop_sub_category, 
                    'e_shop_sub_category': shop_sub_category.e_shop_sub_category, 
                    'shop_sub_category_icon': shop_sub_category.shop_sub_category_icon, 
                    'created_at': shop_sub_category.created_at, 
                    'updated_at': shop_sub_category.updated_at
                }
                response_data['shop_sub_category_list'].append(shop_sub_category_info)
            response_data['ret_val'] = '已取得商店子分類清單!'
    return JsonResponse(response_data)
# 新增商店子分類
def save(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        shop_category_id=request.POST.get('shop_category_id', '')
        c_shop_category = request.POST.get('c_shop_category', '')
        e_shop_category = request.POST.get('e_shop_category', '')
        unselected_shop_category_icon = request.FILES.get('unselected_shop_category_icon')
        selected_shop_category_icon = request.FILES.get('selected_shop_category_icon')
        # shop_category_background_color = request.POST.get('shop_category_background_color', '')
        shop_category_seq = request.POST.get('shop_category_seq', '')
        # 檢查欄位是否填寫
        if response_data['status'] == 0:
            if not(c_shop_category):
                response_data['status'] = -1
                response_data['ret_val'] = '中文商店分類未填寫!'

        if response_data['status'] == 0:
            if not(e_shop_category):
                response_data['status'] = -2
                response_data['ret_val'] = '英文商店分類未填寫!'

        if response_data['status'] == 0:
            if not(unselected_shop_category_icon):
                response_data['status'] = -3
                response_data['ret_val'] = '未上傳 unselected_shop_category_icon!'

        if response_data['status'] == 0:
            if not(selected_shop_category_icon):
                response_data['status'] = -4
                response_data['ret_val'] = '未上傳 selected_shop_category_icon!'

        # if response_data['status'] == 0:
        #     if not(shop_category_background_color):
        #         response_data['status'] = -5
        #         response_data['ret_val'] = '未填寫商店分類背景色!'

        if response_data['status'] == 0:
            if not(shop_category_seq):
                response_data['status'] = -7
                response_data['ret_val'] = '未填寫商店分類排序!'
        # 檢查欄位格式是否正確
        if response_data['status'] == 0:
            if not(re.match('^[\u4e00-\u9fa5]{1,50}$', c_shop_category)):
                response_data['status'] = -8
                response_data['ret_val'] = '中文商店分類格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^[A-Za-z]{1,50}$', e_shop_category)):
                response_data['status'] = -9
                response_data['ret_val'] = '英文商店分類格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^\w+\.(gif|png|jpg|jpeg)$', str(unselected_shop_category_icon.name))):
                response_data['status'] = -10
                response_data['ret_val'] = 'unselected_shop_category_icon 格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^\w+\.(gif|png|jpg|jpeg)$', str(selected_shop_category_icon.name))):
                response_data['status'] = -11
                response_data['ret_val'] = 'selected_shop_category_icon 格式錯誤!'

        # if response_data['status'] == 0:
        #     if not(re.match('^[A-Fa-f0-9]{1,6}$', shop_category_background_color)):
        #         response_data['status'] = -12
        #         response_data['ret_val'] = '商店分類背景色格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^\d+$', shop_category_seq)):
                response_data['status'] = -14
                response_data['ret_val'] = '商店分類排序格式錯誤!'
            
        if response_data['status'] == 0:
            # 上傳圖片
            now = datetime.datetime.now()
            file_rand_str_list = []
            for i in range(2):
                rand_num_list = []
                for j in range(12):
                    rand_num_list.append(random.choice('0123456789'))
                rand_num = ''.join(rand_num_list)
                file_rand_str_list.append(rand_num)
            new_unselected_shop_category_icon_name = now.strftime('%Y%m%d%H%M%S') + '_' + file_rand_str_list[0] + '_' + unselected_shop_category_icon.name
            new_selected_shop_category_icon_name = now.strftime('%Y%m%d%H%M%S') + '_' + file_rand_str_list[1] + '_' + selected_shop_category_icon.name
            fs = FileSystemStorage(location='templates/static/images/shop_category/')
            fs.save(name=new_unselected_shop_category_icon_name, content=unselected_shop_category_icon)
            fs.save(name=new_selected_shop_category_icon_name, content=selected_shop_category_icon)
            # 寫入資料庫
            models.Shop_Sub_Category.objects.create(
                shop_category_id=shop_category_id,
                c_shop_category=c_shop_category, 
                e_shop_category=e_shop_category, 
                unselected_shop_category_icon=new_unselected_shop_category_icon_name, 
                selected_shop_category_icon=new_selected_shop_category_icon_name, 
                # shop_category_background_color=shop_category_background_color,  
                shop_category_seq=shop_category_seq
                
            )
    return JsonResponse(response_data)