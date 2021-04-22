from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from hkshopu import models
import re
import datetime
import math
import uuid
import os
from utils.upload_tools import upload_file
# Create your views here.

# 新增商店頁面
def create(request):
    template = get_template('shop/create.html')
    html = template.render()
    return HttpResponse(html)

# 新增商店並新增選擇商店分類
def save(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'shop_id': ''
    }

    if request.method == 'POST':
        # 欄位資料
        userId = request.POST.get('user_id', '')
        shopIcon = request.FILES.get('shop_icon')
        shopTitle = request.POST.get('shop_title', '')
        shopCategoryId = request.POST.getlist('shop_category_id', '')
        shopPic = request.FILES.get('shop_pic')
        shopDesc = request.POST.get('shop_desc', '')
        paypal = request.POST.get('paypal', '')
        visa = request.POST.get('visa', '')
        master = request.POST.get('master', '')
        apple = request.POST.get('apple', '')
        android = request.POST.get('android', '')
        isShipFree = request.POST.get('is_ship_free', '')
        shipFreeQuota = request.POST.get('ship_free_quota', '')
        fixShipFee = request.POST.get('fix_ship_fee', '')
        fixShipFeeFr = request.POST.get('fix_ship_fee_fr', '')
        fixShipFeeTo = request.POST.get('fix_ship_fee_to', '')
        shipByProduct = request.POST.get('ship_by_product', '')
        discountByPercent = request.POST.get('discount_by_percent', '')
        discountByAmount = request.POST.get('discount_by_amount', '')
        bankCode = request.POST.get('bank_code', '')
        bankName = request.POST.get('bank_name', '')
        bankAccount = request.POST.get('bank_account', '')
        bankAccountName = request.POST.get('bank_account_name', '')
        addressName = request.POST.get('address_name', '')
        addressPhone = request.POST.get('address_phone', '')
        addressArea = request.POST.get('address_area', '')
        addressDistrict = request.POST.get('address_district', '')
        addressRoad = request.POST.get('address_road', '')
        addressNumber = request.POST.get('address_number', '')
        addressOther = request.POST.get('address_other', '')
        addressFloor = request.POST.get('address_floor', '')
        addressRoom = request.POST.get('address_room', '')
        # 新增 log
        shopCategoryIdParam = ''
        if shopCategoryId:
            shopCategoryIdList = []
            for value in shopCategoryId:
                shopCategoryIdList.append('shop_category_id=' + value)
            shopCategoryIdParam += '&'.join(shopCategoryIdList)
        else:
            shopCategoryIdParam += 'shop_category_id='
        models.Audit_Log.objects.create(
            id=uuid.uuid4(), 
            user_id=userId, 
            action='Create New Shop', 
            parameter_in='user_id=' + userId + '&shop_icon=' + str(shopIcon) + '&shop_title=' + shopTitle + '&' + shopCategoryIdParam, 
            parameter_out=''
        )
        # 檢查使用者是否登入
        if responseData['status'] == 0:
            if (not(userId) or userId==''):
                responseData['status'] = -1
                responseData['ret_val'] = '請先登入會員!'
        # 判斷必填欄位是否填寫及欄位格式是否正確
        if responseData['status'] == 0:
            if not(shopIcon):
                responseData['status'] = -2
                responseData['ret_val'] = '未上傳商店小圖!'

        if responseData['status'] == 0:
            if (not(shopTitle) or shopTitle==''):
                responseData['status'] = -3
                responseData['ret_val'] = '未填寫商店標題!'

        if responseData['status'] == 0:
            if (not(shopCategoryId) or shopCategoryId==''):
                responseData['status'] = -4
                responseData['ret_val'] = '未填寫商店分類編號!'

        if responseData['status'] == 0:
            if not(re.match('^.+\.(gif|png|jpg|jpeg)$', str(shopIcon.name))):
                responseData['status'] = -7
                responseData['ret_val'] = '商店小圖格式錯誤!'

        if responseData['status'] == 0:
            for value in shopCategoryId:
                if not(re.match('^\d+$', value)):
                    responseData['status'] = -8
                    responseData['ret_val'] = '商店分類格式錯誤!'
                    break

        # 選填欄位若有填寫，則判斷其格式是否正確
        if responseData['status'] == 0:
            if shopPic:
                if not(re.match('^.+\.(gif|png|jpg|jpeg)$', str(shopPic.name))):
                    responseData['status'] = -9
                    responseData['ret_val'] = '商店主圖格式錯誤!'
            elif (shopPic==''):
                shopPic = None

        if responseData['status'] == 0:
            if paypal:
                if not(re.match('^\w+$', paypal)):
                    responseData['status'] = -10
                    responseData['ret_val'] = 'PayPal 格式錯誤!'
            elif (paypal==''):
                paypal = None

        if responseData['status'] == 0:
            if visa:
                if not(re.match('^\w+$', visa)):
                    responseData['status'] = -11
                    responseData['ret_val'] = 'Visa 卡格式錯誤!'
            elif (visa==''):
                visa = None

        if responseData['status'] == 0:
            if master:
                if not(re.match('^\w+$', master)):
                    responseData['status'] = -12
                    responseData['ret_val'] = 'Master 卡格式錯誤!'
            elif (master==''):
                master = None

        if responseData['status'] == 0:
            if apple:
                if not(re.match('^\w+$', apple)):
                    responseData['status'] = -13
                    responseData['ret_val'] = 'Apple 格式錯誤!'
            elif (apple==''):
                apple = None

        if responseData['status'] == 0:
            if android:
                if not(re.match('^\w+$', android)):
                    responseData['status'] = -14
                    responseData['ret_val'] = 'Android 格式錯誤!'
            elif (shipByProduct==''):
                shipByProduct = None

        if responseData['status'] == 0:
            if isShipFree:
                if not(re.match('^\w+$', isShipFree)):
                    responseData['status'] = -15
                    responseData['ret_val'] = '是否免運費格式錯誤!'
            elif (isShipFree==''):
                isShipFree = None

        if responseData['status'] == 0:
            if shipFreeQuota:
                if not(re.match('^\d+$', shipFreeQuota)):
                    responseData['status'] = -16
                    responseData['ret_val'] = '免運費訂單價格格式錯誤!'
            elif (shipFreeQuota==''):
                shipFreeQuota = None
        if responseData['status'] == 0:
            if fixShipFee:
                if not(re.match('^\d+$', fixShipFee)):
                    responseData['status'] = -17
                    responseData['ret_val'] = '運費訂價格式錯誤!'
            elif (fixShipFee==''):
                fixShipFee = None

        if responseData['status'] == 0:
            if fixShipFeeFr:
                if not(re.match('^\d+$', fixShipFeeFr)):
                    responseData['status'] = -18
                    responseData['ret_val'] = '訂單價格由格式錯誤!'
            elif (fixShipFeeFr==''):
                fixShipFeeFr = None

        if responseData['status'] == 0:
            if fixShipFeeTo:
                if not(re.match('^\d+$', fixShipFeeTo)):
                    responseData['status'] = -19
                    responseData['ret_val'] = '訂單價格至格式錯誤!'
            elif (fixShipFeeTo==''):
                fixShipFeeTo = None

        if responseData['status'] == 0:
            if shipByProduct:
                if not(re.match('^\w+$', shipByProduct)):
                    responseData['status'] = -20
                    responseData['ret_val'] = '運費由商品設定格式錯誤!'
            elif (shipByProduct==''):
                shipByProduct = None

        if responseData['status'] == 0:
            if discountByPercent:
                if not(re.match('^\d+$', discountByPercent)):
                    responseData['status'] = -21
                    responseData['ret_val'] = '百分比折扣格式錯誤!'
            elif (discountByPercent==''):
                discountByPercent = None

        if responseData['status'] == 0:
            if discountByAmount:
                if not(re.match('^\d+$', discountByAmount)):
                    responseData['status'] = -22
                    responseData['ret_val'] = '價格折扣格式錯誤!'
            elif (discountByAmount==''):
                discountByAmount = None
        
        if responseData['status'] == 0:
            if bankCode:
                if not(re.match('^\d+$', bankCode)):
                    responseData['status'] = -23
                    responseData['ret_val'] = '銀行代碼格式錯誤!'
            elif (bankCode==''):
                bankCode = None
        
        if responseData['status'] == 0:
            if bankName:
                if not(re.match('^[\w\s]+$', bankName)):
                    responseData['status'] = -24
                    responseData['ret_val'] = '銀行名稱格式錯誤!'
            elif (bankName==''):
                bankName = None
        
        if responseData['status'] == 0:
            if bankAccountName:
                if not(re.match('^\w+$', bankAccountName)):
                    responseData['status'] = -25
                    responseData['ret_val'] = '銀行戶名格式錯誤!'
            elif (bankAccountName==''):
                bankAccountName = None
        
        if responseData['status'] == 0:
            if bankAccount:
                if not(re.match('^\d+$', bankAccount)):
                    responseData['status'] = -26
                    responseData['ret_val'] = '銀行帳號格式錯誤!'
            elif (bankAccount==''):
                bankAccount = None
        
        if responseData['status'] == 0:
            if addressName:
                if not(re.match('^[\w\s]+$', addressName)):
                    responseData['status'] = -27
                    responseData['ret_val'] = '姓名/公司名稱格式錯誤!'
            elif (addressName==''):
                addressName = None
        
        if responseData['status'] == 0:
            if addressPhone:
                if not(re.match('^\+\d+\s\d+$', addressPhone)):
                    responseData['status'] = -28
                    responseData['ret_val'] = '電話號碼格式錯誤!'
            elif (addressPhone==''):
                addressPhone = None
        
        if responseData['status'] == 0:
            if addressArea:
                if not(re.match('^\w+$', addressArea)):
                    responseData['status'] = -29
                    responseData['ret_val'] = '地域格式錯誤!'
            elif (addressArea==''):
                addressArea = None
        
        if responseData['status'] == 0:
            if addressDistrict:
                if not(re.match('^\w+$', addressDistrict)):
                    responseData['status'] = -30
                    responseData['ret_val'] = '地區格式錯誤!'
            elif (addressDistrict==''):
                addressDistrict = None
        
        if responseData['status'] == 0:
            if addressRoad:
                if not(re.match('^[\w\s+]+$', addressRoad)):
                    responseData['status'] = -31
                    responseData['ret_val'] = '街道名稱格式錯誤!'
            elif (addressRoad==''):
                addressRoad = None
        
        if responseData['status'] == 0:
            if addressNumber:
                if not(re.match('^\w+$', addressNumber)):
                    responseData['status'] = -32
                    responseData['ret_val'] = '街道門牌格式錯誤!'
            elif (addressNumber==''):
                addressNumber = None
        
        if responseData['status'] == 0:
            if addressOther:
                if not(re.match('^[\w\s]+$', addressOther)):
                    responseData['status'] = -33
                    responseData['ret_val'] = '其他地址格式錯誤!'
            elif (addressOther==''):
                addressOther = None
        
        if responseData['status'] == 0:
            if addressFloor:
                if not(re.match('^\w+$', addressFloor)):
                    responseData['status'] = -34
                    responseData['ret_val'] = '樓層格式錯誤!'
            elif (addressFloor==''):
                addressFloor = None
        
        if responseData['status'] == 0:
            if addressRoom:
                if not(re.match('^\w+$', addressRoom)):
                    responseData['status'] = -35
                    responseData['ret_val'] = '房(室)名稱格式錯誤!'
            elif (addressRoom==''):
                addressRoom = None

        
        # 檢查同一人是否重複新增同名的商店
        if responseData['status'] == 0:
            try:
                shop = models.Shop.objects.get(shop_title=shopTitle)
                responseData['status'] = -36
                responseData['ret_val'] = '此商店名稱已存在，請選擇其他名稱!'
            except:
                pass
        # 新增商店並移動圖檔到指定路徑
        if responseData['status'] == 0:
            # 上傳圖片
            destination_path = 'images/shop/'
            shopIconURL = upload_file(FILE=shopIcon,destination_path=destination_path,suffix='icon')
            shopPicURL = upload_file(FILE=shopPic,destination_path=destination_path,suffix='pic')
            # 新增商店
            models.Shop.objects.create(
                user_id=userId,  
                shop_title=shopTitle, 
                shop_icon=shopIconURL, 
                shop_pic=shopPicURL, 
                shop_description=shopDesc, 
                paypal=paypal, 
                visa=visa, 
                master=master, 
                apple=apple, 
                android=android, 
                is_ship_free=isShipFree, 
                ship_by_product=shipByProduct, 
                ship_free_quota=shipFreeQuota, 
                fix_ship_fee=fixShipFee, 
                fix_ship_fee_from=fixShipFeeFr, 
                fix_ship_fee_to=fixShipFeeTo, 
                discount_by_percent=discountByPercent, 
                discount_by_amount=discountByAmount,
                bank_code=bankCode,
                bank_name=bankName,
                bank_account=bankAccount,
                bank_account_name=bankAccountName,
                address_name=addressName,
                address_phone=addressPhone,
                address_area=addressArea,
                address_district=addressDistrict,
                address_road=addressRoad,
                address_number=addressNumber,
                address_other=addressOther,
                address_floor=addressFloor,
                address_room=addressRoom
            )
            # 取得當前商店編號
            shops = models.Shop.objects.order_by('-updated_at')
            responseData['shop_id'] = shops[0].id
            # 新增選擇商店分類
            to_delete_selected_shop_categories = models.Selected_Shop_Category.objects.filter(shop_id=shops[0].id).exclude(shop_category_id__in=shopCategoryId)
            if len(to_delete_selected_shop_categories) > 0:
                to_delete_selected_shop_categories.delete()

            for value in shopCategoryId:
                selected_shop_categories = models.Selected_Shop_Category.objects.filter(shop_id=shops[0].id, shop_category_id=value)
                if len(selected_shop_categories) == 0:
                    models.Selected_Shop_Category.objects.create(
                        shop_id=shops[0].id, 
                        shop_category_id=value
                    )
            responseData['ret_val'] = '商店與選擇商店分類新增成功!'
    return JsonResponse(responseData)
# 更新商店
def update(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        shopIcon = request.FILES.get('shop_icon', '')
        shopTitle = request.POST.get('shop_title', '')
        shopPic = request.FILES.get('shop_pic', '')
        shopDesc = request.POST.get('shop_desc', '')
        paypal = request.POST.get('paypal', '')
        visa = request.POST.get('visa', '')
        master = request.POST.get('master', '')
        apple = request.POST.get('apple', '')
        android = request.POST.get('android', '')
        isShipFree = request.POST.get('is_ship_free', '')
        shipFreeQuota = request.POST.get('ship_free_quota', '')
        fixShipFee = request.POST.get('fix_ship_fee', '')
        fixShipFeeFr = request.POST.get('fix_ship_fee_fr', '')
        fixShipFeeTo = request.POST.get('fix_ship_fee_to', '')
        shipByProduct = request.POST.get('ship_by_product', '')
        discountByPercent = request.POST.get('discount_by_percent', '')
        discountByAmount = request.POST.get('discount_by_amount', '')
        # 現在時間
        now = datetime.datetime.now()
        # FileSystemStorage
        fs = FileSystemStorage(location='templates/static/images/')
        # 檢查商店編號是否正確
        if responseData['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=id)
            except:
                responseData['status'] = -1
                responseData['ret_val'] = '找不到此商店編號的商店!'
        # 檢查使用者是否登入
        if responseData['status'] == 0:
            if not('user' in request.session):
                responseData['status'] = -2
                responseData['ret_val'] = '請先登入會員!'
        # 判斷必填欄位是否填寫及欄位格式是否正確
        if responseData['status'] == 0:
            if not(shopTitle):
                responseData['status'] = -3
                responseData['ret_val'] = '未填寫商店標題!'

        if responseData['status'] == 0:
            if not(shopDesc):
                responseData['status'] = -5
                responseData['ret_val'] = '未填寫商店描述!'
        # 選填欄位若有填寫，則判斷其格式是否正確
        if responseData['status'] == 0:
            if shopIcon:
                if not(re.match('^\w+\.(gif|png|jpg|jpeg)$', str(shopIcon.name))):
                    responseData['status'] = -7
                    responseData['ret_val'] = '商店小圖格式錯誤!'
                else:
                    shopIconName = str(shopIcon.name).split('.')[0]
                    shopIconExtension = str(shopIcon.name).split('.')[1]
                    shopIconFullName = shopIconName + '_' + now.strftime('%Y%m%d%H%M%S') + '_' + str(math.floor(now.timestamp())) + '.' + shopIconExtension
                    fs.save(name=shopIconFullName, content=shopIcon)
                    shop.shop_icon = shopIconFullName
                    shop.save()

        if responseData['status'] == 0:
            if shopPic:
                if not(re.match('^\w+\.(gif|png|jpg|jpeg)$', str(shopPic.name))):
                    responseData['status'] = -8
                    responseData['ret_val'] = '商店主圖格式錯誤!'
                else:
                    shopPicName = str(shopPic.name).split('.')[0]
                    shopPicExtension = str(shopPic.name).split('.')[1]
                    shopPicFullName = shopPicName + '_' + now.strftime('%Y%m%d%H%M%S') + '_' + str(math.floor(now.timestamp())) + '.' + shopPicExtension
                    fs.save(name=shopPicFullName, content=shopPic)
                    shop.shop_pic = shopPicFullName
                    shop.save()

        if responseData['status'] == 0:
            if paypal:
                if not(re.match('^\w+$', paypal)):
                    responseData['status'] = -9
                    responseData['ret_val'] = 'PayPal 格式錯誤!'

        if responseData['status'] == 0:
            if visa:
                if not(re.match('^\w+$', visa)):
                    responseData['status'] = -10
                    responseData['ret_val'] = 'Visa 卡格式錯誤!'

        if responseData['status'] == 0:
            if master:
                if not(re.match('^\w+$', master)):
                    responseData['status'] = -11
                    responseData['ret_val'] = 'Master 卡格式錯誤!'

        if responseData['status'] == 0:
            if apple:
                if not(re.match('^\w+$', apple)):
                    responseData['status'] = -12
                    responseData['ret_val'] = 'Apple 格式錯誤!'

        if responseData['status'] == 0:
            if android:
                if not(re.match('^\w+$', android)):
                    responseData['status'] = -13
                    responseData['ret_val'] = 'Android 格式錯誤!'

        if responseData['status'] == 0:
            if isShipFree:
                if not(re.match('^\w+$', isShipFree)):
                    responseData['status'] = -14
                    responseData['ret_val'] = '是否免運費格式錯誤!'

        if responseData['status'] == 0:
            if shipFreeQuota:
                if not(re.match('^\d+$', shipFreeQuota)):
                    responseData['status'] = -15
                    responseData['ret_val'] = '免運費訂單價格格式錯誤!'

        if responseData['status'] == 0:
            if fixShipFee:
                if not(re.match('^\d+$', fixShipFee)):
                    responseData['status'] = -16
                    responseData['ret_val'] = '運費訂價格式錯誤!'

        if responseData['status'] == 0:
            if fixShipFeeFr:
                if not(re.match('^\d+$', fixShipFeeFr)):
                    responseData['status'] = -17
                    responseData['ret_val'] = '訂單價格由格式錯誤!'

        if responseData['status'] == 0:
            if fixShipFeeTo:
                if not(re.match('^\d+$', fixShipFeeTo)):
                    responseData['status'] = -18
                    responseData['ret_val'] = '訂單價格至格式錯誤!'

        if responseData['status'] == 0:
            if shipByProduct:
                if not(re.match('^\w+$', shipByProduct)):
                    responseData['status'] = -19
                    responseData['ret_val'] = '運費由商品設定格式錯誤!'
        
        if responseData['status'] == 0:
            if not(discountByPercent) and not(discountByAmount):
                responseData['status'] = -20
                responseData['ret_val'] = '折扣欄位必須擇一填寫!'
            else:
                if discountByPercent:
                    if not(re.match('^\d+$', discountByPercent)):
                        responseData['status'] = -21
                        responseData['ret_val'] = '百分比折扣格式錯誤!'

                if discountByAmount:
                    if not(re.match('^\d+$', discountByAmount)):
                        responseData['status'] = -22
                        responseData['ret_val'] = '價格折扣格式錯誤!'
        # 先檢查使用者是否更改商店名稱，若有更改，則檢查是否更改名稱為其他同名的商店
        if responseData['status'] == 0:
            try:
                oldShop = models.Shop.objects.get(id=id, shop_title=shopTitle)
            except:
                sameNameShops = models.Shop.objects.filter(shop_title=shopTitle)
                if len(sameNameShops) > 0:
                    responseData['status'] = -23
                    responseData['ret_val'] = '此商店名稱已存在，請選擇其他名稱!'
        # 更新商店
        if responseData['status'] == 0:
            shop.shop_title = shopTitle
            shop.shop_description = shopDesc
            shop.paypal = paypal
            shop.visa = visa
            shop.master = master
            shop.apple = apple
            shop.android = android
            shop.is_ship_free = isShipFree
            shop.ship_by_product = shipByProduct
            shop.ship_free_quota = shipFreeQuota
            shop.fix_ship_fee = fixShipFee
            shop.fix_ship_fee_from = fixShipFeeFr
            shop.fix_ship_fee_to = fixShipFeeTo
            shop.save()
            responseData['ret_val'] = '商店更新成功!'
    return JsonResponse(responseData)
# 單一商店
def show(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'shop': {}
    }

    if request.method == 'GET':
        # 檢查商店編號是否正確
        if responseData['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=id)
                if (hasattr(shop, 'id')):
                    responseData['shop']['id'] = shop.id
                if (hasattr(shop, 'user_id')):
                    responseData['shop']['user_id'] = shop.user_id
                if (hasattr(shop, 'shop_title')):
                    responseData['shop']['shop_title'] = shop.shop_title
                if (hasattr(shop, 'shop_icon')):
                    responseData['shop']['shop_icon'] = shop.shop_icon
                if (hasattr(shop, 'shop_pic')):
                    responseData['shop']['shop_pic'] = shop.shop_pic
                if (hasattr(shop, 'shop_description')):
                    responseData['shop']['shop_description'] = shop.shop_description
                if (hasattr(shop, 'paypal')):
                    responseData['shop']['paypal'] = shop.paypal
                if (hasattr(shop, 'visa')):
                    responseData['shop']['visa'] = shop.visa
                if (hasattr(shop, 'master')):
                    responseData['shop']['master'] = shop.master
                if (hasattr(shop, 'apple')):
                    responseData['shop']['apple'] = shop.apple
                if (hasattr(shop, 'android')):
                    responseData['shop']['android'] = shop.android
                if (hasattr(shop, 'is_ship_free')):
                    responseData['shop']['is_ship_free'] = shop.is_ship_free
                if (hasattr(shop, 'ship_by_product')):
                    responseData['shop']['ship_by_product'] = shop.ship_by_product
                if (hasattr(shop, 'ship_free_quota')):
                    responseData['shop']['ship_free_quota'] = shop.ship_free_quota
                if (hasattr(shop, 'fix_ship_fee')):
                    responseData['shop']['fix_ship_fee'] = shop.fix_ship_fee
                if (hasattr(shop, 'fix_ship_fee_from')):
                    responseData['shop']['fix_ship_fee_from'] = shop.fix_ship_fee_from
                if (hasattr(shop, 'fix_ship_fee_to')):
                    responseData['shop']['fix_ship_fee_to'] = shop.fix_ship_fee_to
                if (hasattr(shop, 'transaction_method')):
                    responseData['shop']['transaction_method'] = shop.transaction_method
                if (hasattr(shop, 'transport_setting')):
                    responseData['shop']['transport_setting'] = shop.transport_setting
                if (hasattr(shop, 'created_at')):
                    responseData['shop']['created_at'] = shop.created_at
                if (hasattr(shop, 'updated_at')):
                    responseData['shop']['updated_at'] = shop.updated_at
                responseData['ret_val'] = '已找到商店資料!'
            except:
                responseData['status'] = 1
                responseData['ret_val'] = '找不到此商店編號的商店!'
    return JsonResponse(responseData)
# 確認商店名稱是否重複
def checkShopNameIsExistsProcess(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        shop_title = request.POST.get('shop_title', '')

        if response_data['status'] == 0:
            shops = models.Shop.objects.filter(shop_title=shop_title)
            if len(shops) > 0:
                response_data['status'] = -1
                response_data['ret_val'] = '已存在相同名稱的商店!'

        if response_data['status'] == 0:
            response_data['ret_val'] = '商店名稱未重複!'
    return JsonResponse(response_data)
