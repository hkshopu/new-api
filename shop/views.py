from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
                shop = models.Shop.objects.get(shop_title=shopTitle)
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
            responseData['ret_val'] = '商店與選擇商店分類新增成功!'
    return JsonResponse(responseData)
# 更新商店
def update(request, id):
    """
    This API is able to update the shop details according to the selected shop id and update the following information individually:

    Scenarios:

    update the shop_icon

    update the background_pic

    update shop_name and shop_name_update_at if now > shop_name_update_at + 30d

    update shop_long_description

    update address_phone and address_is_phone_show

    update shop_email and email_on

    update facebook_on and instagram_on
    """
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        shopIcon = request.FILES.get('shop_icon', None)
        backgroundPic = request.FILES.get('background_pic', None)
        shopName = request.POST.get('shop_name', None)
        longDescription = request.POST.get('long_description', None)
        addressPhone = request.POST.get('address_phone', None)
        addressIsPhoneShow = request.POST.get('address_is_phone_show', None)
        userEmail = request.POST.get('user_email', None)
        emailOn = request.POST.get('email_on')
        facebookOn = request.POST.get('facebook_on')
        instagramOn = request.POST.get('instagram_on')

        if responseData['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=id)
            except:
                responseData['status'] = -1
                responseData['ret_val'] = '無此商店'
        
        if responseData['status'] == 0:
            destination_path = 'images/shop/'
            if shopIcon:
                db_icon_path = shop.shop_icon
                delete_file(db_icon_path)
                new_icon_path = upload_file(FILE=shopIcon, destination_path=destination_path, suffix="icon")
                shop.shop_icon = new_icon_path
                shop.save()
                responseData['ret_val'] = '商店小圖更新成功!'
            elif backgroundPic:
                db_icon_path = shop.background_pic
                delete_file(db_icon_path)
                new_icon_path = upload_file(FILE=backgroundPic, destination_path=destination_path, suffix="icon")
                shop.background_pic = new_icon_path
                shop.save()
                responseData['ret_val'] = '商店背景更新成功!'                
            elif shopName:
                now = datetime.datetime.now()
                sub = now-shop.shop_name_updated_at
                if sub.days<=30:
                    responseData['status'] = -2
                    responseData['ret_val'] = '商店名稱更新後30天內不得再次更改'
                if responseData['status'] == 0:
                    responseData['status'], responseData['ret_val'] = models.Shop.validate_column('shop_title', -3, shopName)
                if responseData['status'] == 0:
                    shop.shop_title = shopName
                    shop.shop_name_updated_at = now
                    shop.save()
                    responseData['ret_val'] = '商店名稱更新成功!'
            elif longDescription or longDescription is '':
                shop.long_description = longDescription
                shop.save()
                responseData['ret_val'] = '商店描述更新成功!'
            elif not(addressPhone is None) and addressIsPhoneShow:
                pass
            elif userEmail and userEmail is not '' and emailOn and emailOn is not '':
                user = models.User.objects.get(id=shop.user_id)
                if responseData['status'] == 0:
                    user.email = userEmail
                    user.save()
                    shop.email_on = emailOn
                    shop.save()
                    responseData['ret_val'] = '商店電子郵件更新成功'
            elif facebookOn and facebookOn is not '' and instagramOn and instagramOn is not '':
                shop.facebook_on = facebookOn
                shop.instagram_on = instagramOn
                shop.save()
                responseData['ret_val'] = '社群帳號設定更新成功'

    return JsonResponse(responseData)
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
                    'account_name']
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
                    'room']
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
            room = addressRoom
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
            shop_address_default_old.is_default='n'
            shop_address_default_old.save()

        shop_address_default=models.Shop_Address.objects.get(id=shop_address_id)
        shop_address_default.is_default='y'
        shop_address_default.save()

        responseData['status'] =0
        responseData['ret_val'] = '預設商店地址更新成功!'

    return JsonResponse(responseData)
    # pass
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
# 更新店鋪地址
def updateShopAddress(request, id):
    pass
# 刪除店鋪地址
def delShopAddress(request, id):
    pass
# 更新銀行帳號
def updateBankAccount(request, id):
    """
    update the API to set the is_default = “Y” if empty value is passed from UI

    insert the record if no existing records in db where shop_id = selected shop id

    delete the records in db if shop id = selected shop but not exits in the bank account dataset from UI
    """
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        shipment_settings = request.POST.get('bank_account')
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
# 新增運輸設定
def createShipmentSetting(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        shipmentDesc = request.POST.get('shipment_desc')
        onOff = request.POST.get('onoff')

        if responseData['status'] == 0:
            try:
                models.Shop.objects.get(id=id)
            except:
                responseData['status'] = -1
                responseData['ret_val'] = '無此商店!'
                
        if responseData['status'] == 0:
            # 建立資料
            for setting in shipment_settings:
                models.Shop_Shipment_Setting.objects.create(
                    shop_id=id,
                    shipment_desc=setting['shipment_desc'],
                    onoff=setting['onoff']
                )
            responseData['ret_val'] = '運輸設定更新成功!'
    return JsonResponse(responseData)
# 更新運輸設定
def updateShipmentSetting(request, id):
    pass
# 刪除運輸設定
def delShipmentSetting(request, id):
    pass
# 取得運輸設定
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
                responseData['data'].append(tempSetting)\
            
    return JsonResponse(responseData)
# 設定運輸設定
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
                shop = models.Shop.objects.get(id=id)
            except:
                response_data['status'] = 1
                response_data['ret_val'] = '找不到此商店編號的商店!'

        if response_data['status'] == 0:
            products = models.Product.objects.filter(shop_id=id)
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
                shop = models.Shop.objects.get(id=id)
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
                shop = models.Shop.objects.get(id=id)
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
                shop = models.Shop.objects.get(id=id)
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
