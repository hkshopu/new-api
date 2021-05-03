from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.db.models import Q
from django.db import transaction
from django.core.files.storage import FileSystemStorage
from hkshopu import models
import re
import datetime
import math
import uuid
import os
from utils.upload_tools import upload_file
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
                shop = models.Shop.objects.get(shop_title=shopTitle)
                responseData['status'] = -99
                responseData['ret_val'] = '此商店名稱已存在，請選擇其他名稱!'
            except:
                pass
        # 將空字串轉成0
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
        shop_icon = request.FILES.get('shop_icon', '')
        shop_title = request.POST.get('shop_title', '')
        shop_category_id = request.POST.getlist('shop_category_id', [])
        shop_pic = request.FILES.get('shop_pic', '')
        shop_description = request.POST.get('shop_description', '')
        paypal = request.POST.get('paypal', '')
        visa = request.POST.get('visa', '')
        master = request.POST.get('master', '')
        apple = request.POST.get('apple', '')
        android = request.POST.get('android', '')
        is_ship_free = request.POST.get('is_ship_free', '')
        ship_by_product = request.POST.get('ship_by_product', '')
        ship_free_quota = request.POST.get('ship_free_quota', 0)
        fix_ship_fee = request.POST.get('fix_ship_fee', 0)
        fix_ship_fee_from = request.POST.get('fix_ship_fee_from', 0)
        fix_ship_fee_to = request.POST.get('fix_ship_fee_to', 0)
        transaction_method = request.POST.get('transaction_method', '')
        transport_setting = request.POST.get('transport_setting', '')
        discount_by_amount = request.POST.get('discount_by_amount', 0)
        discount_by_percent = request.POST.get('discount_by_percent', 0)
        bank_code = request.POST.get('bank_code', '')
        bank_name = request.POST.get('bank_name', '')
        bank_account = request.POST.get('bank_account', '')
        bank_account_name = request.POST.get('bank_account_name', '')
        address_name = request.POST.get('address_name', '')
        address_country_code = request.POST.get('address_country_code', '')
        address_phone = request.POST.get('address_phone', '')
        address_is_phone_show = request.POST.get('address_is_phone_show', '')
        address_area = request.POST.get('address_area', '')
        address_district = request.POST.get('address_district', '')
        address_road = request.POST.get('address_road', '')
        address_number = request.POST.get('address_number', '')
        address_other = request.POST.get('address_other', '')
        address_floor = request.POST.get('address_floor', '')
        address_room = request.POST.get('address_room', '')

        if response_data['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=id)
            except:
                response_data['status'] = -1
                response_data['ret_val'] = '找不到此商店編號的商店!'

        if response_data['status'] == 0:
            if not(shop.shop_icon) and not(shop_icon):
                response_data['status'] = -3
                response_data['ret_val'] = '未上傳商店小圖!'

        if response_data['status'] == 0:
            if not(shop.shop_title) and not(shop_title):
                response_data['status'] = -4
                response_data['ret_val'] = '未填寫商店標題!'

        if response_data['status'] == 0:
            selected_shop_categories = models.Selected_Shop_Category.objects.filter(shop_id=id)
            if len(selected_shop_categories) == 0 and not(shop_category_id):
                response_data['status'] = -5
                response_data['ret_val'] = '未填寫商店分類編號!'

        if response_data['status'] == 0:
            if shop_icon:
                if not(re.match('^.+\.(gif|png|jpg|jpeg)$', str(shop_icon.name))):
                    response_data['status'] = -7
                    response_data['ret_val'] = '商店小圖格式錯誤!'

        if response_data['status'] == 0:
            if shop_category_id:
                for value in shop_category_id:
                    if not(re.match('^\d+$', value)):
                        response_data['status'] = -8
                        response_data['ret_val'] = '商店分類編號格式錯誤!'
                        break

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
            if bank_code:
                if not(re.match('^\d+$', bank_code)):
                    response_data['status'] = -23
                    response_data['ret_val'] = '銀行代碼格式錯誤!'

        if response_data['status'] == 0:
            if bank_name:
                if not(re.match('^[()\w\s]+$', bank_name)):
                    response_data['status'] = -24
                    response_data['ret_val'] = '銀行名稱格式錯誤!'

        if response_data['status'] == 0:
            if bank_account:
                if not(re.match('^[\-\d]+$', bank_account)):
                    response_data['status'] = -25
                    response_data['ret_val'] = '銀行帳號格式錯誤!'

        if response_data['status'] == 0:
            if bank_account_name:
                if not(re.match('^[!@.#$%)(^&*\+\-\w\s]+$', bank_account_name)):
                    response_data['status'] = -26
                    response_data['ret_val'] = '銀行戶名格式錯誤!'

        if response_data['status'] == 0:
            if address_name:
                if not(re.match('^[!@.#$%)(^&*\+\-\w\s]+$', address_name)):
                    response_data['status'] = -27
                    response_data['ret_val'] = '姓名/公司名稱格式錯誤!'

        if response_data['status'] == 0:
            if address_country_code:
                if not(re.match('^[\+\d]+$', address_country_code)):
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
            shops = models.Shop.objects.filter(shop_title=shop_title)
            if len(shops) > 0:
                response_data['status'] = -38
                response_data['ret_val'] = '此商店名稱已存在，請選擇其他名稱!'

        if response_data['status'] == 0:
            # 上傳圖檔
            destination_path = 'images/shop/'
            shop_icon_url = ''
            shop_pic_url = ''
            if shop_icon:
                shop_icon_url += upload_file(FILE=shop_icon, destination_path=destination_path, suffix='icon')
            if shop_pic:
                shop_pic_url += upload_file(FILE=shop_pic, destination_path=destination_path, suffix='pic')
            # 更新商店
            shop.shop_title = shop_title
            shop.shop_icon = shop_icon_url
            shop.shop_pic = shop_pic_url
            shop.shop_description = shop_description
            shop.paypal = paypal
            shop.visa = visa
            shop.master = master
            shop.apple = apple
            shop.android = android
            shop.is_ship_free = is_ship_free
            shop.ship_by_product = ship_by_product
            shop.ship_free_quota = ship_free_quota
            shop.fix_ship_fee = fix_ship_fee
            shop.fix_ship_fee_from = fix_ship_fee_from
            shop.fix_ship_fee_to = fix_ship_fee_to
            shop.transaction_method = transaction_method
            shop.transport_setting = transport_setting
            shop.discount_by_amount = discount_by_amount
            shop.discount_by_percent = discount_by_percent
            shop.bank_code = bank_code
            shop.bank_name = bank_name
            shop.bank_account = bank_account
            shop.bank_account_name = bank_account_name
            shop.address_name = address_name
            shop.address_country_code = address_country_code
            shop.address_phone = address_phone
            shop.address_is_phone_show = address_is_phone_show
            shop.address_area = address_area
            shop.address_district = address_district
            shop.address_road = address_road
            shop.address_number = address_number
            shop.address_other = address_other
            shop.address_floor = address_floor
            shop.address_room = address_room
            shop.save()
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
                shop = models.Shop.objects.get(id=id)
                shop_bank_account = models.Shop_Bank_Account.objects.filter(shop_id=shop.id)
                shop_address = models.Shop_Address.objects.filter(shop_id=shop.id)
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
                    'shop_email',
                    'email_on',
                    'long_description',
                    'facebook_on',
                    'instagram_on'
                    ]
                shop_bank_account_attr = [
                    'id'
                    'code',
                    'name',
                    'account',
                    'account_name'
                ]
                shop_address_attr = [
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
                ]
                for attr in shop_attr:
                    if(hasattr(shop, attr)):
                        responseData['data'][attr] = getattr(shop, attr)
                    elif attr is 'shop_bank_account':
                        responseData['data'][attr] = []
                        for item in shop_bank_account.values():
                            responseData['data'][attr].append(item)
                    elif attr is 'shop_address':
                        responseData['data'][attr] = []
                        for item in shop_address.values():
                            responseData['data'][attr].append(item)
                products = models.Product.objects.filter(shop_id=shop.id)
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
            shops = models.Shop.objects.filter(shop_title=shopTitle)
            if len(shops) > 0:
                response_data['status'] = -1
                response_data['ret_val'] = '已存在相同名稱的商店!'

        if response_data['status'] == 0:
            response_data['ret_val'] = '商店名稱未重複!'
            
        # 新增 log
        models.Audit_Log.objects.create(
            id=uuid.uuid4(), 
            user_id=0, 
            action='Check Shop Name', 
            parameter_in='shop_title=' + shopTitle + '&response_data[ret_val]=' + response_data['ret_val'] , 
            parameter_out=''
        )
    return JsonResponse(response_data)
# 更新選擇商店分類
def updateSelectedShopCategory(request,id):
    pass
# 新增店鋪地址
def addShopAddress(request):
    pass
# 更新店鋪地址
def updateShopAddress(request, id):
    pass
# 刪除店鋪地址
def delShopAddress(request, id):
    pass
# 更新銀行帳號
def updateBankAccount(request, id):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        code = request.POST.get('code','')
        name = request.POST.get('name','')
        account = request.POST.get('account','')
        account_name = request.POST.get('account_name','')
        # 檢查欄位是否正確
        if response_data['status'] == 0:
            shop_bank_account = models.Shop_Bank_Account.objects.filter(id=id)
            if len(shop_bank_account) is 0:
                response_data['status'] = -1
                response_data['ret_val'] = '無此商店銀行帳號!'
        if response_data['status'] == 0:
            response_data['status'],response_data['ret_val'] = models.Shop_Bank_Account.validate_column('code', -2, code)
        if response_data['status'] == 0:
            response_data['status'],response_data['ret_val'] = models.Shop_Bank_Account.validate_column('name', -3, name)
        if response_data['status'] == 0:
            response_data['status'],response_data['ret_val'] = models.Shop_Bank_Account.validate_column('account', -4, account)
        if response_data['status'] == 0:
            response_data['status'],response_data['ret_val'] = models.Shop_Bank_Account.validate_column('account_name', -5, account_name)
        if response_data['status'] == 0:
            shop_bank_account.update(code=code, name=name, account=account, account_name=account_name)
            response_data['ret_val'] = '商店銀行帳號更新成功!'

    return JsonResponse(response_data)
# 新增銀行帳號
def createBankAccount(request, id):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': '',
        'id':''
    }
    if request.method == 'POST':
        code = request.POST.get('code','')
        name = request.POST.get('name','')
        account = request.POST.get('account','')
        account_name = request.POST.get('account_name','')
        # 檢查欄位是否正確
        if response_data['status'] == 0:
            response_data['status'],response_data['ret_val'] = models.Shop_Bank_Account.validate_column('shop_id', -1, id)
        if response_data['status'] == 0:
            response_data['status'],response_data['ret_val'] = models.Shop_Bank_Account.validate_column('code', -2, code)
        if response_data['status'] == 0:
            response_data['status'],response_data['ret_val'] = models.Shop_Bank_Account.validate_column('name', -3, name)
        if response_data['status'] == 0:
            response_data['status'],response_data['ret_val'] = models.Shop_Bank_Account.validate_column('account', -4, account)
        if response_data['status'] == 0:
            response_data['status'],response_data['ret_val'] = models.Shop_Bank_Account.validate_column('account_name', -5, account_name)
        if response_data['status'] == 0:
            shop_bank_account = models.Shop_Bank_Account.objects.create(
                id=uuid.uuid4(), 
                shop_id = id,
                code=code,
                name=name,
                account=account,
                account_name=account_name
            )
            response_data['id'] = shop_bank_account.id
            response_data['ret_val'] = '商店銀行帳號新增成功!'

    return JsonResponse(response_data)
# 刪除銀行帳號
def delBankAccount(request, id):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'GET':
        # 檢查欄位是否正確
        if response_data['status'] == 0:
            shop_bank_account = models.Shop_Bank_Account.objects.filter(id=id)
            if len(shop_bank_account) is 0:
                response_data['status'] = -1
                response_data['ret_val'] = '無此商店銀行帳號!'

        if response_data['status'] == 0:
            shop_bank_account.delete()
            response_data['ret_val'] = '商店銀行帳號刪除成功!'

    return JsonResponse(response_data)
# 運輸設定
def shipmentSettings(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        if responseData['status'] == 0:
            shop = models.Shop.objects.filter(id=id)
            if len(shop)!=1:
                responseData['status'] = -1
                responseData['ret_val'] = '無此商店!'

        if responseData['status'] == 0:
            try:
                shipment_settings = json.loads(request.POST.get('shipment_settings'))
                # 檢查格式
                for setting in shipment_settings:
                    shipmentDesc = setting['shipment_desc']
                    onOff = setting['onoff']
            except:
                responseData['status'] = -2
                responseData['ret_val'] = '運輸設定格式錯誤!'
                
        if responseData['status'] == 0:
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
# 新增運輸設定
def addShipmentSetting(request):
    pass
def 更新運輸設定(request, id):
    pass
# 刪除運輸設定
def delShipmentSetting(request, id):
    pass

def testAPI(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }

    object_methods = [method_name for method_name in dir(models.Product.objects)
                  if (callable(getattr(models.Product.objects, method_name)) and not method_name.startswith('_'))]
    print(object_methods)
    print(models.Shop.objects.check())
    
    # for key, value in request.POST.lists():
    #     print(key, value)
    #     print(request.POST.get(key))
    return JsonResponse(responseData)