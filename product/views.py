from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.db.models import Q
from hkshopu import models
import re
import datetime
import math
from django.core.files.storage import FileSystemStorage
from utils.upload_tools import upload_file
import json
# Create your views here.
# 取得商品清單
def index(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'product_list': []
    }

    if request.method == 'GET':
        if responseData['status'] == 0:
            products = models.Product.objects.all()
            if len(products) == 0:
                responseData['status'] = 1
                responseData['ret_val'] = '未建立任何商品!'
            else:
                for product in products:
                    productInfo = {
                        'id': product.id,
                        'product_category_id': product.product_category_id, 
                        'product_title': product.product_title,
                        'quantity': product.quantity, 
                        'product_description': product.product_description, 
                        'product_price': product.product_price, 
                        'shipping_fee': product.shipping_fee, 
                        'created_at': product.created_at, 
                        'updated_at': product.updated_at,
                        'weight':product.weight,
                        'longterm_stock_up':product.longterm_stock_up,
                        'new_secondhand':product.new_secondhand
                    }
                    responseData['product_list'].append(productInfo)
                responseData['ret_val'] = '已取得商品清單!'
    return JsonResponse(responseData)

# 新增商品
def save(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': '',
        'pic_upload':'',
        'product_id':[]
    }

    if request.method == 'POST':
        # 欄位資料
        shop_id = request.POST.get('shop_id', '')
        product_category_id = request.POST.get('product_category_id', '')
        product_sub_category_id = request.POST.get('product_sub_category_id', '')
        product_title = request.POST.get('product_title', '')
        quantity = request.POST.get('quantity', 0)
        product_description = request.POST.get('product_description', '')
        # product_country_code = request.POST.get('product_country_code', '') UI無此column
        product_price = request.POST.get('product_price', 0)
        shipping_fee = request.POST.get('shipping_fee', 0)
        weight = request.POST.get('weight', 0)
        new_secondhand = request.POST.get('new_secondhand', '')
        user_id = request.POST.get('user_id', '')
        length = request.POST.get('length', 0)
        width = request.POST.get('width', 0)
        height = request.POST.get('height', 0)
        #商品圖片
        # product_id = request.POST.get('product_id',0)
        product_pic_list = request.FILES.getlist('product_pic_list', [])
        # # 商品規格
        product_spec_list=json.loads(request.POST.get('product_spec_list'))
        print(product_spec_list["product_spec_list"])
        print("====================")
        print(product_spec_list["product_spec_list"][3]["price"])
        print(len(product_spec_list["product_spec_list"]))
        # 商品運送方式
        shipment_method=json.loads(request.POST.get('shipment_method'))

        # for i in range(len(product_spec_list)):
        #     response_data['status'] = -88

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

        # if response_data['status'] == 0:
        #     if product_country_code:
        #         if not(re.match('^\d+$', product_country_code)):
        #             response_data['status'] = -14
        #             response_data['ret_val'] = '產品產地代碼格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^\d+$', product_price)):
                response_data['status'] = -15
                response_data['ret_val'] = '產品價格格式錯誤!'

        if response_data['status'] == 0:
            if not(re.match('^\d+$', shipping_fee)):
                response_data['status'] = -16
                response_data['ret_val'] = '產品運費格式錯誤!'

        if response_data['status'] == 0:
            if not(new_secondhand):
                response_data['status'] = -17
                response_data['ret_val'] = '未填寫全新或二手!'

        if response_data['status'] == 0:
            if weight:
                if not(re.match('^\d+$', weight)):
                    response_data['status'] = -18
                    response_data['ret_val'] = '產品重量格式錯誤!'
        # 檢查商店編號是否存在
        if response_data['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=shop_id)
            except:
                response_data['status'] = -19
                response_data['ret_val'] = '商店編號不存在!'
        # 檢查產品分類編號是否正確
        if response_data['status'] == 0:
            try:
                product_category = models.Product_Category.objects.get(id=product_category_id)
            except:
                response_data['status'] = -20
                response_data['ret_val'] = '產品分類編號不存在!'
        # 檢查產品子分類編號是否正確
        if response_data['status'] == 0:
            try:
                product_sub_category = models.Product_Sub_Category.objects.get(id=product_sub_category_id)
            except:
                response_data['status'] = -21
                response_data['ret_val'] = '產品子分類編號不存在!'
        #商品圖片檢查

        # if response_data['status'] == 0:
        #     if not(product_id):
        #         response_data['status'] = -22
        #         response_data['ret_val'] = '未填寫產品編號!'

        if response_data['status'] == 0:
            if not(product_pic_list):
                response_data['status'] = -23
                response_data['ret_val'] = '未上傳產品圖片!'

        # if response_data['status'] == 0:
        #     if not(re.match('^\d+$', product_id)):
        #         response_data['status'] = -24
        #         response_data['ret_val'] = '產品編號格式錯誤!'

        # if response_data['status'] == 0:
        #     for product_pic in product_pic_list:
        #         if not(re.match('^\w+\.(gif|png|jpg|jpeg)$', str(product_pic_list))):
        #             response_data['status'] = -25
        #             response_data['ret_val'] = '產品圖片格式錯誤!'
        #             break

        # if response_data['status'] == 0:
        #     try:
        #         product = models.Product.objects.get(id=product_id)
        #     except:
        #         response_data['status'] = -26
        #         response_data['ret_val'] = '該產品編號錯誤或不存在!'
        #-----------
        #圖片上傳功能
        productPicURL=[]
        if response_data['status'] == 0:
            for product_pic in product_pic_list:

                # upload_file(product_pic,'images/product/',suffix="img")
                productPicURL.append(upload_file(product_pic,'images/product/',suffix="img"))
                # response_data['status'] = -100
                # response_data['pic_upload'] = 'success'
                #return url需參數
            # return JsonResponse(response_data)
            models.Product.objects.create(
                shop_id=shop_id, 
                product_category_id=product_category_id, 
                product_sub_category_id=product_sub_category_id, 
                product_title=product_title, 
                quantity=quantity, 
                product_description=product_description, 
                # product_country_code=product_country_code, 
                product_price=product_price, 
                shipping_fee=shipping_fee, 
                weight=weight,
                new_secondhand=new_secondhand,
                user_id=user_id,
                length=length, 
                width=width, 
                height=height
            )
            #傳回product_id
            products=models.Product.objects.filter(
                shop_id=shop_id, 
                product_category_id=product_category_id, 
                product_sub_category_id=product_sub_category_id, 
                product_title=product_title, 
                quantity=quantity, 
                product_description=product_description, 
                # product_country_code=product_country_code, 
                product_price=product_price, 
                shipping_fee=shipping_fee, 
                weight=weight,
                new_secondhand=new_secondhand
                )
            for product in products:
                    productInfo = {
                    'id': product.id,
                }
            response_data['product_id'].append(productInfo)
            getProductID=[]
            getProductID.append(productInfo)
            print(getProductID)
            #圖片上傳DB
            for product_pic_url in productPicURL:
                # 自訂圖片檔名
                # now = datetime.datetime.now()
                # product_pic_name = str(product_pic.name).split('.')[0]
                # product_pic_extension = str(product_pic.name).split('.')[1]
                # product_pic_fullname = product_pic_name + '_' + now.strftime('%Y%m%d%H%M%S') + '_' + str(math.floor(now.timestamp())) + '.' + product_pic_extension
                # # 上傳圖片檔案
                # fs = FileSystemStorage(location='templates/static/images/selected_product_pic/')
                # fs.save(name=product_pic_fullname, content=product_pic)
                # 寫入資料庫
                models.Selected_Product_Pic.objects.create(
                    product_id=getProductID[0]['id'], 
                    product_pic=product_pic_url
                )
           #----------------
            
            # 寫入資料庫(規格)
            for i in range(len(product_spec_list["product_spec_list"])):
                models.Product_Spec.objects.create(
                    product_id=getProductID[0]['id'],
                    spec_desc_1=product_spec_list["product_spec_list"][i]["spec_desc_1"],
                    spec_desc_2=product_spec_list["product_spec_list"][i]["spec_desc_2"],
                    spec_dec_1_items=product_spec_list["product_spec_list"][i]["spec_dec_1_items"],
                    spec_dec_2_items=product_spec_list["product_spec_list"][i]["spec_dec_2_items"],
                    price=product_spec_list["product_spec_list"][i]["price"],
                    quantity=product_spec_list["product_spec_list"][i]["quantity"],
                )
            

            for i in range(len(shipment_method)):
                models.Product_Shipment_Method.objects.create(
                    product_id=getProductID[0]['id'],
                    shipment_desc=shipment_method[i]["shipment_desc"],
                    price=shipment_method[i]["price"],
                    onoff=shipment_method[i]["onoff"],
                    shop_id=shipment_method[i]["shop_id"]
                )

            response_data['ret_val'] = '產品新增成功!'
            response_data['status'] = -1000
            response_data['pic_upload'] = 'success'
          
        #------------
    return JsonResponse(response_data)
# 更新商品
# def update(request, id): #id是product_id
#     # 回傳資料
#     responseData = {
#         'status': 0, 
#         'ret_val': ''
#     }
#     if request.method == 'POST':
#         # 欄位資料
#         shop_id = request.POST.get('shop_id', '')
#         product_category_id = request.POST.get('product_category_id', '')
#         product_sub_category_id = request.POST.get('product_sub_category_id', '')
#         product_title = request.POST.get('product_title', '')
#         quantity = request.POST.get('quantity', 0)
#         product_description = request.POST.get('product_description', '')
#         # product_country_code = request.POST.get('product_country_code', '') UI無此column
#         product_price = request.POST.get('product_price', 0)
#         shipping_fee = request.POST.get('shipping_fee', 0)
#         weight = request.POST.get('weight', 0)
#         new_secondhand = request.POST.get('new_secondhand', '')

#         #商品圖片
#         product_id = request.POST.get('product_id',0)
#         product_pic_list = request.FILES.getlist('product_pic_list', [])
#         # # 商品規格
#         product_spec_list=json.loads(request.POST.get('product_spec_list'))
#         print(product_spec_list["product_spec_list"])
#         print("====================")
#         print(product_spec_list["product_spec_list"][3]["price"])
#         print(len(product_spec_list["product_spec_list"]))
#         # 檢查商店編號是否正確
#         if responseData['status'] == 0:
#             try:
#                 product = models.Product.objects.get(id=id)
#             except:
#                 responseData['status'] = -1
#                 responseData['ret_val'] = '找不到此商品編號的商品!'
#         # 檢查使用者是否登入
#         if responseData['status'] == 0:
#             if not('user' in request.session):
#                 responseData['status'] = -2
#                 responseData['ret_val'] = '請先登入會員!'
#         # 判斷必填欄位是否填寫及欄位格式是否正確
#         if responseData['status'] == 0:
#             if not(product_category_id):
#                 responseData['status'] = -3
#                 responseData['ret_val'] = '未填寫商品分類編號!'

#         if responseData['status'] == 0:
#             if not(product_sub_category_id):
#                 responseData['status'] = -5
#                 responseData['ret_val'] = '未填寫商品子分類編號!'
#         if responseData['status'] == 0:
#             if not(product_title):
#                 responseData['status'] = -5
#                 responseData['ret_val'] = '未填寫商品名稱!'
#         if responseData['status'] == 0:
#             if not(quantity):
#                 responseData['status'] = -5
#                 responseData['ret_val'] = '未填寫數量!'
#         # 選填欄位若有填寫，則判斷其格式是否正確


#         if responseData['status'] == 0:
#             if paypal:
#                 if not(re.match('^\w+$', paypal)):
#                     responseData['status'] = -9
#                     responseData['ret_val'] = 'PayPal 格式錯誤!'

#         if responseData['status'] == 0:
#             if visa:
#                 if not(re.match('^\w+$', visa)):
#                     responseData['status'] = -10
#                     responseData['ret_val'] = 'Visa 卡格式錯誤!'

#         if responseData['status'] == 0:
#             if master:
#                 if not(re.match('^\w+$', master)):
#                     responseData['status'] = -11
#                     responseData['ret_val'] = 'Master 卡格式錯誤!'

#         if responseData['status'] == 0:
#             if apple:
#                 if not(re.match('^\w+$', apple)):
#                     responseData['status'] = -12
#                     responseData['ret_val'] = 'Apple 格式錯誤!'

#         if responseData['status'] == 0:
#             if android:
#                 if not(re.match('^\w+$', android)):
#                     responseData['status'] = -13
#                     responseData['ret_val'] = 'Android 格式錯誤!'

#         if responseData['status'] == 0:
#             if isShipFree:
#                 if not(re.match('^\w+$', isShipFree)):
#                     responseData['status'] = -14
#                     responseData['ret_val'] = '是否免運費格式錯誤!'

#         if responseData['status'] == 0:
#             if shipFreeQuota:
#                 if not(re.match('^\d+$', shipFreeQuota)):
#                     responseData['status'] = -15
#                     responseData['ret_val'] = '免運費訂單價格格式錯誤!'

#         if responseData['status'] == 0:
#             if fixShipFee:
#                 if not(re.match('^\d+$', fixShipFee)):
#                     responseData['status'] = -16
#                     responseData['ret_val'] = '運費訂價格式錯誤!'

#         if responseData['status'] == 0:
#             if fixShipFeeFr:
#                 if not(re.match('^\d+$', fixShipFeeFr)):
#                     responseData['status'] = -17
#                     responseData['ret_val'] = '訂單價格由格式錯誤!'

#         if responseData['status'] == 0:
#             if fixShipFeeTo:
#                 if not(re.match('^\d+$', fixShipFeeTo)):
#                     responseData['status'] = -18
#                     responseData['ret_val'] = '訂單價格至格式錯誤!'

#         if responseData['status'] == 0:
#             if shipByProduct:
#                 if not(re.match('^\w+$', shipByProduct)):
#                     responseData['status'] = -19
#                     responseData['ret_val'] = '運費由商品設定格式錯誤!'
        
#         if responseData['status'] == 0:
#             if not(discountByPercent) and not(discountByAmount):
#                 responseData['status'] = -20
#                 responseData['ret_val'] = '折扣欄位必須擇一填寫!'
#             else:
#                 if discountByPercent:
#                     if not(re.match('^\d+$', discountByPercent)):
#                         responseData['status'] = -21
#                         responseData['ret_val'] = '百分比折扣格式錯誤!'

#                 if discountByAmount:
#                     if not(re.match('^\d+$', discountByAmount)):
#                         responseData['status'] = -22
#                         responseData['ret_val'] = '價格折扣格式錯誤!'
#         # 先檢查使用者是否更改商店名稱，若有更改，則檢查是否更改名稱為其他同名的商店
#         if responseData['status'] == 0:
#             try:
#                 oldShop = models.Shop.objects.get(id=id, shop_title=shopTitle)
#             except:
#                 sameNameShops = models.Shop.objects.filter(shop_title=shopTitle)
#                 if len(sameNameShops) > 0:
#                     responseData['status'] = -23
#                     responseData['ret_val'] = '此商店名稱已存在，請選擇其他名稱!'
#         # 更新商店
#         if responseData['status'] == 0:
#             shop.shop_title = shopTitle
#             shop.shop_description = shopDesc
#             shop.paypal = paypal
#             shop.visa = visa
#             shop.master = master
#             shop.apple = apple
#             shop.android = android
#             shop.is_ship_free = isShipFree
#             shop.ship_by_product = shipByProduct
#             shop.ship_free_quota = shipFreeQuota
#             shop.fix_ship_fee = fixShipFee
#             shop.fix_ship_fee_from = fixShipFeeFr
#             shop.fix_ship_fee_to = fixShipFeeTo
#             shop.save()
#             responseData['ret_val'] = '商店更新成功!'
#     return JsonResponse(responseData)

#=================
def spec_test(request):
    response_data = {
        'status': 0, 
        'ret_val': '',
    }
    if request.method == 'POST':
        # 欄位資料
        product_spec_list=json.loads(request.POST.get('product_spec_list'))
        print(product_spec_list["product_spec_list"])
        print("====================")
        print(product_spec_list["product_spec_list"][3]["price"])
        print(len(product_spec_list["product_spec_list"]))

        # 檢查欄位是否填寫 
        if response_data['status'] == 0:
            # for product_spec_list02 in product_spec_list:
            # 寫入資料庫
            for i in range(len(product_spec_list["product_spec_list"])):
                # models.Product_Spec.objects.create(
                #     product_id=product_spec_list[i][0],
                #     spec_name=product_spec_list[i][1],
                #     price=product_spec_list[i][2],
                #     quantity=product_spec_list[i][3],
                #     size=product_spec_list[i][4]
                # )
                models.Product_Spec.objects.create(
                    product_id=product_spec_list["product_spec_list"][i]["product_id"],
                    spec_desc_1=product_spec_list["product_spec_list"][i]["spec_desc_1"],
                    spec_desc_2=product_spec_list["product_spec_list"][i]["spec_desc_2"],
                    spec_dec_1_items=product_spec_list["product_spec_list"][i]["spec_dec_1_items"],
                    spec_dec_2_items=product_spec_list["product_spec_list"][i]["spec_dec_2_items"],
                    price=product_spec_list["product_spec_list"][i]["price"],
                    quantity=product_spec_list["product_spec_list"][i]["quantity"],
                )
            # print(product_spec_list)

            # for product_spec in product_spec_list:
            #     models.Product_Spec.objects.create(
            #             product_id=product_spec['product_id'],
            #             spec_name=product_spec['spec_name'],
            #             price=product_spec['price'],
            #             quantity=product_spec['quantity'],
            #             size=product_spec['size']
            #     )
            #     response_data['test']=product_spec.product_id

            response_data['status'] = -1000
            response_data['ret_val'] = '成功!'
            # response_data['test'].append(product_spec_list)
            

    return JsonResponse(response_data)