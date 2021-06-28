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
            shoppingCart_checks=models.Shopping_Cart.objects.filter(user_id=user_id,product_id=product_id,product_spec_id=product_spec_id)
            user_address_id=models.User_Address.objects.filter(user_id=user_id,is_default='Y')
            payment_id=models.Payment_Method.objects.get(is_default='Y')
            shipments=models.Product_Shipment_Method.objects.filter(product_id=product_id,onoff='on').order_by('price')[:1]
            # print(shipments)
            if len(shoppingCart_checks)==0:
                if len(user_address_id)==0:
                    models.Shopping_Cart.objects.create(
                            id=uuid.uuid4(),
                            user_id=user_id,
                            product_id=product_id,
                            product_spec_id=product_spec_id,
                            quantity=quantity,
                            # user_address_id=user_address_id.id,
                            payment_id=payment_id.id,
                            product_shipment_id=shipments[0].id
                    )
                    cart_check=models.Shopping_Cart.objects.filter(user_id=user_id,product_id=product_id,product_spec_id=product_spec_id,quantity=quantity)
                    if(len(cart_check))==0:
                        response_data['ret_val'] = '購物車新增失敗!'
                    else:
                        response_data['ret_val'] = '購物車新增成功!'
                else:
                    models.Shopping_Cart.objects.create(
                            id=uuid.uuid4(),
                            user_id=user_id,
                            product_id=product_id,
                            product_spec_id=product_spec_id,
                            quantity=quantity,
                            user_address_id=user_address_id[0].id,
                            payment_id=payment_id.id,
                            product_shipment_id=shipments[0].id
                    )
                    cart_check=models.Shopping_Cart.objects.filter(user_id=user_id,product_id=product_id,product_spec_id=product_spec_id,quantity=quantity)
                    if(len(cart_check))==0:
                        response_data['ret_val'] = '購物車新增失敗!'
                    else:
                        response_data['ret_val'] = '購物車新增成功!'
            else : 
                for shoppingCart_check in shoppingCart_checks:
                    shoppingCart_check.quantity=shoppingCart_check.quantity+int(quantity)
                    shoppingCart_check.save()
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
                    'user_address_id':"",
                    'name_in_address':"",
                    'address_phone':"",
                    'address':"",
                    'productList':[],
                    'payment_id':"",
                    'payment_desc':""
                }
                products=models.Product.objects.filter(id__in=getProductID)
                cartList.update({"shop_id":shop.id})
                cartList.update({"shop_title":shop.shop_title})
                cartList.update({"shop_icon":shop.shop_icon})
                try:
                    address=models.User_Address.objects.get(user_id=user_id,is_default='Y')
                except models.User_Address.DoesNotExist:
                    address = None

                if address:
                    cartList.update({"user_address_id":address.id})
                    cartList.update({"name_in_address":address.name})
                    cartList.update({"address_phone":address.phone})
                    cartList.update({"address":address.area+address.district+address.road+address.number+address.floor+address.room})

                try:
                    payment=models.Payment_Method.objects.get(is_default='Y')
                except models.Payment_Method.DoesNotExist:
                    payment = None
                if payment:
                    cartList.update({"payment_id":payment.id})
                    cartList.update({"payment_desc":payment.payment_desc})

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
                                    "product_spec_id":productSpec.id,
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
                                    "product_shipment_id":productShipment.id,
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
                                    "product_spec_id":'',
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
                                    "product_shipment_id":productShipment.id,
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

#取得購物車數量
def count(request,user_id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method == 'GET':
        if responseData['status'] == 0:
            shoppingCarts=models.Shopping_Cart.objects.filter(user_id=user_id).count()

            cartCount={
                "cartCount":shoppingCarts
            }
            responseData['data'].append(cartCount)
            responseData['ret_val'] = '已取得購物車數量!'
    return JsonResponse(responseData)

#更新購物車
def update(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method=='POST':
        shopping_cart_item_id=json.loads(request.POST.get('shopping_cart_item_id'))
        new_quantity=request.POST.get('new_quantity', '')
        selected_shipment_id=request.POST.get('selected_shipment_id', '')
        selected_user_address_id=request.POST.get('selected_user_address_id', '')
        selected_payment_id=request.POST.get('selected_payment_id', '')
        getCartID=[]
        for i in range(len(shopping_cart_item_id["shopping_cart_item_id"])):
            getCartID.append(shopping_cart_item_id["shopping_cart_item_id"][i])

        if response_data['status']==0:
            shoppingCarts=models.Shopping_Cart.objects.filter(id__in=getCartID)
            for shoppingCart in shoppingCarts:
                if selected_shipment_id !='':
                    shoppingCart.product_shipment_id=selected_shipment_id               
                elif new_quantity !='':
                    shoppingCart.quantity=new_quantity      
                elif selected_user_address_id !='':
                    shoppingCart.user_address_id =selected_user_address_id
                elif selected_payment_id !='':
                    shoppingCart.payment_id =selected_payment_id

                shoppingCart.save()
                response_data['ret_val'] = '購物車更新成功!'
    return JsonResponse(response_data)

#取得商品運送方式
def product_shipment(request,product_id):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method=='GET':       

        if response_data['status']==0:
            shipments=models.Product_Shipment_Method.objects.filter(product_id=product_id,onoff='on')

            for shipment in shipments:
                shipmentList={
                    "shipment_id":shipment.id,
                    "shipment_desc":shipment.shipment_desc,
                    "shipment_price":shipment.price
                }
                response_data["data"].append(shipmentList)

            response_data['ret_val'] = '運送方式取得成功!'
    return JsonResponse(response_data)

#刪除購物車
def delete(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method=='POST':
        shopping_cart_item_id=json.loads(request.POST.get('shopping_cart_item_id'))

        getCartID=[]
        for i in range(len(shopping_cart_item_id["shopping_cart_item_id"])):
            getCartID.append(shopping_cart_item_id["shopping_cart_item_id"][i])

        if response_data['status']==0:
            shoppingCarts=models.Shopping_Cart.objects.filter(id__in=getCartID).delete()
            response_data['ret_val'] = '刪除成功'

    return JsonResponse(response_data)
    
def buyer_address(request,user_id): 
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    } 
    if request.method=='GET':
        if response_data['status']==0:
            userAddresses=models.User_Address.objects.filter(user_id=user_id)
            for userAddress in userAddresses:
                addressInfo={
                    "id":userAddress.id,
                    "name":userAddress.name,
                    "phone":userAddress.phone,
                    "address": userAddress.area + userAddress.district + userAddress.road +userAddress.number + userAddress.floor + userAddress.room
                }
                response_data['data'].append(addressInfo)

            response_data['ret_val'] = '買家地址取得成功'
    return JsonResponse(response_data)

#加入購物車
def add_buyer_address(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method=='POST':

        user_id= request.POST.get('user_id', '')
        name= request.POST.get('name', '')
        country_code = request.POST.get('country_code', '')
        phone=request.POST.get('phone', '')
        area=request.POST.get('area', '')
        district=request.POST.get('district', '')
        road=request.POST.get('road', '')
        number=request.POST.get('number', '')
        other=request.POST.get('other', '')
        floor=request.POST.get('floor', '')
        room=request.POST.get('room', '')
        print("======")
        print(user_id)
        print(type(user_id))
        print("======")
        if user_id=='' or name=='' or country_code=='' or phone=='' or area=='' or district=='' or road=='' or number=='':
            responseData['status'] = -11
            responseData['ret_val'] = '未填寫必要欄位!'
            return JsonResponse(responseData)
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.User_Address.validate_column('name',-1,name)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.User_Address.validate_column('phone',-2,phone)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.User_Address.validate_column('area',-3,area)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.User_Address.validate_column('district',-4,district)             
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.User_Address.validate_column('road',-5,road)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.User_Address.validate_column('number',-6,number)        
        # if responseData['status'] == 0:
        #     responseData['status'],responseData['ret_val'] = models.User_Address.validate_column('road',-7,road)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.User_Address.validate_column('floor',-7,floor)        
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.User_Address.validate_column('room',-8,room)   
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.User_Address.validate_column('country_code',-9,country_code)     
        if responseData['status'] == 0:
            responseData['status'],responseData['ret_val'] = models.User_Address.validate_column('other',-10,other)         

        if responseData['status']==0:
            addresses=models.User_Address.objects.filter(user_id=user_id).count()
            if addresses>0:
                models.User_Address.objects.create(
                        id=uuid.uuid4(),
                        user_id=user_id,
                        name=name,
                        phone=phone,
                        area=area,
                        district=district,
                        road=road,
                        number=number,
                        floor=floor,
                        room=room,
                        country_code=country_code,
                        other=other,
                        is_default='N',
                        is_address_show='N'
                )
                responseData['ret_val'] = '買家地址新增成功!'
            else:
                models.User_Address.objects.create(
                        id=uuid.uuid4(),
                        user_id=user_id,
                        name=name,
                        phone=phone,
                        area=area,
                        district=district,
                        road=road,
                        number=number,
                        floor=floor,
                        room=room,
                        country_code=country_code,
                        other=other,
                        is_default='Y',
                        is_address_show='N'
                )
                responseData['ret_val'] = '買家地址新增成功!'
    return JsonResponse(responseData)