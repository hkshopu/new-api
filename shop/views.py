from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from django.template.loader import get_template
from django.db.models import Q
from django.db.models import Avg
from django.db.models import Sum
from django.db import transaction
from django.core.files.storage import FileSystemStorage
from hkshopu import models
import re
import datetime
import math
import uuid
import os
from utils.upload_tools import upload_file
from utils.upload_tools import delete_file
import json
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
        addressCountryCode = request.POST.get('address_country_code', '')
        addressPhone = request.POST.get('address_phone', '')
        addressIsPhoneShow = request.POST.get('address_is_phone_show', '')
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
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('user_id',-1,userId)
        # 判斷必填欄位是否填寫及欄位格式是否正確
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('shop_icon',-2,shopIcon)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('shop_title',-3,shopTitle)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Selected_Shop_Category.validate_column('shop_category_id',-4,shopCategoryId)

        # 選填欄位若有填寫，則判斷其格式是否正確        
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('shop_pic',-9,shopPic)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('paypal',-10,paypal)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('visa',-11,visa)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('master',-12,master)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('apple',-13,apple)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('android',-14,android)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('is_ship_free',-15,isShipFree)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('ship_free_quota',-16,shipFreeQuota)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('fix_ship_fee',-17,fixShipFee)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('fix_ship_fee_from',-18,fixShipFeeFr)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('fix_ship_fee_to',-19,fixShipFeeTo)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('ship_by_product',-20,shipByProduct)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('discount_by_percent',-21,discountByPercent)
        if responseData['status'] == 0: 
            responseData['status'],responseData['ret_val'] = models.Shop.validate_column('discount_by_amount',-22,discountByAmount)
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Bank_Account.validate_column('code',-23,bankCode)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Bank_Account.validate_column('name',-24,bankName)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Bank_Account.validate_column('account_name',-25,bankAccountName)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Bank_Account.validate_column('account',-26,bankAccount)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Address.validate_column('name',-27,addressName)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Address.validate_column('phone',-28,addressPhone)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Address.validate_column('area',-29,addressArea)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Address.validate_column('district',-30,addressDistrict)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Address.validate_column('road',-31,addressRoad)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Address.validate_column('number',-32,addressNumber)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Address.validate_column('other',-33,addressOther)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Address.validate_column('floor',-34,addressFloor)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Address.validate_column('room',-35,addressRoom)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Address.validate_column('country_code',-36,addressCountryCode)
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.Shop_Address.validate_column('is_phone_show',-37,addressIsPhoneShow)
        
        # 檢查同一人是否重複新增同名的商店
        if responseData['status'] == 0:
            try:
                shop = models.Shop.objects.get(shop_title=shopTitle,is_delete='N')
                responseData['status'] = -99
                responseData['ret_val'] = '此商店名稱已存在，請選擇其他名稱!'
            except:
                pass
        # 將空字串轉成0或預設值
        if isShipFree is '':
            isShipFree = None
        if shipByProduct is '':
            shipByProduct = None
        if addressIsPhoneShow is '':
            addressIsPhoneShow = None
        if shipFreeQuota is '':
            shipFreeQuota = 0
        if fixShipFee is '':
            fixShipFee = 0
        if fixShipFeeFr is '':
            fixShipFeeFr = 0
        if fixShipFeeTo is '':
            fixShipFeeTo = 0
        if discountByPercent is '':
            discountByPercent = 0
        if discountByAmount is '':
            discountByAmount = 0
        # 新增商店並移動圖檔到指定路徑
        if responseData['status'] == 0:
            # 上傳圖片
            destination_path = 'images/shop/'
            shopIconURL = upload_file(FILE=shopIcon,destination_path=destination_path,suffix='icon')
            shopPicURL = upload_file(FILE=shopPic,destination_path=destination_path,suffix='pic')
            with transaction.atomic():
                # This code executes inside a transaction.
                # 新增商店
                new_shop = models.Shop.objects.create(
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
                    discount_by_amount=discountByAmount
                )
                # 新增商店地址
                models.Shop_Address.objects.create(
                    id = uuid.uuid4(),
                    shop_id = new_shop.id,
                    name = addressName,
                    country_code = addressCountryCode,
                    phone = addressPhone,
                    is_phone_show = addressIsPhoneShow,
                    area = addressArea,
                    district = addressDistrict,
                    road = addressRoad,
                    number = addressNumber,
                    other = addressOther,
                    floor = addressFloor,
                    room = addressRoom
                )
                # 新增商店銀行帳號
                models.Shop_Bank_Account.objects.create(
                    id = uuid.uuid4(),
                    shop_id = new_shop.id,
                    code = bankCode,
                    name = bankName,
                    account = bankAccount,
                    account_name = bankAccountName
                )
                # 取得當前商店編號
                responseData['shop_id'] = new_shop.id
                # 新增選擇商店分類
                to_delete_selected_shop_categories = models.Selected_Shop_Category.objects.filter(shop_id=new_shop.id).exclude(shop_category_id__in=shopCategoryId)
                if len(to_delete_selected_shop_categories) > 0:
                    to_delete_selected_shop_categories.delete()

                for value in shopCategoryId:
                    selected_shop_categories = models.Selected_Shop_Category.objects.filter(shop_id=new_shop.id, shop_category_id=value)
                    if (len(selected_shop_categories) == 0 and value != 0):
                        models.Selected_Shop_Category.objects.create(
                            shop_id=new_shop.id,
                            shop_category_id=value
                        )
                # 取得預設運輸方法
                shipment_default_methods = models.Shipment_default_method.objects.all()
                # 新增商店運輸設定
                for shipment_default_method in shipment_default_methods:
                    models.Shop_Shipment_Setting.objects.create(
                        shop_id=new_shop.id, 
                        shipment_desc=shipment_default_method.shipment_default_desc, 
                        onoff=shipment_default_method.onoff
                    )
            responseData['ret_val'] = '商店與選擇商店分類新增成功!'
    return JsonResponse(responseData)
# 更新商店
def update(request, id):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        shop_icon = request.FILES.get('shop_icon', None)
        shop_title = request.POST.get('shop_title', None)
        # shop_category_id = request.POST.getlist('shop_category_id', None)
        shop_pic = request.FILES.get('shop_pic', None)
        shop_description = request.POST.get('shop_description', None)
        paypal = request.POST.get('paypal', None)
        visa = request.POST.get('visa', None)
        master = request.POST.get('master', None)
        apple = request.POST.get('apple', None)
        android = request.POST.get('android', None)
        is_ship_free = request.POST.get('is_ship_free', None)
        ship_by_product = request.POST.get('ship_by_product', None)
        ship_free_quota = request.POST.get('ship_free_quota', None)
        fix_ship_fee = request.POST.get('fix_ship_fee', None)
        fix_ship_fee_from = request.POST.get('fix_ship_fee_from', None)
        fix_ship_fee_to = request.POST.get('fix_ship_fee_to', None)
        transaction_method = request.POST.get('transaction_method', None)
        transport_setting = request.POST.get('transport_setting', None)
        discount_by_amount = request.POST.get('discount_by_amount', None)
        discount_by_percent = request.POST.get('discount_by_percent', None)
        address_id = request.POST.get('address_id', None)
        address_name = request.POST.get('address_name', None)
        address_country_code = request.POST.get('address_country_code', None)
        address_phone = request.POST.get('address_phone', None)
        address_is_phone_show = request.POST.get('address_is_phone_show', None)
        address_area = request.POST.get('address_area', None)
        address_district = request.POST.get('address_district', None)
        address_road = request.POST.get('address_road', None)
        address_number = request.POST.get('address_number', None)
        address_other = request.POST.get('address_other', None)
        address_floor = request.POST.get('address_floor', None)
        address_room = request.POST.get('address_room', None)
        background_pic = request.FILES.get('background_pic', None)
        shop_phone = request.POST.get('shop_phone', None)
        shop_is_phone_show = request.POST.get('shop_is_phone_show', None)
        shop_email = request.POST.get('shop_email', None)
        email_on = request.POST.get('email_on', None)
        long_description = request.POST.get('long_description', None)
        facebook_on = request.POST.get('facebook_on', None)
        instagram_on = request.POST.get('instagram_on', None)

        if response_data['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=id,is_delete='N')
            except:
                response_data['status'] = -1
                response_data['ret_val'] = '找不到此商店編號的商店!'

        if response_data['status'] == 0:
            if not(address_id):
                if address_name or address_country_code or address_phone or address_is_phone_show or address_area or address_district or address_road or address_number or address_other or address_floor or address_room:
                    response_data['status'] = -2
                    response_data['ret_val'] = '未填寫商店地址編號!'

        if response_data['status'] == 0:
            if address_id:
                try:
                    shop_address = models.Shop_Address.objects.get(id=address_id)
                except:
                    response_data['status'] = -3
                    response_data['ret_val'] = '找不到此商店地址編號的地址!'

        if response_data['status'] == 0:
            if shop_title == '':
                response_data['status'] = -6
                response_data['ret_val'] = '商店標題不可為空!'

        if response_data['status'] == 0:
            if shop_icon:
                if not(re.match('^.+\.(gif|png|jpg|jpeg)$', str(shop_icon.name))):
                    response_data['status'] = -7
                    response_data['ret_val'] = '商店小圖格式錯誤!'

        # if response_data['status'] == 0:
        #     if shop_category_id:
        #         for value in shop_category_id:
        #             if not(re.match('^\d+$', value)):
        #                 response_data['status'] = -8
        #                 response_data['ret_val'] = '商店分類編號格式錯誤!'
        #                 break

        if response_data['status'] == 0:
            if shop_pic:
                if not(re.match('^.+\.(gif|png|jpg|jpeg)$', str(shop_pic.name))):
                    response_data['status'] = -9
                    response_data['ret_val'] = '商店主圖格式錯誤!'

        if response_data['status'] == 0:
            if paypal:
                if not(re.match('^\w+$', paypal)):
                    response_data['status'] = -10
                    response_data['ret_val'] = 'PayPal 格式錯誤!'

        if response_data['status'] == 0:
            if visa:
                if not(re.match('^\w+$', visa)):
                    response_data['status'] = -11
                    response_data['ret_val'] = 'Visa 格式錯誤!'

        if response_data['status'] == 0:
            if master:
                if not(re.match('^\w+$', master)):
                    response_data['status'] = -12
                    response_data['ret_val'] = 'Master 格式錯誤!'

        if response_data['status'] == 0:
            if apple:
                if not(re.match('^\w+$', apple)):
                    response_data['status'] = -13
                    response_data['ret_val'] = 'Apple 格式錯誤!'

        if response_data['status'] == 0:
            if android:
                if not(re.match('^\w+$', android)):
                    response_data['status'] = -14
                    response_data['ret_val'] = 'Android 格式錯誤!'

        if response_data['status'] == 0:
            if is_ship_free:
                if not(re.match('^(Y|N)$', is_ship_free)):
                    response_data['status'] = -15
                    response_data['ret_val'] = '是否免運費格式錯誤!'

        if response_data['status'] == 0:
            if ship_by_product:
                if not(re.match('^(Y|N)$', ship_by_product)):
                    response_data['status'] = -16
                    response_data['ret_val'] = '運費由商品設定格式錯誤!'

        if response_data['status'] == 0:
            if ship_free_quota:
                if not(re.match('^\d+$', ship_free_quota)):
                    response_data['status'] = -17
                    response_data['ret_val'] = '免運費訂單價格格式錯誤!'

        if response_data['status'] == 0:
            if fix_ship_fee:
                if not(re.match('^\d+$', fix_ship_fee)):
                    response_data['status'] = -18
                    response_data['ret_val'] = '運費訂價格式錯誤!'

        if response_data['status'] == 0:
            if fix_ship_fee_from:
                if not(re.match('^\d+$', fix_ship_fee_from)):
                    response_data['status'] = -19
                    response_data['ret_val'] = '訂單價格由格式錯誤!'

        if response_data['status'] == 0:
            if fix_ship_fee_to:
                if not(re.match('^\d+$', fix_ship_fee_to)):
                    response_data['status'] = -20
                    response_data['ret_val'] = '訂單價格至格式錯誤!'

        if response_data['status'] == 0:
            if discount_by_amount:
                if not(re.match('^\d+$', discount_by_amount)):
                    response_data['status'] = -21
                    response_data['ret_val'] = '價格折扣格式錯誤!'

        if response_data['status'] == 0:
            if discount_by_percent:
                if not(re.match('^\d+$', discount_by_percent)):
                    response_data['status'] = -22
                    response_data['ret_val'] = '百分比折扣格式錯誤!'

        if response_data['status'] == 0:
            if address_name:
                if not(re.match('^[!@.#$%)(^&*\+\-\w\s]+$', address_name)):
                    response_data['status'] = -27
                    response_data['ret_val'] = '姓名/公司名稱格式錯誤!'

        if response_data['status'] == 0:
            if address_country_code:
                if not(re.match('^[0-9]{3}$', address_country_code)):
                    response_data['status'] = -28
                    response_data['ret_val'] = '國碼格式錯誤!'

        if response_data['status'] == 0:
            if address_phone:
                if not(re.match('^\d+$', address_phone)):
                    response_data['status'] = -29
                    response_data['ret_val'] = '電話號碼格式錯誤!'

        if response_data['status'] == 0:
            if address_is_phone_show:
                if not(re.match('^\w+$', address_is_phone_show)):
                    response_data['status'] = -30
                    response_data['ret_val'] = '顯示在店鋪簡介格式錯誤!'

        if response_data['status'] == 0:
            if address_area:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', address_area)):
                    response_data['status'] = -31
                    response_data['ret_val'] = '地域格式錯誤!'

        if response_data['status'] == 0:
            if address_district:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', address_district)):
                    response_data['status'] = -32
                    response_data['ret_val'] = '地區格式錯誤!'

        if response_data['status'] == 0:
            if address_road:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', address_road)):
                    response_data['status'] = -33
                    response_data['ret_val'] = '街道名稱格式錯誤!'

        if response_data['status'] == 0:
            if address_number:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', address_number)):
                    response_data['status'] = -34
                    response_data['ret_val'] = '街道門牌格式錯誤!'

        if response_data['status'] == 0:
            if address_other:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', address_other)):
                    response_data['status'] = -35
                    response_data['ret_val'] = '其他地址格式錯誤!'

        if response_data['status'] == 0:
            if address_floor:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', address_floor)):
                    response_data['status'] = -36
                    response_data['ret_val'] = '樓層格式錯誤!'

        if response_data['status'] == 0:
            if address_room:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', address_room)):
                    response_data['status'] = -37
                    response_data['ret_val'] = '房(室)名稱格式錯誤!'

        if response_data['status'] == 0:
            if background_pic:
                if not(re.match('^.+\.(gif|png|jpg|jpeg)$', str(background_pic.name))):
                    response_data['status'] = -38
                    response_data['ret_val'] = '背景圖片格式錯誤!'

        if response_data['status'] == 0:
            if shop_email:
                if not(re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', shop_email)):
                    response_data['status'] = -39
                    response_data['ret_val'] = '商店電子郵件格式錯誤!'

        if response_data['status'] == 0:
            if email_on:
                if not(re.match('^(Y|N)$', email_on)):
                    response_data['status'] = -40
                    response_data['ret_val'] = '電子郵件開啟設定格式錯誤!'

        if response_data['status'] == 0:
            if facebook_on:
                if not(re.match('^(Y|N)$', facebook_on)):
                    response_data['status'] = -41
                    response_data['ret_val'] = 'Facebook 開啟設定格式錯誤!'

        if response_data['status'] == 0:
            if instagram_on:
                if not(re.match('^(Y|N)$', instagram_on)):
                    response_data['status'] = -42
                    response_data['ret_val'] = 'Instagram 開啟設定格式錯誤!'

        if response_data['status'] == 0:
            if shop_title:
                if shop.shop_name_updated_at:
                    now = datetime.datetime.now()
                    if (now - shop.shop_name_updated_at).days < 30:
                        response_data['status'] = -43
                        response_data['ret_val'] = '過去 30 天內已更改過商店名稱!'

        if response_data['status'] == 0:
            shops = models.Shop.objects.filter(shop_title=shop_title,is_delete='N')
            if len(shops) > 0:
                response_data['status'] = -44
                response_data['ret_val'] = '此商店名稱已存在，請選擇其他名稱!'

        if response_data['status'] == 0:
            if shop_phone:
                if not(re.match('^\d+$', shop_phone)):
                    response_data['status'] = -29
                    response_data['ret_val'] = '電話號碼格式錯誤!'

        if response_data['status'] == 0:
            # 上傳圖檔
            destination_path = 'images/shop/'
            shop_icon_url = ''
            shop_pic_url = ''
            background_pic_url = ''
            if shop_icon:
                shop_icon_url += upload_file(FILE=shop_icon, destination_path=destination_path, suffix='icon')
            if shop_pic:
                shop_pic_url += upload_file(FILE=shop_pic, destination_path=destination_path, suffix='pic')
            if background_pic:
                background_pic_url += upload_file(FILE=background_pic, destination_path=destination_path, suffix='background_pic')
            # 更新商店
            if shop_title is not None:
                if shop_title != shop.shop_title:
                    shop.shop_title = shop_title
            if shop_icon is not None:
                if shop_icon_url != shop.shop_icon:
                    shop.shop_icon = shop_icon_url
            if shop_pic is not None:
                if shop_pic_url != shop.shop_pic:
                    shop.shop_pic = shop_pic_url
            if shop_description is not None:
                if shop_description != shop.shop_description:
                    shop.shop_description = shop_description
            if paypal is not None:
                if paypal != shop.paypal:
                    shop.paypal = paypal
            if visa is not None:
                if visa != shop.visa:
                    shop.visa = visa
            if master is not None:
                if master != shop.master:
                    shop.master = master
            if apple is not None:
                if apple != shop.apple:
                    shop.apple = apple
            if android is not None:
                if android != shop.android:
                    shop.android = android
            if is_ship_free is not None:
                if is_ship_free != shop.is_ship_free:
                    shop.is_ship_free = is_ship_free
            if ship_by_product is not None:
                if ship_by_product != shop.ship_by_product:
                    shop.ship_by_product = ship_by_product
            if ship_free_quota is not None:
                if ship_free_quota != shop.ship_free_quota:
                    shop.ship_free_quota = ship_free_quota
            if fix_ship_fee is not None:
                if fix_ship_fee != shop.fix_ship_fee:
                    shop.fix_ship_fee = fix_ship_fee
            if fix_ship_fee_from is not None:
                if fix_ship_fee_from != shop.fix_ship_fee_from:
                    shop.fix_ship_fee_from = fix_ship_fee_from
            if fix_ship_fee_to is not None:
                if fix_ship_fee_to != shop.fix_ship_fee_to:
                    shop.fix_ship_fee_to = fix_ship_fee_to
            if transaction_method is not None:
                if transaction_method != shop.transaction_method:
                    shop.transaction_method = transaction_method
            if transport_setting is not None:
                if transport_setting != shop.transport_setting:
                    shop.transport_setting = transport_setting
            if discount_by_amount is not None:
                if discount_by_amount != shop.discount_by_amount:
                    shop.discount_by_amount = discount_by_amount
            if discount_by_percent is not None:
                if discount_by_percent != shop.discount_by_percent:
                    shop.discount_by_percent = discount_by_percent
            if address_name is not None:
                if address_name != shop_address.name:
                    shop_address.name = address_name
            if address_country_code is not None:
                if address_country_code != shop_address.country_code:
                    shop_address.country_code = address_country_code
            if address_phone is not None:
                if address_phone != shop_address.phone:
                    shop_address.phone = address_phone
            if address_is_phone_show is not None:
                if address_is_phone_show != shop_address.is_phone_show:
                    shop_address.is_phone_show = address_is_phone_show
            if address_area is not None:
                if address_area != shop_address.area:
                    shop_address.area = address_area
            if address_district is not None:
                if address_district != shop_address.district:
                    shop_address.district = address_district
            if address_road is not None:
                if address_road != shop_address.road:
                    shop_address.road = address_road
            if address_number is not None:
                if address_number != shop_address.number:
                    shop_address.number = address_number
            if address_other is not None:
                if address_other != shop_address.other:
                    shop_address.other = address_other
            if address_floor is not None:
                if address_floor != shop_address.floor:
                    shop_address.floor = address_floor
            if address_room is not None:
                if address_room != shop_address.room:
                    shop_address.room = address_room
            if background_pic is not None:
                if background_pic_url != shop.background_pic:
                    shop.background_pic = background_pic_url
            if shop_phone is not None:
                if shop_phone != shop.address_phone:
                    shop.address_phone = shop_phone
            if shop_is_phone_show is not None:
                if shop_is_phone_show != shop.address_is_phone_show:
                    shop.address_is_phone_show = shop_is_phone_show
            if shop_email is not None:
                if shop_email != shop.shop_email:
                    shop.shop_email = shop_email
            if email_on is not None:
                if email_on != shop.email_on:
                    shop.email_on = email_on
            if long_description is not None:
                if long_description != shop.long_description:
                    description = str(long_description).split('\n')
                    shop.long_description = long_description
                    if len(description) == 1:
                        shop.shop_description = description[0]
                    else:
                        shop.shop_description = description[0] + '\n' + description[1]
            if facebook_on is not None:
                if facebook_on != shop.facebook_on:
                    shop.facebook_on = facebook_on
            if instagram_on is not None:
                if instagram_on != shop.instagram_on:
                    shop.instagram_on = instagram_on
            shop.save()
            if address_id:
                shop_address.save()
            # 更新選擇商店分類
            # to_delete_selected_shop_categories = models.Selected_Shop_Category.objects.filter(shop_id=id).exclude(shop_category_id__in=shop_category_id)
            # if len(to_delete_selected_shop_categories) > 0:
            #     to_delete_selected_shop_categories.delete()

            # for value in shop_category_id:
            #     selected_shop_categories = models.Selected_Shop_Category.objects.filter(shop_id=id, shop_category_id=value)
            #     if len(selected_shop_categories) == 0:
            #         models.Selected_Shop_Category.objects.create(
            #             shop_id=id,
            #             shop_category_id=value
            #         )
            response_data['ret_val'] = '商店更新成功!'
    return JsonResponse(response_data)
# 單一商店
def show(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': {}
    }

    if request.method == 'GET':
        # 檢查商店編號是否正確
        if responseData['status'] == 0:
            try:
                shop_attr = [
                    'id',
                    'user_id',
                    'shop_title',
                    'shop_icon',
                    'shop_pic',
                    'shop_description',
                    'paypal',
                    'visa',
                    'master',
                    'apple',
                    'android',
                    'is_ship_free',
                    'ship_by_product',
                    'ship_free_quota',
                    'fix_ship_fee',
                    'fix_ship_fee_from',
                    'fix_ship_fee_to',
                    'transaction_method',
                    'transport_setting',
                    'discount_by_amount',
                    'discount_by_percent',
                    'shop_bank_account',
                    'shop_address',
                    'shop_name_updated_at',
                    'background_pic',
                    'address_phone',
                    'address_is_phone_show',
                    'shop_email',
                    'email_on',
                    'long_description',
                    'facebook_on',
                    'instagram_on'
                    ]
                
                shop = models.Shop.objects.get(id=id,is_delete='N')
                shop_bank_account = models.Shop_Bank_Account.objects.values_list(
                    'id',
                    'code',
                    'name',
                    'account',
                    'account_name'
                ).filter(shop_id=shop.id)
                shop_address = models.Shop_Address.objects.values_list(
                    'id',
                    'name',
                    'country_code',
                    'phone',
                    'is_phone_show',
                    'area',
                    'district',
                    'road',
                    'number',
                    'other',
                    'floor',
                    'room'
                ).filter(shop_id=shop.id)

                responseData['data']['username'] = models.User.objects.get(id=shop.user_id).account_name
                for attr in shop_attr:
                    if(hasattr(shop, attr)):
                        if attr == 'address_phone':
                            responseData['data']['shop_phone'] = getattr(shop, attr)
                        elif attr == 'address_is_phone_show':
                            responseData['data']['shop_is_phone_show'] = getattr(shop, attr)
                        else:
                            responseData['data'][attr] = getattr(shop, attr)

                    elif attr is 'shop_bank_account': # join table
                        responseData['data'][attr] = []
                        for item in shop_bank_account.values():
                            if 'account' in item:
                                item['account'] = "*"+item['account'][-4:]
                            responseData['data'][attr].append(item)                            
                                    
                    elif attr is 'shop_address': # join table
                        responseData['data'][attr] = []
                        for item in shop_address.values():
                            responseData['data'][attr].append(item)
                products = models.Product.objects.filter(shop_id=shop.id,is_delete='N')
                responseData['data']['product_count'] = len(products)
                # dummy data
                responseData['data']['rating'] = 0
                responseData['data']['follower'] = 0
                responseData['data']['income'] = 0
                # ----------
                shop_category_id = models.Selected_Shop_Category.objects.filter(shop_id=id)
                responseData['data']['shop_category_id'] = []
                for obj in shop_category_id:
                    responseData['data']['shop_category_id'].append(getattr(obj,'shop_category_id'))
                responseData['ret_val'] = '已找到商店資料!'
            except:
                responseData['status'] = 1
                responseData['ret_val'] = '找不到此商店編號的商店!'
    return JsonResponse(responseData)
# 刪除商店
def delete(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '',
        'data': {"order_count": 0}
    }
    if request.method == 'DELETE':
        try:
            shop = models.Shop.objects.get(id=id,is_delete='N')
        except:
            responseData['status'], responseData['status'] = -1, '無此商店'
        if responseData['status'] == 0:
            orders = models.Shop_Order.objects.filter(shop_id=id).exclude(status='Pending for Delivery')
            orders_count = len(orders)
            if orders_count>0:
                responseData['status'], responseData['ret_val'], responseData['data']['order_count'] = -2, '尚有訂單未完成', orders_count
        if responseData['status'] == 0:
            shop.is_delete='Y'
            shop.save()
            responseData['ret_val'] = '刪除成功'
    return JsonResponse(responseData)
    

# 確認商店名稱是否重複
def checkShopNameIsExistsProcess(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        shopTitle = request.POST.get('shop_title', '')
        shopTitle = shopTitle.replace('"','')
        shopTitle = shopTitle.replace("'",'')
        if response_data['status'] == 0:
            shops = models.Shop.objects.filter(shop_title=shopTitle, is_delete='N')
            if len(shops) > 0:
                response_data['status'] = -1
                response_data['ret_val'] = '已存在相同名稱的商店!'

        if response_data['status'] == 0:
            response_data['ret_val'] = '商店名稱未重複!'
            
    return JsonResponse(response_data)
# 更新選擇商店分類
def updateSelectedShopCategory(request,id):
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        shop_category_ids = request.POST.get('shop_category_id', '') # json
        
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Selected_Shop_Category.validate_column('shop_id', -1, id)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Selected_Shop_Category.validate_column('shop_category_id_json', -2, shop_category_ids)

        if responseData['status'] == 0:
            selected_shop_categories = models.Selected_Shop_Category.objects.filter(shop_id=id)
            shop_category_ids = json.loads(shop_category_ids)
            with transaction.atomic():
                for category_id in shop_category_ids:
                    if len(models.Selected_Shop_Category.objects.filter(shop_id=id,shop_category_id=category_id)) is 0: # insert
                        print('insert')
                        models.Selected_Shop_Category.objects.create(
                            shop_id=id,
                            shop_category_id=category_id
                        )
                    selected_shop_categories=selected_shop_categories.filter(~Q(shop_category_id=category_id))
                if len(selected_shop_categories)>0: # delete
                    print('delete')
                    selected_shop_categories.delete()
            responseData['ret_val'] = '選擇商店分類更新成功!'

    return JsonResponse(responseData)
# 新增店鋪地址
def createShopAddress(request,id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        addressName = request.POST.get('address_name', '')
        addressCountryCode = request.POST.get('address_country_code', '')
        addressPhone = request.POST.get('address_phone', '')
        addressIsPhoneShow = request.POST.get('address_is_phone_show', '')
        addressArea = request.POST.get('address_area', '')
        addressDistrict = request.POST.get('address_district', '')
        addressRoad = request.POST.get('address_road', '')
        addressNumber = request.POST.get('address_number', '')
        addressOther = request.POST.get('address_other', '')
        addressFloor = request.POST.get('address_floor', '')
        addressRoom = request.POST.get('address_room', '')
        # 新增商店地址
        models.Shop_Address.objects.create(
            id = uuid.uuid4(),
            shop_id = id,
            name = addressName,
            country_code = addressCountryCode,
            phone = addressPhone,
            is_phone_show = addressIsPhoneShow,
            area = addressArea,
            district = addressDistrict,
            road = addressRoad,
            number = addressNumber,
            other = addressOther,
            floor = addressFloor,
            room = addressRoom,
            is_address_show='N',
            is_default='N'
        )
        responseData['status'] =0
        responseData['ret_val'] = '商店地址新增成功!'

    return JsonResponse(responseData)
        # pass
# 更新預設店鋪地址 is_default
def updateShopAddress_isDefault(request): #id : uuid(column)
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        shop_id= request.POST.get('shop_id', '')
        shop_address_id = request.POST.get('shop_address_id', '')

        shop_address_default_olds=models.Shop_Address.objects.filter(shop_id=shop_id)
        for shop_address_default_old in shop_address_default_olds:
            shop_address_default_old.is_default='N'
            shop_address_default_old.save()

        shop_address_default=models.Shop_Address.objects.get(id=shop_address_id)
        shop_address_default.is_default='Y'
        shop_address_default.save()

        responseData['status'] =0
        responseData['ret_val'] = '預設商店地址設定成功!'

    return JsonResponse(responseData)
    # pass
def updateShopAddress_isAddressShow(request): #id : uuid(column)
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        shop_id= request.POST.get('shop_id', '')
        show_status= request.POST.get('show_status', '')
        # shop_address_id = request.POST.get('shop_address_id', '')

        shop_address_isAddressShows=models.Shop_Address.objects.filter(shop_id=shop_id)
        for shop_address_isAddressShow in shop_address_isAddressShows:
            shop_address_isAddressShow.is_address_show=show_status
            shop_address_isAddressShow.save()

        responseData['status'] =0
        responseData['ret_val'] = '設定顯示預設店鋪地址成功!'

    return JsonResponse(responseData)
    # pass
# 更新店鋪地址(x)
def updateShopAddress_unused(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        addressID=request.POST.get('address_ID', '')
        addressName= request.POST.get('address_name', '')
        addressCountry_code= request.POST.get('address_country_code', '')
        addressPhone= request.POST.get('address_phone', '')
        addressIs_phone_show= request.POST.get('address_is_phone_show', '')
        addressArea= request.POST.get('address_area', '')
        addressDistrict= request.POST.get('address_district', '')
        addressRoad= request.POST.get('address_road', '')
        addressNumber= request.POST.get('address_number', '')
        addressOther= request.POST.get('address_other', '')
        addressFloor= request.POST.get('address_floor', '')
        addressRoom= request.POST.get('address_room', '')

        shop_address=models.Shop_Address.objects.get(id=addressID)
        shop_address.name=addressName
        shop_address.country_code=addressCountry_code
        shop_address.phone=addressPhone
        shop_address.is_phone_show=addressIs_phone_show
        shop_address.area=addressDistrict
        shop_address.road=addressRoad
        shop_address.number=addressNumber
        shop_address.other=addressOther
        shop_address.floor=addressFloor
        shop_address.room=addressRoom
        shop_address.save()

        responseData['status'] =0
        responseData['ret_val'] = '商店地址更新成功!'

    return JsonResponse(responseData)
    pass
# 更新商店地址
def updateShopAddress(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        shop_address_list = request.POST.get('shop_address_list')
        # if responseData['status'] == 0:
        #     responseData['status'], responseData['ret_val'] = models.Shop_Shipment_Setting.validate_column('shop_id', -1, id)
        # if responseData['status'] == 0:
        #     responseData['status'], responseData['ret_val'] = models.Shop_Shipment_Setting.validate_column('shipment_settings', -2, shipment_settings)
        if responseData['status'] == 0:
            shop_address_list = json.loads(shop_address_list)
            # print(shop_address_list)
            shop_address_delete = models.Shop_Address.objects.filter(shop_id=id)
            # print(shop_address_delete)
            with transaction.atomic():
                for setting in shop_address_list:
                    # print(setting.name)
                    shop_address = models.Shop_Address.objects.filter(shop_id=id).filter(name=setting['name']).filter(country_code=setting['country_code']).filter(phone=setting['phone']).filter(area=setting['area']).filter(district=setting['district']).filter(road=setting['road']).filter(number=setting['number']).filter(other=setting['other']).filter(floor=setting['floor']).filter(room=setting['room'])
                    # shop_address = models.Shop_Address.objects.filter(Q(shop_id=id)&Q(name=setting['name'])&Q(country_code=setting['country_code'])&Q(phone=setting['phone'])&Q(area=setting['area'])&Q(district=setting['district'])&Q(road=setting['road'])&Q(number=setting['number'])&Q(other=setting['other'])&Q(floor=setting['floor'])&Q(room=setting['room']))
                    row_count = len(shop_address)
                    if row_count is 0: # insert
                        models.Shop_Address.objects.create(
                            id = uuid.uuid4(),
                            shop_id=id,
                            name=setting['name'],
                            country_code=setting['country_code'],
                            phone=setting['phone'],
                            area=setting['area'],
                            district=setting['district'],
                            road=setting['road'],
                            number=setting['number'],
                            other=setting['other'],
                            floor=setting['floor'],
                            room=setting['room'],
                            is_address_show='N',
                            is_default='N'
                        )
                    elif row_count is 1: # update
                        shop_address.update(name=setting['name'],country_code=setting['country_code'],
                            phone=setting['phone'],
                            area=setting['area'],
                            district=setting['district'],
                            road=setting['road'],
                            number=setting['number'],
                            other=setting['other'],
                            floor=setting['floor'],
                            room=setting['room'])
                    shop_address_delete = shop_address_delete.filter(~Q(name=setting['name'],country_code=setting['country_code'],
                            phone=setting['phone'],
                            area=setting['area'],
                            district=setting['district'],
                            road=setting['road'],
                            number=setting['number'],
                            other=setting['other'],
                            floor=setting['floor'],
                            room=setting['room'])
                            )
                if len(shop_address_delete) > 0: # delete
                    shop_address_delete.delete()
            responseData['ret_val'] = '更新商店地址成功'
    return JsonResponse(responseData)
def get_shop_address(request,id): 
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }

    if request.method == 'GET':
        if responseData['status'] == 0:
            shop_address = models.Shop_Address.objects.filter(shop_id=id)
            if len(shop_address) == 0:
                responseData['status'] = 1
                responseData['ret_val'] = '未建立任何商店地址!'
            else:
                for shop_address_info in shop_address:
                    shopAddressInfo = {
                        'id':shop_address_info.id,
                        'shop_id': shop_address_info.shop_id,
                        'name': shop_address_info.name, 
                        'country_code': shop_address_info.country_code,
                        'phone': shop_address_info.phone, 
                        'is_phone_show': shop_address_info.is_phone_show, 
                        'area': shop_address_info.area, 
                        'district': shop_address_info.district, 
                        'road': shop_address_info.road,
                        'number':shop_address_info.number,
                        'other':shop_address_info.other,
                        'floor':shop_address_info.floor,
                        'room':shop_address_info.room,
                        'is_address_show':shop_address_info.is_address_show,
                        'is_default':shop_address_info.is_default
                    }
                    responseData['data'].append(shopAddressInfo)
                responseData['ret_val'] = '已取得商店地址!'
    return JsonResponse(responseData)
# 刪除店鋪地址
def delete_shop_address(request): #id : uuid(column)
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        address_id= request.POST.get('address_id', '')
        if responseData['status'] == 0:
            models.Shop_Address.objects.filter(id=address_id).delete()
            address_delete=models.Shop_Address.objects.filter(id=address_id)
            if len(address_delete)==0:
                responseData['status'] = 0
                responseData['ret_val'] = '刪除商店地址成功!'
            else:
                responseData['status'] = -1
                responseData['ret_val'] = '刪除商店地址失敗!'

    return JsonResponse(responseData)
    # pass
# 刪除店鋪地址
def delete_shop_address_forAndroid(request): #id : uuid(column)
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # address_id= request.POST.getlist('address_id', '')
        address_id=json.loads(request.POST.get('address_id'))
        if responseData['status'] == 0:
            addressIDList=[]
            for addressID in address_id:
                addressIDList.append(addressID)
            print(addressIDList)
            models.Shop_Address.objects.filter(id__in=addressIDList).delete()
            address_delete=models.Shop_Address.objects.filter(id__in=addressIDList)
            print(len(address_delete))
            if len(address_delete)==0:
                responseData['status'] = 0
                responseData['ret_val'] = '刪除商店地址成功!'
            else:
                responseData['status'] = -1
                responseData['ret_val'] = '刪除商店地址失敗!'

    return JsonResponse(responseData)
    # pass
# 銀行帳號
def bankAccount(request, id=0, bank_account_id=''):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '',
        'data': []
    }
    if request.method == 'GET': # 取得
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Shop_Bank_Account.validate_column('shop_id', -1, id)
        if responseData['status'] == 0:
            shop_bank_account_attr = [
                'id',
                'shop_id',
                'code',
                'name',
                'account',
                'account_name',
                'is_default']
            shop_bank_accounts = models.Shop_Bank_Account.objects.filter(shop_id=id).order_by('-is_default')
            for account in shop_bank_accounts:
                tempAccount = {}
                for attr in shop_bank_account_attr:
                    if(hasattr(account, attr)):
                        if attr is 'account':
                            tempAccount[attr] = '*'+getattr(account, attr)[-4:]
                        else:
                            tempAccount[attr] = getattr(account, attr)
                responseData['data'].append(tempAccount)
            responseData['ret_val'] = '已找到銀行帳號資料!'
    elif request.method == 'PATCH': # 修改 - 是否預設(Y/N)
        try:
            default_account = models.Shop_Bank_Account.objects.get(id=bank_account_id)
        except:
            responseData['status'] = -1
            responseData['ret_val'] = '無此商店銀行帳號'

        if responseData['status'] == 0:
            default_account.is_default = 'Y'
            default_account.save()
            other_account = models.Shop_Bank_Account.objects.filter(shop_id=default_account.shop_id).filter(~Q(id=bank_account_id))
            other_account.update(is_default='N')
            
            responseData['ret_val'] = '預設商店銀行帳號更新成功'
    elif request.method == 'POST': # 新增        
        code = request.POST.get('code', '')
        name = request.POST.get('name', '')
        account = request.POST.get('account', '')
        account_name = request.POST.get('account_name', '')
        is_default = request.POST.get('is_default', 'N')
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Shop_Bank_Account.validate_column('shop_id', -1, id)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Shop_Bank_Account.validate_column('code', -2, code)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Shop_Bank_Account.validate_column('name', -3, name)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Shop_Bank_Account.validate_column('account', -4, account)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Shop_Bank_Account.validate_column('account_name', -5, account_name)
            
        if responseData['status'] == 0:
            new = models.Shop_Bank_Account.objects.create(
                id=uuid.uuid4(),
                shop_id=id,
                code=code,
                name=name,
                account=account,
                account_name=account_name,
                is_default=is_default
            )
            responseData['data'] = {'id':new.id}
            responseData['ret_val'] = '商店銀行帳號新增成功'
    elif request.method == 'DELETE': # 刪除
        try:
            account = models.Shop_Bank_Account.objects.get(id=bank_account_id)
        except:
            responseData['status'] = -1
            responseData['ret_val'] = '無此商店銀行帳號'

        if responseData['status'] == 0:
            try:
                with transaction.atomic():
                    account.delete()
                    responseData['ret_val'] = '預設商店銀行帳號刪除成功'
            except:
                responseData['status'] = -99
                responseData['ret_val'] = '預設商店銀行帳號刪除失敗'

    return JsonResponse(responseData)

# 運輸設定 - 同步
def shipmentSettings(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        shipment_settings = request.POST.get('shipment_settings')
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Shop_Shipment_Setting.validate_column('shop_id', -1, id)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Shop_Shipment_Setting.validate_column('shipment_settings', -2, shipment_settings)
        if responseData['status'] == 0:
            shipment_settings = json.loads(shipment_settings)
            settings = models.Shop_Shipment_Setting.objects.filter(shop_id=id)
            if(len(settings)>0):
                settings.delete()
            # 建立資料
            for setting in shipment_settings:
                models.Shop_Shipment_Setting.objects.create(
                    shop_id=id,
                    shipment_desc=setting['shipment_desc'],
                    onoff=setting['onoff']
                )
            responseData['ret_val'] = '運輸設定更新成功!'
    return JsonResponse(responseData)
# 運輸設定 - 取得
def getShipmentSettings(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '',
        'data': []
    }
    if request.method == 'GET':
        responseData['status'], responseData['ret_val'] = models.Shop_Shipment_Setting.validate_column('shop_id', -1, id)
        if responseData['status'] == 0:
            shop_shipment_settings = models.Shop_Shipment_Setting.objects.filter(shop_id=id)
            shop_shipment_settings_attr = [
                'id',
                'shop_id',
                'shipment_desc',
                'onoff'
            ]
            for setting in shop_shipment_settings:
                tempSetting = {}
                for attr in shop_shipment_settings_attr:
                    if(hasattr(setting, attr)):
                        tempSetting[attr] = getattr(setting, attr)
                responseData['data'].append(tempSetting)
            responseData['ret_val'] = '已找到商店運輸設定資料!'
            
    return JsonResponse(responseData)
# 運輸設定 - 設定
def setShipmnetSettings(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        shipment_settings = request.POST.get('shipment_settings')
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Shop_Shipment_Setting.validate_column('shop_id', -1, id)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Shop_Shipment_Setting.validate_column('shipment_settings', -2, shipment_settings)
        if responseData['status'] == 0:
            shipment_settings = json.loads(shipment_settings)
            shop_shipment_settings_delete = models.Shop_Shipment_Setting.objects.filter(shop_id=id)
            with transaction.atomic():
                for setting in shipment_settings:
                    shop_shipment_settings = models.Shop_Shipment_Setting.objects.filter(shop_id=id).filter(shipment_desc=setting['shipment_desc'])
                    row_count = len(shop_shipment_settings)
                    if row_count is 0: # insert
                        models.Shop_Shipment_Setting.objects.create(
                            shop_id=id,
                            shipment_desc=setting['shipment_desc'],
                            onoff=setting['onoff']
                        )
                    elif row_count is 1: # update
                        shop_shipment_settings.update(onoff=setting['onoff'])
                    shop_shipment_settings_delete = shop_shipment_settings_delete.filter(~Q(shipment_desc=setting['shipment_desc']))
                if len(shop_shipment_settings_delete) > 0: # delete
                    shop_shipment_settings_delete.delete()
            responseData['ret_val'] = '運輸設定設定成功'
    return JsonResponse(responseData)

# 取得單一商店產品數量
def get_product_quantity_of_specific_shop(request, id):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'product_quantity': 0
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=id,is_delete='N')
            except:
                response_data['status'] = 1
                response_data['ret_val'] = '找不到此商店編號的商店!'

        if response_data['status'] == 0:
            products = models.Product.objects.filter(shop_id=id,is_delete='N')
            response_data['product_quantity'] = len(products)
            response_data['ret_val'] = '已取得該商店產品數量!'
    return JsonResponse(response_data)
# 取得單一商店追蹤者數量
def get_follower_quantity_of_specific_shop(request, id):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'follower_quantity': 0
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=id,is_delete='N')
            except:
                response_data['status'] = 1
                response_data['ret_val'] = '找不到此商店編號的商店!'

        if response_data['status'] == 0:
            followers = models.Shop_Follower.objects.filter(shop_id=id)
            response_data['follower_quantity'] = len(followers)
            response_data['ret_val'] = '已取得該商店追蹤者數量!'
    return JsonResponse(response_data)
# 取得單一商店產品平均評價
def get_product_average_rating_of_specific_shop(request, id):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'average_rating': 0
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=id,is_delete='N')
            except:
                response_data['status'] = 1
                response_data['ret_val'] = '找不到此商店編號的商店!'

        if response_data['status'] == 0:
            sum_of_rating = 0
            shop_product_ratings = models.Shop_Product_Rating.objects.filter(shop_id=id)
            for shop_product_rating in shop_product_ratings:
                sum_of_rating += shop_product_rating.rating
            response_data['average_rating'] = round(sum_of_rating / len(shop_product_ratings))
            response_data['ret_val'] = '已取得該商店產品平均評價!'
    return JsonResponse(response_data)
# 取得單一商店訂單金額總和
def get_order_amount_of_specific_shop(request, id):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'order_amount': 0
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=id,is_delete='N')
            except:
                response_data['status'] = 1
                response_data['ret_val'] = '找不到此商店編號的商店!'

        if response_data['status'] == 0:
            order_amount = 0
            shop_orders = models.Shop_Order.objects.filter(shop_id=id)
            for shop_order in shop_orders:
                order_amount += shop_order.amount
            response_data['order_amount'] = order_amount
            response_data['ret_val'] = '已取得該商店訂單金額總和!'
    return JsonResponse(response_data)
# 取得單一商店通知設定
def get_notification_setting_of_specific_shop(request, id):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'notification_setting': {}
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            try:
                shop = models.Shop.objects.values_list('marketing_notification', 'follower_notification', 'rating_notification', 'system_upgrade_notification', 'hkshopu_event_notification', flat=True).filter(id=id)
            except:
                response_data['status'] = 1
                response_data['ret_val'] = '找不到此商店編號的商店!'

        if response_data['status'] == 0:
            response_data['notification_setting']['marketing_notification'] = shop.marketing_notification
            response_data['notification_setting']['follower_notification'] = shop.follower_notification
            response_data['notification_setting']['rating_notification'] = shop.rating_notification
            response_data['notification_setting']['system_upgrade_notification'] = shop.system_upgrade_notification
            response_data['notification_setting']['hkshopu_event_notification'] = shop.hkshopu_event_notification
    return JsonResponse(response_data)
# 更新單一商店通知設定
def update_notification_setting_of_specific_shop(request, id):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        marketing_notification = request.POST.get('marketing_notification', '')
        follower_notification = request.POST.get('follower_notification', '')
        rating_notification = request.POST.get('rating_notification', '')
        system_upgrade_notification = request.POST.get('system_upgrade_notification', '')
        hkshopu_event_notification = request.POST.get('hkshopu_event_notification', '')

        if response_data['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=id,is_delete='N')
            except:
                response_data['status'] = -1
                response_data['ret_val'] = '找不到此商店編號的商店!'

        if response_data['status'] == 0:
            if not(marketing_notification):
                response_data['status'] = -2
                response_data['ret_val'] = '未填寫促銷通知!'

        if response_data['status'] == 0:
            if not(follower_notification):
                response_data['status'] = -3
                response_data['ret_val'] = '未填寫追蹤者通知!'

        if response_data['status'] == 0:
            if not(rating_notification):
                response_data['status'] = -4
                response_data['ret_val'] = '未填寫評價通知!'

        if response_data['status'] == 0:
            if not(system_upgrade_notification):
                response_data['status'] = -5
                response_data['ret_val'] = '未填寫系統升級通知!'

        if response_data['status'] == 0:
            if not(hkshopu_event_notification):
                response_data['status'] = -6
                response_data['ret_val'] = '未填寫 HKShopU 事件通知!'

        if response_data['status'] == 0:
            if not(re.match('^(Y|N)$', marketing_notification)):
                response_data['status'] = -7
                response_data['ret_val'] = '促銷通知格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^(Y|N)$', follower_notification)):
                response_data['status'] = -8
                response_data['ret_val'] = '追蹤者通知格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^(Y|N)$', rating_notification)):
                response_data['status'] = -9
                response_data['ret_val'] = '評價通知格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^(Y|N)$', system_upgrade_notification)):
                response_data['status'] = -10
                response_data['ret_val'] = '系統升級通知格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^(Y|N)$', hkshopu_event_notification)):
                response_data['status'] = -11
                response_data['ret_val'] = 'HKShopU 事件通知格式錯誤!'

        if response_data['status'] == 0:
            if marketing_notification != shop.marketing_notification:
                shop.marketing_notification = marketing_notification
            if follower_notification != shop.follower_notification:
                shop.follower_notification = follower_notification
            if rating_notification != shop.rating_notification:
                shop.rating_notification = rating_notification
            if system_upgrade_notification != shop.system_upgrade_notification:
                shop.system_upgrade_notification = system_upgrade_notification
            if hkshopu_event_notification != shop.hkshopu_event_notification:
                shop.hkshopu_event_notification = hkshopu_event_notification
            shop.save()
    return JsonResponse(response_data)
# 取得單一商店簡要資訊
def get_simple_info_of_specific_shop(request, id):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': {}
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=id,is_delete='N')
            except:
                response_data['status'] = 1
                response_data['ret_val'] = '找不到此商店編號的商店!'

        if response_data['status'] == 0:
            shop_addresses = models.Shop_Address.objects.filter(shop_id=id)
            response_data['data']['shop_address'] = []
            for shop_address in shop_addresses:
                shop_address_info = {}
                if shop_address.is_address_show == 'Y' and shop_address.is_default == 'Y':
                    shop_address_info['country_code'] = shop_address.country_code
                    shop_address_info['area'] = shop_address.area
                    shop_address_info['district'] = shop_address.district
                    shop_address_info['road'] = shop_address.road
                    shop_address_info['number'] = shop_address.number
                    shop_address_info['other'] = shop_address.other
                    shop_address_info['floor'] = shop_address.floor
                    shop_address_info['room'] = shop_address.room
                response_data['data']['shop_address'].append(shop_address_info)
            response_data['data']['shop_name'] = shop.shop_title
            response_data['data']['shop_icon'] = shop.shop_icon
            response_data['data']['background_pic'] = shop.background_pic
            if shop.address_is_phone_show == 'Y':
                response_data['data']['phone'] = shop.address_phone
            if shop.email_on == 'Y':
                response_data['data']['shop_email'] = shop.shop_email
            response_data['data']['long_description'] = shop.long_description
            response_data['ret_val'] = '取得單一商店簡要資訊成功!'
    return JsonResponse(response_data)
# 取得推薦熱門商店列表
def get_recommended_shops(request):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            shops = models.Shop.objects.values('id', 'shop_icon', 'shop_title')[:8]
            if len(shops) == 0:
                response_data['status'] = 1
                response_data['ret_val'] = '目前暫無商店!'

        if response_data['status'] == 0:
            for shop in shops:
                sum_of_shop_ratings = 0
                average_of_shop_ratings = 0
                shop_ratings = models.Shop_Rate.objects.filter(shop_id=shop.id).values('rating')
                for shop_rating in shop_ratings:
                    sum_of_shop_ratings += shop_rating.rating
                if len(shop_ratings) > 0:
                    average_of_shop_ratings = sum_of_shop_ratings / len(shop_ratings)
                shop_followers = models.Shop_Follower.objects.filter(shop_id=shop.id)
                data = {
                    'shop_icon': shop.shop_icon, 
                    'shop_title': shop.shop_title, 
                    'shop_average_rating': average_of_shop_ratings, 
                    'shop_followed': 'N' if len(shop_followers) == 0 else 'Y'
                }
                response_data['data'].append(data)
            response_data['ret_val'] = '取得推薦熱門商店列表成功!'
    return JsonResponse(response_data)
# 取得推薦單一熱門商店
def get_specific_recommended_shop(request, id):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': {}
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=id)
            except:
                response_data['status'] = 1
                response_data['ret_val'] = '找不到此商店!'

        if response_data['status'] == 0:
            sum_of_shop_ratings = 0
            average_of_shop_ratings = 0
            shop_ratings = models.Shop_Rate.objects.filter(shop_id=shop.id)
            shop_rating_nums = len(shop_ratings)
            for shop_rating in shop_ratings:
                sum_of_shop_ratings += shop_rating.rating
            if shop_rating_nums > 0:
                average_of_shop_ratings = sum_of_shop_ratings / shop_rating_nums
            products_of_shop = models.Product.objects.filter(shop_id=shop.id)
            product_nums_of_shop = len(products_of_shop)
            shop_followers = models.Shop_Follower.objects.filter(shop_id=shop.id)
            follower_nums_of_shop = len(shop_followers)
    return JsonResponse(response_data)