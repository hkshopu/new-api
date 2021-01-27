from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from hkshopu import models
import re
import datetime
import math

# Create your views here.

# 新增產品圖片
def save(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': ''
    }

    if request.method == 'POST':
        # 欄位資料
        product_id = request.POST.get('product_id', '')
        product_pic = request.FILES.get('product_pic', '')

        if response_data['status'] == 0:
            if not(product_id):
                response_data['status'] = -1
                response_data['ret_val'] = '未填寫產品編號!'

        if response_data['status'] == 0:
            if not(product_pic):
                response_data['status'] = -2
                response_data['ret_val'] = '未上傳產品圖片!'

        if response_data['status'] == 0:
            if not(re.match('^\d+$', product_id)):
                response_data['status'] = -3
                response_data['ret_val'] = '產品編號格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^\w+\.(gif|png|jpg|jpeg)$', str(product_pic))):
                response_data['status'] = -4
                response_data['ret_val'] = '產品圖片格式錯誤!'

        if response_data['status'] == 0:
            # 自訂圖片檔名
            now = datetime.datetime.now()
            product_pic_name = str(product_pic.name).split('.')[0]
            product_pic_extension = str(product_pic.name).split('.')[1]
            product_pic_fullname = product_pic_name + '_' + now.strftime('%Y%m%d%H%M%S') + '_' + str(math.floor(now.timestamp())) + '.' + product_pic_extension
            # 上傳圖片檔案
            fs = FileSystemStorage(location='templates/static/images/')
            fs.save(name=product_pic_fullname, content=product_pic)
            # 寫入資料庫
            models.Selected_Product_Pic.objects.create(
                product_id=product_id, 
                product_pic=product_pic_fullname
            )
            response_data['ret_val'] = '新增產品圖片成功!'
    return JsonResponse(response_data)