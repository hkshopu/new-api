from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.core.files.storage import FileSystemStorage
import mysql.connector
import datetime
import re

# Create your views here.

# 新增商店頁面
def create(request):
    template = get_template('shop/create.html')
    html = template.render()
    return HttpResponse(html)

# 新增商店
def createProcess(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }

    if request.method == 'POST':
        # 欄位資料
        shopIcon = request.FILES.get('shop_icon', '')
        shopTitle = request.POST.get('shop_title', '')
        shopCategoryId = request.POST.get('shop_category_id', 0)
        shopPic = request.FILES.get('shop_pic', '')
        shopDesc = request.POST.get('shop_desc', '')
        paypal = request.POST.get('paypal', '')
        visa = request.POST.get('visa', '')
        master = request.POST.get('master', '')
        apple = request.POST.get('apple', '')
        android = request.POST.get('android', '')
        isShipFree = request.POST.get('is_ship_free', '')
        shipFreeQuota = request.POST.get('ship_free_quota', 0)
        fixShipFee = request.POST.get('fix_ship_fee', 0)
        fixShipFeeFr = request.POST.get('fix_ship_fee_fr', 0)
        fixShipFeeTo = request.POST.get('fix_ship_fee_to', 0)
        shipByProduct = request.POST.get('ship_by_product', '')
        # 欲寫入資料庫之欄位
        insertColumns = [
            '`user_id`', 
            '`shop_icon`', 
            '`shop_title`', 
            '`shop_category_id`', 
            '`shop_pic`', 
            '`shop_desc`'
        ]
        # 檢查使用者是否登入
        if responseData['status'] == 0:
            if not('user' in request.session):
                responseData['status'] = -1
                responseData['ret_val'] = '請先登入會員!'
        # 判斷必填欄位是否填寫及欄位格式是否正確
        if responseData['status'] == 0:
            if not(shopIcon):
                responseData['status'] = -2
                responseData['ret_val'] = '未上傳商店小圖!'

        if responseData['status'] == 0:
            if not(shopTitle):
                responseData['status'] = -3
                responseData['ret_val'] = '未填寫商店標題!'

        if responseData['status'] == 0:
            if not(shopCategoryId):
                responseData['status'] = -4
                responseData['ret_val'] = '未選擇商店類別!'

        if responseData['status'] == 0:
            if not(shopPic):
                responseData['status'] = -5
                responseData['ret_val'] = '未上傳商店主圖!'

        if responseData['status'] == 0:
            if not(shopDesc):
                responseData['status'] = -6
                responseData['ret_val'] = '未填寫商店描述!'

        if responseData['status'] == 0:
            if not(re.match('^\w+\.(gif|png|jpg|jpeg)$', str(shopIcon.name))):
                responseData['status'] = -7
                responseData['ret_val'] = '商店小圖格式錯誤!'

        if responseData['status'] == 0:
            if not(re.match('^\d+$', shopCategoryId)):
                responseData['status'] = -8
                responseData['ret_val'] = '商店分類格式錯誤!'

        if responseData['status'] == 0:
            if not(re.match('^\w+\.(gif|png|jpg|jpeg)$', str(shopPic.name))):
                responseData['status'] = -9
                responseData['ret_val'] = '商店主圖格式錯誤!'
        # 判斷選填欄位若有填寫，則其格式是否正確
        if responseData['status'] == 0:
            if paypal:
                if not(re.match('^\w+$', paypal)):
                    responseData['status'] = -10
                    responseData['ret_val'] = 'PayPal 格式錯誤!'
                else:
                    insertColumns.append('`paypal`')

        if responseData['status'] == 0:
            if visa:
                if not(re.match('^\w+$', visa)):
                    responseData['status'] = -11
                    responseData['ret_val'] = 'Visa 卡格式錯誤!'
                else:
                    insertColumns.append('`visa`')

        if responseData['status'] == 0:
            if master:
                if not(re.match('^\w+$', master)):
                    responseData['status'] = -12
                    responseData['ret_val'] = 'Master 卡格式錯誤!'
                else:
                    insertColumns.append('`master`')

        if responseData['status'] == 0:
            if apple:
                if not(re.match('^\w+$', apple)):
                    responseData['status'] = -13
                    responseData['ret_val'] = 'Apple 格式錯誤!'
                else:
                    insertColumns.append('`apple`')

        if responseData['status'] == 0:
            if android:
                if not(re.match('^\w+$', android)):
                    responseData['status'] = -14
                    responseData['ret_val'] = 'Android 格式錯誤!'
                else:
                    insertColumns.append('`android`')

        if responseData['status'] == 0:
            if isShipFree:
                if not(re.match('^\w+$', isShipFree)):
                    responseData['status'] = -15
                    responseData['ret_val'] = '是否免運費格式錯誤!'
                else:
                    insertColumns.append('`is_ship_free`')

        if responseData['status'] == 0:
            if shipFreeQuota:
                if not(re.match('^\d+$', shipFreeQuota)):
                    responseData['status'] = -16
                    responseData['ret_val'] = '免運費訂單價格格式錯誤!'
                else:
                    insertColumns.append('`ship_free_quota`')

        if responseData['status'] == 0:
            if fixShipFee:
                if not(re.match('^\d+$', fixShipFee)):
                    responseData['status'] = -17
                    responseData['ret_val'] = '運費訂價格式錯誤!'
                else:
                    insertColumns.append('`fix_ship_fee`')

        if responseData['status'] == 0:
            if fixShipFeeFr:
                if not(re.match('^\d+$', fixShipFeeFr)):
                    responseData['status'] = -18
                    responseData['ret_val'] = '訂單價格由格式錯誤!'
                else:
                    insertColumns.append('`fix_ship_fee_fr`')

        if responseData['status'] == 0:
            if fixShipFeeTo:
                if not(re.match('^\d+$', fixShipFeeTo)):
                    responseData['status'] = -19
                    responseData['ret_val'] = '訂單價格至格式錯誤!'
                else:
                    insertColumns.append('`fix_ship_fee_to`')

        if responseData['status'] == 0:
            if shipByProduct:
                if not(re.match('^\w+$', shipByProduct)):
                    responseData['status'] = -20
                    responseData['ret_val'] = '運費由商品設定格式錯誤!'
                else:
                    insertColumns.append('`ship_by_product`')
        # 檢查同一人是否重複新增同名的商店
        if responseData['status'] == 0:
            conn = mysql.connector.connect(
                host='localhost', 
                user='root', 
                password='32753715', 
                database='store'
            )
            cursor = conn.cursor(buffered=True)
            query = 'select * from `hkshopu_shop` where  `shop_title` = %s limit 1'
            values = (shopTitle, )
            cursor.execute(query, values)
            if cursor.rowcount > 0:
                responseData['status'] = -21
                responseData['ret_val'] = '此商店名稱已存在，請選擇其他名稱!'
        # 新增商店並移動圖檔到指定路徑
        if responseData['status'] == 0:
            now = datetime.datetime.now()
            # shop_icon
            shopIconName = str(shopIcon.name).split('.')[0]
            shopIconExtension = str(shopIcon.name).split('.')[1]
            shopIconFullName = shopIconName + '_' + now.strftime('%Y%m%d%H%M%S') + '_' + str(round(now.timestamp())) + '.' + shopIconExtension
            # shop_pic
            shopPicName = str(shopPic.name).split('.')[0]
            shopPicExtension = str(shopPic.name).split('.')[1]
            shopPicFullName = shopPicName + '_' + now.strftime('%Y%m%d%H%M%S') + '_' + str(round(now.timestamp())) + '.' + shopPicExtension
            # 移動圖檔到指定路徑
            fs = FileSystemStorage(location='templates/static/images/')
            fs.save(name=shopIconFullName, content=shopIcon)
            fs.save(name=shopPicFullName, content=shopPic)
            # 新增商店
            query = 'insert into `hkshopu_shop` (' + ','.join(insertColumns) + ') values (%s, %s, %s, %s, %s, %s)'
            values = (request.session['user']['id'], shopIconFullName, shopTitle, shopCategoryId, shopPicFullName, shopDesc)
            cursor.execute(query, values)
            conn.commit()
            responseData['ret_val'] = '商店新增成功!'
    return JsonResponse(responseData)