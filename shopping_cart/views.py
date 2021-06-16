from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.db.models import Q,Sum
from hkshopu import models
import re
import datetime
import math
from django.core.files.storage import FileSystemStorage
from utils.upload_tools import upload_file , delete_file
import json
import uuid
from django.db.models import Avg
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

#加入購物車
def add(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method=='POST':
        #重要邏輯 : 如果user重複加入購物車，需判斷 if user_id、product_id、product_spec_id與table 中 data相同，將quanity 加上去或update

        user_id= request.POST.get('user_id', '')
        product_id= request.POST.get('product_id', '')
        product_spec_id = request.POST.get('product_spec_id', '')
        quantity=request.POST.get('quantity', '')
        # product_shipment_id=request.POST.get('product_shipment_id', '')
        if quantity=='':
            quantity=1
        else : 
            quantity=quantity

        if response_data['status']==0:
            models.Shopping_Cart.objects.create(
                    id=uuid.uuid4(),
                    user_id=user_id,
                    product_id=product_id,
                    product_spec_id=product_spec_id,
                    quantity=quantity
            )
            cart_check=models.Shopping_Cart.objects.filter(user_id=user_id,product_id=product_id,product_spec_id=product_spec_id,quantity=quantity)
            if(len(cart_check))==0:
                response_data['ret_val'] = '購物車新增失敗!'
            else:
                response_data['ret_val'] = '購物車新增成功!'
    return JsonResponse(response_data)

#購物車清單
def shopping_cart_item(request,user_id): #user_id
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }

    if request.method == 'GET':
        if responseData['status'] == 0:
            shoppingCarts=models.Shopping_Cart.objects.filter(user_id=user_id)
            # products = models.Product.objects.filter(is_delete='N',product_status='active',shop_id=productsShopId.shop_id).filter(~Q(id=product_id))[:3]
            getProductID=[]
            getShopID=[]
            getSpecID=[]
            for shoppingCart in shoppingCarts:
                getProductID.append(shoppingCart.product_id)
                if shoppingCart.product_spec_id=='':
                    pass
                else :
                    getSpecID.append(shoppingCart.product_spec_id)
            print(getSpecID)
            productsShopId=models.Product.objects.filter(id__in=getProductID)
            for shopId in productsShopId:
                getShopID.append(shopId.shop_id)

            shops=models.Shop.objects.filter(id__in=getShopID)
            for shop in shops:
                cartList={
                    'shop_id':0,
                    'shop_title':"",
                    'shop_icon':"",
                    'productList':[]
                }
                products=models.Product.objects.filter(id__in=getProductID)
                cartList.update({"shop_id":shop.id})
                cartList.update({"shop_title":shop.shop_title})
                cartList.update({"shop_icon":shop.shop_icon})
                
                for product in products:
                    if shop.id==product.shop_id:
                        if product.product_spec_on=='y':
                            shipmentList=[]
                            productPics=models.Selected_Product_Pic.objects.get(product_id=product.id,cover='y')
                            productShipments=models.Product_Shipment_Method.objects.filter(product_id=product.id)
                            productSpecs=models.Product_Spec.objects.filter(id__in=getSpecID).filter(product_id=product.id)
               
                            for productSpec in productSpecs:
                                specList=[]
                                productList={
                                "product_id":product.id,
                                "product_title":product.product_title,
                                "product_pic":productPics.product_pic,
                                "shipmentList":shipmentList,
                                "product_spec":specList
                                }
                                cartID=models.Shopping_Cart.objects.get(product_id=product.id,product_spec_id=productSpec.id,user_id=user_id)
                                
                                spec_final={
                                    "shopping_cart_item_id":cartID.id,
                                    "shopping_cart_quantity":cartID.quantity,
                                    "spec_desc_1":productSpec.spec_desc_1,
                                    "spec_desc_2":productSpec.spec_desc_2,
                                    "spec_dec_1_items":productSpec.spec_dec_1_items,
                                    "spec_dec_2_items":productSpec.spec_dec_2_items,
                                    "spec_price":productSpec.price,
                                    "spec_quantity":productSpec.quantity,
                                    }
                                specList.append(spec_final)
                            
                                cartList["productList"].append(productList)

                            for productShipment in productShipments:
                                shipment_final={
                                    "shipment_desc":productShipment.shipment_desc,
                                    "shipment_price":productShipment.price
                                }
                                shipmentList.append(shipment_final)
                            # productList={
                            #     "product_id":product.id,
                            #     "product_title":product.product_title,
                            #     "product_pic":productPics.product_pic,
                            #     "shipmentList":shipmentList,
                            #     "product_spec":specList
                            # }

                            # cartList["productList"].append(productList)
                        else : 
                            print("spec=n")
                            shipmentList=[]
                            productPics=models.Selected_Product_Pic.objects.get(product_id=product.id,cover='y')
                            productShipments=models.Product_Shipment_Method.objects.filter(product_id=product.id)

                            productSpecs=models.Product_Spec.objects.filter(id__in=getSpecID).filter(product_id=product.id)
                            specList=[]
                            cartID=models.Shopping_Cart.objects.get(product_id=product.id,product_spec_id=0,user_id=user_id)
                            spec_final={
                                    "shopping_cart_item_id":cartID.id,
                                    "shopping_cart_quantity":cartID.quantity,
                                    "spec_desc_1":'',
                                    "spec_desc_2":'',
                                    "spec_dec_1_items":'',
                                    "spec_dec_2_items":'',
                                    "spec_price":product.product_price,
                                    "spec_quantity":product.quantity
                                    }
                            specList.append(spec_final)
                            for productShipment in productShipments:
                                shipment_final={
                                    "shipment_desc":productShipment.shipment_desc,
                                    "shipment_price":productShipment.price
                                }
                                shipmentList.append(shipment_final)

                            productList={
                                "product_id":product.id,
                                "product_title":product.product_title,
                                "product_pic":productPics.product_pic,
                                "shipmentList":shipmentList,
                                "product_spec":specList
                            }

                            cartList["productList"].append(productList)
                responseData['data'].append(cartList)   
            responseData['ret_val'] = '已取得商品清單!'
    return JsonResponse(responseData)

#=================
def spec_test(request):
    response_data = {
        'status': 0, 
        'ret_val': '',
    }
    if request.method == 'POST':
        # 欄位資料
        product_spec_list=json.loads(request.POST.get('product_spec_list'))
        print(product_spec_list)
        print("====================")
        print(product_spec_list[0])
        # print(product_spec_list["product_spec_list"][3]["price"])
        # print(len(product_spec_list["product_spec_list"]))
        
        # 檢查欄位是否填寫 
        if response_data['status'] == 0:
            if product_spec_list[0]["shipment"] is None:
                response_data['status'] = -1000
                response_data['ret_val'] = '成功!'
            else:
                response_data['status'] = -87
                response_data['ret_val'] = '失敗!'
    return JsonResponse(response_data)

def pic_conpression(image,width,height):
    im = Image.open(image)#Key Point
    print(im.format, im.size, im.mode)
    new_image=im.resize((width,height))
    print(new_image)

    pic_io=BytesIO ()
    new_image.save (pic_io, im.format)

    pic_file=InMemoryUploadedFile (
    file=pic_io,  field_name=None,  name=image.name,  content_type=image.content_type,  size=image.size,  charset=None
    )
    print(pic_file.seek(0)) #must have seek()
    return pic_file

    #pass

# 圖片壓縮
def pic_resize(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':

        if response_data['status'] == 0:

            productPicURL=[]
            for filename, product_pic_list in request.FILES.lists():
                # print(filename)
                # print(product_pic_list)
                # name = request.FILES[filename].name
                # print(name)
                for index,f in enumerate(product_pic_list):
                    if index==0:
                        for i in range(3):
                            if i ==0: #L     
                                productPicURL.append(upload_file(pic_conpression(f,150,150),'images/img_compression/',suffix="img"))
                            elif i==1: #M
                                productPicURL.append(upload_file(pic_conpression(f,100,100),'images/img_compression/',suffix="img"))
                            elif i==2: #S
                                productPicURL.append(upload_file(pic_conpression(f,50,50),'images/img_compression/',suffix="img"))       
                    else: 
                        productPicURL.append(upload_file(f,'images/img_NoCompression/',suffix="img"))
            #處理圖片&cover
            print(productPicURL)
            for index,product_pic_url in enumerate(productPicURL):            
                # 寫入資料庫
                if index==0 or index==1 or index==2:
                    models.Selected_Product_Pic.objects.create(
                        product_id=5282, 
                        product_pic=product_pic_url,
                        cover="y"
                    )
                else :
                    models.Selected_Product_Pic.objects.create(
                        product_id=5282, 
                        product_pic=product_pic_url,
                        cover="n"
                    )
            response_data['status'] = 0
            response_data['ret_val'] = '圖片壓縮成功!'
    return JsonResponse(response_data)