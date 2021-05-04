from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.db.models import Q
from hkshopu import models
import re
import datetime
import math
from django.core.files.storage import FileSystemStorage
from utils.upload_tools import upload_file , delete_file
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
# 取得單一商片的商品清單
def shop_product(request,id,keyword,product_status,quantity): #shop_id
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }

    if request.method == 'GET':
        if responseData['status'] == 0:
            print(quantity)
            if product_status=="active" and int(quantity)>0: #架上商品
                print("===架上商品===")
                if keyword=="none":
                    print("為空值")
                    products = models.Product.objects.filter(shop_id=id).filter(product_status=product_status)
                    getProductID=[]
                    for product in products:
                        getProductID.append(product.id)
                    
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products:   
                        for productPic in productPics:
                            # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
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
                                        'new_secondhand':product.new_secondhand,
                                        'length':product.length,
                                        'width':product.width,
                                        'height':product.height,
                                        'like':product.like,
                                        'seen':product.seen,
                                        'sold_quantity':product.sold_quantity,
                                        'pic_path':productPic.product_pic,
                                        # 'price' : productSpec.price
                                    }
                                    v = []
                                    # object_methods = [method_name for method_name in dir(responseData['data'])
                                    #     if (callable(getattr(responseData['data'], method_name)) and not method_name.startswith('_'))]
                                    for obj in productSpecs:
                                        # if product.id==productSpecs.product.id:
                                        # responseData['data'].update({'price':obj.price})
                                        v.append(getattr(obj,'price'))
                                    productInfo.update({'price':v})   
                                    responseData['data'].append(productInfo)                 

                    responseData['ret_val'] = '已取得商品清單!'
                else: 
                    print("不能為空值")
                    print("=========")
                    print(keyword)
                    products = models.Product.objects.filter(shop_id=id).filter(Q(product_title__contains=keyword) | Q(product_description__contains=keyword))
                    getProductID=[]
                    for product in products:
                        getProductID.append(product.id)
                    
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products:   
                        for productPic in productPics:
                            # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
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
                                        'new_secondhand':product.new_secondhand,
                                        'length':product.length,
                                        'width':product.width,
                                        'height':product.height,
                                        'like':product.like,
                                        'seen':product.seen,
                                        'sold_quantity':product.sold_quantity,
                                        'pic_path':productPic.product_pic,
                                        # 'price' : productSpec.price
                                    }
                                    v = []
                                    # object_methods = [method_name for method_name in dir(responseData['data'])
                                    #     if (callable(getattr(responseData['data'], method_name)) and not method_name.startswith('_'))]
                                    for obj in productSpecs:
                                        # if product.id==productSpecs.product.id:
                                        # responseData['data'].update({'price':obj.price})
                                        v.append(getattr(obj,'price'))
                                    productInfo.update({'price':v})   
                                    responseData['data'].append(productInfo)                 
            elif product_status=="active" and int(quantity)==0: #已售完
                print("===已售完===")
                print("=========")
                print(keyword)
                if keyword=="none":
                    print("為空值")
                    products = models.Product.objects.filter(shop_id=id).filter(product_status=product_status)
                    getProductID=[]
                    for product in products:
                        getProductID.append(product.id)
                    
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products:   
                        for productPic in productPics:
                            # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
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
                                        'new_secondhand':product.new_secondhand,
                                        'length':product.length,
                                        'width':product.width,
                                        'height':product.height,
                                        'like':product.like,
                                        'seen':product.seen,
                                        'sold_quantity':product.sold_quantity,
                                        'pic_path':productPic.product_pic,
                                        # 'price' : productSpec.price
                                    }
                                    v = []
                                    # object_methods = [method_name for method_name in dir(responseData['data'])
                                    #     if (callable(getattr(responseData['data'], method_name)) and not method_name.startswith('_'))]
                                    for obj in productSpecs:
                                        # if product.id==productSpecs.product.id:
                                        # responseData['data'].update({'price':obj.price})
                                        v.append(getattr(obj,'price'))
                                    productInfo.update({'price':v})   
                                    responseData['data'].append(productInfo)                 

                    responseData['ret_val'] = '已取得商品清單!'
                else: 
                    print("不能為空值")
                    print("=========")
                    print(keyword)
                    products = models.Product.objects.filter(shop_id=id).filter(Q(product_title__contains=keyword) | Q(product_description__contains=keyword))
                    getProductID=[]
                    for product in products:
                        getProductID.append(product.id)
                    
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products:   
                        for productPic in productPics:
                            # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
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
                                        'new_secondhand':product.new_secondhand,
                                        'length':product.length,
                                        'width':product.width,
                                        'height':product.height,
                                        'like':product.like,
                                        'seen':product.seen,
                                        'sold_quantity':product.sold_quantity,
                                        'pic_path':productPic.product_pic,
                                        # 'price' : productSpec.price
                                    }
                                    v = []
                                    # object_methods = [method_name for method_name in dir(responseData['data'])
                                    #     if (callable(getattr(responseData['data'], method_name)) and not method_name.startswith('_'))]
                                    for obj in productSpecs:
                                        # if product.id==productSpecs.product.id:
                                        # responseData['data'].update({'price':obj.price})
                                        v.append(getattr(obj,'price'))
                                    productInfo.update({'price':v})   
                                    responseData['data'].append(productInfo)
                    responseData['ret_val'] = '已取得商品清單!'
            elif product_status=="draft": #未上架
                print("===未上架===")
                print("=========")
                print(keyword)
                if keyword=="none":
                    print("為空值")
                    products = models.Product.objects.filter(shop_id=id).filter(product_status=product_status)
                    getProductID=[]
                    for product in products:
                        getProductID.append(product.id)
                    
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products:   
                        for productPic in productPics:
                            # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
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
                                        'new_secondhand':product.new_secondhand,
                                        'length':product.length,
                                        'width':product.width,
                                        'height':product.height,
                                        'like':product.like,
                                        'seen':product.seen,
                                        'sold_quantity':product.sold_quantity,
                                        'pic_path':productPic.product_pic,
                                        # 'price' : productSpec.price
                                    }
                                    v = []
                                    # object_methods = [method_name for method_name in dir(responseData['data'])
                                    #     if (callable(getattr(responseData['data'], method_name)) and not method_name.startswith('_'))]
                                    for obj in productSpecs:
                                        # if product.id==productSpecs.product.id:
                                        # responseData['data'].update({'price':obj.price})
                                        v.append(getattr(obj,'price'))
                                    productInfo.update({'price':v})   
                                    responseData['data'].append(productInfo)                 

                    responseData['ret_val'] = '已取得商品清單!'
                else: 
                    print("不能為空值")
                    print("=========")
                    print(keyword)
                    products = models.Product.objects.filter(shop_id=id).filter(Q(product_title__contains=keyword) | Q(product_description__contains=keyword))
                    getProductID=[]
                    for product in products:
                        getProductID.append(product.id)
                    
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products:   
                        for productPic in productPics:
                            # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
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
                                        'new_secondhand':product.new_secondhand,
                                        'length':product.length,
                                        'width':product.width,
                                        'height':product.height,
                                        'like':product.like,
                                        'seen':product.seen,
                                        'sold_quantity':product.sold_quantity,
                                        'pic_path':productPic.product_pic,
                                        # 'price' : productSpec.price
                                    }
                                    v = []
                                    # object_methods = [method_name for method_name in dir(responseData['data'])
                                    #     if (callable(getattr(responseData['data'], method_name)) and not method_name.startswith('_'))]
                                    for obj in productSpecs:
                                        # if product.id==productSpecs.product.id:
                                        # responseData['data'].update({'price':obj.price})
                                        v.append(getattr(obj,'price'))
                                    productInfo.update({'price':v})   
                                    responseData['data'].append(productInfo)
                    responseData['ret_val'] = '已取得商品清單!'
            else :
                responseData['status'] = -8787
                responseData['ret_val'] = '有誤!'
    return JsonResponse(responseData)
# 單一商品
def product_info(request,id): #product_id
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }

    if request.method == 'GET':
        if responseData['status'] == 0:
            # shop=models.Shop.objects.get(id=id)
            products = models.Product.objects.filter(id=id)
            getProductID=[]
            for product in products:
                getProductID.append(product.id)
               
            # productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
            productPics=models.Selected_Product_Pic.objects.filter(product_id=getProductID[0])
            productSpecs=models.Product_Spec.objects.filter(product_id=getProductID[0])
            for product in products:       
                productInfo = {
                    'id': product.id,
                    'product_category_id': product.product_category_id,
                    'product_sub_category_id': product.product_sub_category_id,  
                    'product_title': product.product_title,
                    # 'quantity': product.quantity, 
                    'product_description': product.product_description, 
                    # 'product_price': product.product_price, 
                    'shipping_fee': product.shipping_fee, 
                    'created_at': product.created_at, 
                    'updated_at': product.updated_at,
                    'weight':product.weight,
                    'longterm_stock_up':product.longterm_stock_up,
                    'new_secondhand':product.new_secondhand,
                    'product_status':product.product_status,
                    'length':product.length,
                    'width':product.width,
                    'height':product.height,
                    'like':product.like,
                    'seen':product.seen,
                    'sold_quantity':product.sold_quantity,
                    'product_spec_on':product.product_spec_on
                }

                v = []
                spec_desc_1=[]
                spec_desc_2=[]
                spec_dec_1_items=[]
                spec_dec_2_items=[]
                quantity=[]
                v2=[]
              
                for obj in productSpecs:
                    v.append(getattr(obj,'price'))
                    spec_desc_1.append(getattr(obj,'spec_desc_1'))
                    spec_desc_2.append(getattr(obj,'spec_desc_2'))
                    spec_dec_1_items.append(getattr(obj,'spec_dec_1_items'))
                    spec_dec_2_items.append(getattr(obj,'spec_dec_2_items'))
                    quantity.append(getattr(obj,'quantity'))
                for picObj in productPics:
                    v2.append(getattr(picObj,'product_pic'))

                productInfo.update({'price':v})
                productInfo.update({'spec_desc_1':spec_desc_1})
                productInfo.update({'spec_desc_2':spec_desc_2})
                productInfo.update({'spec_dec_1_items':spec_dec_1_items})
                productInfo.update({'spec_dec_2_items':spec_dec_2_items})
                productInfo.update({'quantity':quantity})
                productInfo.update({'pic_path':v2})   
                responseData['data'].append(productInfo)

            responseData['ret_val'] = '已取得商品資訊!'
    return JsonResponse(responseData)

# 更新商品
def update(request,id): #product_id
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        # product_id = request.POST.get('product_id', '') #前一個api先取得
        product_category_id = request.POST.get('product_category_id', '')
        product_sub_category_id = request.POST.get('product_sub_category_id', '')
        product_title = request.POST.get('product_title', '')
        # quantity = request.POST.get('quantity', 0)
        product_description = request.POST.get('product_description', '')
        # product_price = request.POST.get('product_price', 0)
        shipping_fee = request.POST.get('shipping_fee', 0)
        weight = request.POST.get('weight', 0)
        new_secondhand = request.POST.get('new_secondhand', '')
        user_id = request.POST.get('user_id', 0)
        length = request.POST.get('length', 0)
        width = request.POST.get('width', 0)
        height = request.POST.get('height', 0)
        longterm_stock_up = request.POST.get('longterm_stock_up', 0)
        product_status=request.POST.get('product_status', '')
        # 商品規格
        product_spec_list=json.loads(request.POST.get('product_spec_list'))
        print(product_spec_list["product_spec_list"])
        print("====================")
        # print(product_spec_list["product_spec_list"][3]["price"])
        print(len(product_spec_list["product_spec_list"]))
        # 商品運送方式
        shipment_method=json.loads(request.POST.get('shipment_method'))
        print(id)
        if response_data['status'] == 0:
            try:
                product = models.Product.objects.get(id=id)
                productSpec= models.Product_Spec.objects.filter(product_id=id)
                productShipment= models.Product_Shipment_Method.objects.filter(product_id=id)
            except:
                response_data['status'] = -1
                response_data['ret_val'] = '找不到此編號的商品!'
        if response_data['status'] == 0:
            product = models.Product.objects.get(id=id)
            product.product_category_id = product_category_id
            product.product_sub_category_id = product_sub_category_id
            product.product_title = product_title
            product.product_description = product_description
            product.shipping_fee = shipping_fee
            product.weight = weight
            product.new_secondhand=new_secondhand
            product.length=length
            product.width=width
            product.height=height
            product.longterm_stock_up=longterm_stock_up
            product.product_status=product_status
            product.save()

            productPics=models.Selected_Product_Pic.objects.filter(product_id=id)
            for product_pic_del in productPics:
               delete_file(product_pic_del.product_pic)

            productPicURL=[]
            for filename, product_pic_list in request.FILES.lists():
                print(filename,product_pic_list)
                name = request.FILES[filename].name
                print(name)
                for f in product_pic_list:

                    # upload_file(product_pic,'images/product/',suffix="img")
                    productPicURL.append(upload_file(f,'images/product_test/',suffix="img"))
            
            models.Selected_Product_Pic.objects.filter(product_id=id).delete()
            #處理圖片&cover
            for index,product_pic_url in enumerate(productPicURL):            
                # 寫入資料庫
                if index==0:
                    models.Selected_Product_Pic.objects.create(
                        product_id=id, 
                        product_pic=product_pic_url,
                        cover="y"
                    )
                else :
                    models.Selected_Product_Pic.objects.create(
                        product_id=id, 
                        product_pic=product_pic_url,
                        cover="n"
                    )
                
            models.Product_Spec.objects.filter(product_id=id).delete()
            models.Product_Shipment_Method.objects.filter(product_id=id).delete()
                # 寫入資料庫(規格)
            for i in range(len(product_spec_list["product_spec_list"])):
                models.Product_Spec.objects.create(
                    product_id=id,
                    spec_desc_1=product_spec_list["product_spec_list"][i]["spec_desc_1"],
                    spec_desc_2=product_spec_list["product_spec_list"][i]["spec_desc_2"],
                    spec_dec_1_items=product_spec_list["product_spec_list"][i]["spec_dec_1_items"],
                    spec_dec_2_items=product_spec_list["product_spec_list"][i]["spec_dec_2_items"],
                    price=product_spec_list["product_spec_list"][i]["price"],
                    quantity=product_spec_list["product_spec_list"][i]["quantity"],
                )
            

            for i in range(len(shipment_method)):
                models.Product_Shipment_Method.objects.create(
                    product_id=id,
                    shipment_desc=shipment_method[i]["shipment_desc"],
                    price=shipment_method[i]["price"],
                    onoff=shipment_method[i]["onoff"],
                    shop_id=shipment_method[i]["shop_id"]
                )
            response_data['status'] = 0
            response_data['ret_val'] = '商品更新成功!'
    return JsonResponse(response_data)
# 新增商品
def save(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': ''
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
        # product_price = request.POST.get('product_price', 0)
        shipping_fee = request.POST.get('shipping_fee', 0)
        weight = request.POST.get('weight', 0)
        new_secondhand = request.POST.get('new_secondhand', '')
        user_id = request.POST.get('user_id', 0)
        length = request.POST.get('length', 0)
        width = request.POST.get('width', 0)
        height = request.POST.get('height', 0)
        longterm_stock_up = request.POST.get('longterm_stock_up', 0)
        product_status=request.POST.get('product_status', '')
        product_spec_on=request.POST.get('product_spec_on', '')
        
        #商品規格
        product_spec_list=json.loads(request.POST.get('product_spec_list'))
        # print(product_spec_list["product_spec_list"])
        # print("====================")
        # print(product_spec_list["product_spec_list"][3]["price"])
        # print(len(product_spec_list["product_spec_list"]))
        # 商品運送方式
        shipment_method=json.loads(request.POST.get('shipment_method'))

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

        # if response_data['status'] == 0:
        #     if not(product_price):
        #         response_data['status'] = -6
        #         response_data['ret_val'] = '未填寫產品單價!'

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

        # if response_data['status'] == 0:
            # if not(re.match('^\w+$', product_title)):
                # response_data['status'] = -11
                # response_data['ret_val'] = '產品標題格式錯誤!'

        if response_data['status'] == 0:
            if quantity:
                if not(re.match('^\d+$', quantity)):
                    response_data['status'] = -12
                    response_data['ret_val'] = '產品庫存數量格式錯誤!'

        # if response_data['status'] == 0:
        #     if not(re.match('^\d+$', product_price)):
        #         response_data['status'] = -15
        #         response_data['ret_val'] = '產品價格格式錯誤!'

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


        if response_data['status']==0:
            if product_spec_list["product_spec_list"][0]["spec_desc_1"]=="" and product_spec_list["product_spec_list"][0]["spec_desc_2"]=="" and product_spec_list["product_spec_list"][0]["price"]==0 and product_spec_list["product_spec_list"][0]["quantity"]==0:
                response_data['status'] = -87
                response_data['ret_val'] = '未傳送商品規格!'
        if response_data['status']==0:
            if shipment_method[0]["price"]==0 and shipment_method[0]["shop_id"]==0 and shipment_method[0]["shipment_desc"]=="" and shipment_method[0]["onoff"]=="on":
                response_data['status'] = -88
                response_data['ret_val'] = '未傳送商品運輸方式!'

        productPicURL=[]
        
        if response_data['status'] == 0:
            for filename, product_pic_list in request.FILES.lists():
                print(filename,product_pic_list)
                name = request.FILES[filename].name
                print(name)
                for f in product_pic_list:

                    # upload_file(product_pic,'images/product/',suffix="img")
                    productPicURL.append(upload_file(f,'images/product_test/',suffix="img"))
                
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
                # product_price=product_price, 
                shipping_fee=shipping_fee, 
                weight=weight,
                new_secondhand=new_secondhand,
                user_id=user_id,
                length=length, 
                width=width, 
                height=height,
                longterm_stock_up=longterm_stock_up,
                product_status=product_status,
                product_spec_on=product_spec_on
            )
            #傳回product_id
            products=models.Product.objects.filter(
                shop_id=shop_id, 
                product_category_id=product_category_id, 
                product_sub_category_id=product_sub_category_id, 
                product_title=product_title, 
                quantity=quantity, 
                product_description=product_description,  
                # product_price=product_price, 
                shipping_fee=shipping_fee, 
                weight=weight,
                new_secondhand=new_secondhand
                )
            for product in products:
                    productInfo = {
                    'id': product.id,
                }
            getProductID=[]
            getProductID.append(productInfo)
            print(getProductID)
            #圖片上傳DB
            #處理cover
            for index,product_pic_url in enumerate(productPicURL):
            
                # 寫入資料庫
                if index==0:
                    models.Selected_Product_Pic.objects.create(
                        product_id=getProductID[0]['id'], 
                        product_pic=product_pic_url,
                        cover="y"
                    )
                else :
                    models.Selected_Product_Pic.objects.create(
                        product_id=getProductID[0]['id'], 
                        product_pic=product_pic_url,
                        cover="n"
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
            response_data['status'] = 0
            # response_data['pic_upload'] = 'success'
          
        #------------
    return JsonResponse(response_data)
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