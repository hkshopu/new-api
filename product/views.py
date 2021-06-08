from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
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
# 取得單一商店的商品清單
def shop_product(request,id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }

    if request.method == 'GET':
        if responseData['status'] == 0:
            # shop=models.Shop.objects.get(id=id)
            products = models.Product.objects.filter(shop_id=id).filter(product_status='active').filter(is_delete='N')
            getProductID=[]
            for product in products:
                getProductID.append(product.id)
               
            productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
            for product in products:   
                if product.product_spec_on=='y':
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
                                'product_status':product.product_status,
                                'pic_path':productPic.product_pic,
                                'product_spec_on':product.product_spec_on
                                # 'price' : productSpec.price
                            }
                            #responseData['data'].append(productInfo)    
                            # responseData['data']['price'] = {}
                            v = []
                            price_range=[]
                            quantity_sum=[]
                            for obj in productSpecs:
                                # if product.id==productSpecs.product.id:
                                # responseData['data'].update({'price':obj.price})
                                v.append(getattr(obj,'price'))
                                price_range.append(getattr(obj,'price'))
                                quantity_sum.append(getattr(obj,'quantity'))
                            min_price=min(price_range)
                            max_price=max(price_range)
                        
                            productInfo.update({'price':v})   
                            productInfo.update({'min_price':min_price})   
                            productInfo.update({'max_price':max_price})  
                            productInfo.update({'min_quantity':product.quantity}) 
                            productInfo.update({'max_quantity':product.quantity})
                            productInfo.update({'sum_quantity': sum(quantity_sum)}) 
                            responseData['data'].append(productInfo)
                elif product.product_spec_on=='n':   
                    for productPic in productPics:
                        # for productSpec in productSpecs:    
                        if product.id==productPic.product_id : 
                            # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
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
                                'product_status':product.product_status,
                                'pic_path':productPic.product_pic,
                                'product_spec_on':product.product_spec_on
                                # 'price' : productSpec.price
                            }
                            #responseData['data'].append(productInfo)    
                            # responseData['data']['price'] = {}
                            productInfo.update({'min_price':product.product_price}) 
                            productInfo.update({'max_price':product.product_price}) 
                            productInfo.update({'min_quantity':product.quantity}) 
                            productInfo.update({'max_quantity':product.quantity})
                            productInfo.update({'sum_quantity':product.quantity})
                            responseData['data'].append(productInfo) 
                                         

            responseData['ret_val'] = '已取得商品清單!'
    return JsonResponse(responseData)
# 取得我的商品清單
def product_list(request,id,keyword,product_status,quantity): #shop_id
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }

    if request.method == 'GET':
        if responseData['status'] == 0:
            
            if product_status=="active" and int(quantity)==1: #架上商品
                
                if keyword=="none":
                    products = models.Product.objects.filter(shop_id=id).filter(product_status=product_status).filter(is_delete='N')
                    # print(products)
                    getProductID=[]
                    for product in products:
                        getProductID.append(product.id)
                    
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products: 
                         
                        if product.product_spec_on=='y':
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    
                                    
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id).filter(quantity__gt=0)
                                    
                                    if(len(productSpecs)==0):
                                        break
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
                                        'product_spec_on':product.product_spec_on,
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
                                    min_price=min(v)
                                    max_price=max(v)
                                    productInfo.update({'min_price':min_price}) 
                                    productInfo.update({'max_price':max_price})   
                                    responseData['data'].append(productInfo)
                        elif product.product_spec_on=='n':     
                            
                            for productPic in productPics:  
                                
                                if product.id==productPic.product_id and product.quantity !=0 : 
                                    
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
                                        'product_spec_on':product.product_spec_on,
                                        'pic_path':productPic.product_pic,
                                        # 'price' : productSpec.price
                                    }
                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    responseData['data'].append(productInfo)
                    responseData['ret_val'] = '已取得商品清單!'
                else: 
                    
                    products = models.Product.objects.filter(shop_id=id).filter(is_delete='N').filter(Q(product_title__contains=keyword) | Q(product_description__contains=keyword))
                    getProductID=[]
                    for product in products:
                        getProductID.append(product.id)
                    
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products: 
                        
                        if product.product_spec_on=='y':
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    
                                    
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id).filter(quantity__gt=0)
                                    
                                    if(len(productSpecs)==0):
                                        break
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
                                        'product_spec_on':product.product_spec_on,
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
                                    min_price=min(v)
                                    max_price=max(v)
                                    productInfo.update({'min_price':min_price}) 
                                    productInfo.update({'max_price':max_price})   
                                    responseData['data'].append(productInfo)
                        elif product.product_spec_on=='n':     
                            
                            
                            for productPic in productPics:  
                                
                                if product.id==productPic.product_id  and product.quantity !=0 : 
                                    
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
                                        'product_spec_on':product.product_spec_on,
                                        'pic_path':productPic.product_pic,
                                        # 'price' : productSpec.price
                                    }
                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    responseData['data'].append(productInfo)
                    responseData['ret_val'] = '已取得商品清單!'             
            elif product_status=="active" and int(quantity)==0: #已售完
                
                # print(keyword)
                zero_status=[]
                if keyword=="none":
                    
                    products_on_id = models.Product.objects.filter(shop_id=id).filter(product_status=product_status).filter(quantity=-1).filter(is_delete='N')
                    products_off_id = models.Product.objects.filter(shop_id=id).filter(product_status=product_status).filter(quantity=0).filter(is_delete='N')
                    getProductID=[]
                    # print(products)
                    # for product in products_on_id:
                    #     getProductID.append(product.id)

                    productSpecs_tests=models.Product_Spec.objects.filter(product_id__in=products_on_id).values('product_id').order_by('product_id').annotate(quantity_sum=Sum('quantity')).filter(quantity_sum=0)
                    # productSpecsIDList=[] #沒spec等於塞product的id
                    

                    for i in range (len(productSpecs_tests)):
                        getProductID.append(productSpecs_tests[i]['product_id'])
                       
                    # print(productSpecsIDList)
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    

                    products = models.Product.objects.filter(id__in=getProductID)
                    for product in products:  
                        if product.product_spec_on=='y' and product.quantity==-1 : 
                            for productPic in productPics:
                            # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    
                                    productSpecs=models.Product_Spec.objects.filter(product_id__in=getProductID) #.filter(quantity=0)

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
                                        'product_spec_on':product.product_spec_on,
                                        'pic_path':productPic.product_pic,
                                        # 'price' : productSpec.price
                                    }
                                    v = []

                                    productSpecs_final=models.Product_Spec.objects.filter(product_id=product.id) #.filter(quantity=0)
                                    for obj in productSpecs_final:
                                        # if product.id==productSpecs.product.id:
                                        # responseData['data'].update({'price':obj.price})
                                        v.append(getattr(obj,'price'))
                                    min_price=min(v)
                                    max_price=max(v)
                                    productInfo.update({'min_price':min_price}) 
                                    productInfo.update({'max_price':max_price})
                                    # productInfo.update({'price':v})   
                                    responseData['data'].append(productInfo)                 
                        elif product.product_spec_on=='n' and product.quantity==0:
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
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
                                        'product_spec_on':product.product_spec_on,
                                        'pic_path':productPic.product_pic,
                                        # 'price' : productSpec.price
                                    }
                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    responseData['data'].append(productInfo)
                    responseData['ret_val'] = '已取得商品清單!'
                else: 
                    
                    products_on_id = models.Product.objects.filter(shop_id=id).filter(product_status=product_status).filter(quantity=-1).filter(is_delete='N')
                    products_off_id = models.Product.objects.filter(shop_id=id).filter(product_status=product_status).filter(quantity=0).filter(is_delete='N') 
                    getProductID=[]
                    # print(products)
                    # for product in products_on_id:
                    #     getProductID.append(product.id)

                    productSpecs_tests=models.Product_Spec.objects.filter(product_id__in=products_on_id).values('product_id').order_by('product_id').annotate(quantity_sum=Sum('quantity')).filter(quantity_sum=0)
                    # productSpecsIDList=[] #沒spec等於塞product的id
                   

                    for i in range (len(productSpecs_tests)):
                        getProductID.append(productSpecs_tests[i]['product_id'])
                      
                    # print(productSpecsIDList)
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    

                    products = models.Product.objects.filter(id__in=getProductID)


                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')
                    for product in products:  
                        if product.product_spec_on=='y'and product.quantity==0: 
                            for productPic in productPics:
                            # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    
                                    productSpecs=models.Product_Spec.objects.filter(product_id__in=getProductID) #.filter(quantity=0)

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
                                        'product_spec_on':product.product_spec_on,
                                        'pic_path':productPic.product_pic,
                                        # 'price' : productSpec.price
                                    }
                                    v = []

                                    productSpecs_final=models.Product_Spec.objects.filter(product_id=product.id) #.filter(quantity=0)
                                    for obj in productSpecs_final:
                                        # if product.id==productSpecs.product.id:
                                        # responseData['data'].update({'price':obj.price})
                                        v.append(getattr(obj,'price'))
                                    min_price=min(v)
                                    max_price=max(v)
                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price})
                                    # productInfo.update({'price':v})   
                                    responseData['data'].append(productInfo)                 
                        elif product.product_spec_on=='n' and product.quantity==0:
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
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
                                        'product_spec_on':product.product_spec_on,
                                        'pic_path':productPic.product_pic,
                                        # 'price' : productSpec.price
                                    }
                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    responseData['data'].append(productInfo)
                    responseData['ret_val'] = '已取得商品清單!'
            elif product_status=="draft": #未上架
                
                if keyword=="none":
                    
                    products = models.Product.objects.filter(shop_id=id).filter(product_status=product_status).filter(is_delete='N')
                    getProductID=[]
                    for product in products:
                        getProductID.append(product.id)
                    
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products: 
                       
                        if product.product_spec_on=='y':
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    
                                    
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    
                                    if(len(productSpecs)==0):
                                        break
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
                                        'product_spec_on':product.product_spec_on,
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
                                    min_price=min(v)
                                    max_price=max(v)
                                    productInfo.update({'min_price':min_price}) 
                                    productInfo.update({'max_price':max_price})   
                                    responseData['data'].append(productInfo)
                        elif product.product_spec_on=='n':     
                            
                            for productPic in productPics:  
                                
                                if product.id==productPic.product_id : 
                                    
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
                                        'product_spec_on':product.product_spec_on,
                                        'pic_path':productPic.product_pic,
                                        # 'price' : productSpec.price
                                    }
                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    responseData['data'].append(productInfo)
                    responseData['ret_val'] = '已取得商品清單!'
                else: 
                    
                    products = models.Product.objects.filter(shop_id=id).filter(is_delete='N').filter(Q(product_title__contains=keyword) | Q(product_description__contains=keyword)).filter(product_status=product_status)
                    getProductID=[]
                    for product in products:
                        getProductID.append(product.id)
                    
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products: 
                      
                        if product.product_spec_on=='y':
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    
                                    
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    
                                    if(len(productSpecs)==0):
                                        break
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
                                        'product_spec_on':product.product_spec_on,
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
                                    min_price=min(v)
                                    max_price=max(v)
                                    productInfo.update({'min_price':min_price}) 
                                    productInfo.update({'max_price':max_price})   
                                    responseData['data'].append(productInfo)
                        elif product.product_spec_on=='n':     
                            
                            for productPic in productPics:  
                                
                                if product.id==productPic.product_id : 
                                    
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
                                        'product_spec_on':product.product_spec_on,
                                        'pic_path':productPic.product_pic,
                                        # 'price' : productSpec.price
                                    }
                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
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
            products = models.Product.objects.filter(id=id).filter(is_delete='N')
            getProductID=[]
            for product in products:
                getProductID.append(product.id)
               
            # productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
            productPics=models.Selected_Product_Pic.objects.filter(product_id=getProductID[0])
            productSpecs=models.Product_Spec.objects.filter(product_id=getProductID[0])
            productShipments=models.Product_Shipment_Method.objects.filter(product_id=id)
            
            for product in products:       
                productInfo = {
                    'id': product.id,
                    'product_category_id': product.product_category_id,
                    'product_sub_category_id': product.product_sub_category_id,  
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
                shipment_desc=[]
                shipment_price=[]
                onoff=[]
                v2=[]
              
                for obj in productSpecs:
                    v.append(getattr(obj,'price'))
                    spec_desc_1.append(getattr(obj,'spec_desc_1'))
                    spec_desc_2.append(getattr(obj,'spec_desc_2'))
                    spec_dec_1_items.append(getattr(obj,'spec_dec_1_items'))
                    spec_dec_2_items.append(getattr(obj,'spec_dec_2_items'))
                    quantity.append(getattr(obj,'quantity'))

                for productShipment in productShipments:
                    shipment_desc.append(getattr(productShipment,'shipment_desc'))
                    shipment_price.append(getattr(productShipment,'price'))
                    onoff.append(getattr(productShipment,'onoff'))

                for picObj in productPics:
                    v2.append(getattr(picObj,'product_pic'))

                productInfo.update({'spec_price':v})
                productInfo.update({'spec_desc_1':spec_desc_1})
                productInfo.update({'spec_desc_2':spec_desc_2})
                productInfo.update({'spec_dec_1_items':spec_dec_1_items})
                productInfo.update({'spec_dec_2_items':spec_dec_2_items})
                productInfo.update({'spec_quantity':quantity})
                productInfo.update({'shipment_desc':shipment_desc})
                productInfo.update({'shipment_price':shipment_price})
                productInfo.update({'onoff':onoff})
                productInfo.update({'pic_path':v2})   
                responseData['data'].append(productInfo)

            responseData['ret_val'] = '已取得商品資訊!'
    return JsonResponse(responseData)
# 單一商品for android
def product_info_forAndroid(request,id): #product_id
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }

    if request.method == 'GET':
        if responseData['status'] == 0:
            # shop=models.Shop.objects.get(id=id)
            products = models.Product.objects.filter(id=id).filter(is_delete='N')
            getCategoryID=[]
            getSubCategoryID=[]
            
            for product in products:
                getCategoryID.append(product.product_category_id)
                getSubCategoryID.append(product.product_sub_category_id)
            
            # productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
            
            if products[0].product_spec_on=='y':
                
                productPics=models.Selected_Product_Pic.objects.filter(product_id=id)
                productSpecs=models.Product_Spec.objects.filter(product_id=id)
                productShipments=models.Product_Shipment_Method.objects.filter(product_id=id)
                productCategorys=models.Product_Category.objects.filter(id=getCategoryID[0])
                productSubCategorys=models.Product_Sub_Category.objects.filter(id=getSubCategoryID[0])
                
                for product in products:       
                    productInfo = {
                        'id': product.id,
                        'product_category_id': product.product_category_id,
                        'product_sub_category_id': product.product_sub_category_id,  
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
                        'product_status':product.product_status,
                        'length':product.length,
                        'width':product.width,
                        'height':product.height,
                        'like':product.like,
                        'seen':product.seen,
                        'sold_quantity':product.sold_quantity,
                        'product_spec_on':product.product_spec_on,
                        # 'c_category_name':productCategorys.c_product_category,
                        # 'c_sub_category_name':productSubCategorys.c_product_sub_category
                    }
                # category_name=[]
                # sub_category_name=[]
                print(productCategorys)
                for productCategory in productCategorys:
                    category_name=(getattr(productCategory,'c_product_category'))
                productInfo.update({'c_product_category':category_name}) 
                
                for productSubCategory in productSubCategorys:
                    sub_category_name=(getattr(productSubCategory,'c_product_sub_category'))
                productInfo.update({'c_sub_product_category':sub_category_name}) 

                # pic_list=[]
                # for productPic in productPics:
                #     pic_list.append(getattr(productPic,'product_pic'))
                # productInfo.update({'pic_path':pic_list})

                # responseData['data'].append(productInfo)
                # # product_spec_list=['product_spec_list']
                # spec_dict={"product_spec_list":[]}
                # spec_price_dict={"spec_price":[]}
                # spec_price=[]
                
                # for productSpec in productSpecs:
                #     productSpecInfo = {
                #         "spec_desc_1":productSpec.spec_desc_1,
                #         "spec_desc_2":productSpec.spec_desc_2,
                #         "spec_dec_1_items":productSpec.spec_dec_1_items,
                #         "spec_dec_2_items":productSpec.spec_dec_2_items,
                #         "quantity":productSpec.quantity,
                #         "price":productSpec.price
                #     }
                #     v = []
                #     for obj in productSpecs:
                #         # if product.id==productSpecs.product.id:
                #         # responseData['data'].update({'price':obj.price})
                #         v.append(getattr(obj,'price'))
                #     # productSpecInfo.update({'price':v})
                    
                #     spec_price.append(productSpec.price)
                #     spec_dict["product_spec_list"].append(productSpecInfo)
                # min_price=min(spec_price)
                # max_price=max(spec_price)
                # productSpecPriceInfo = {
                #     "min_price":min_price,
                #     "max_price":max_price
                # }
                # spec_price_dict["spec_price"].append(productSpecPriceInfo)

                # spec_dict.update({"min_price":min_price})     
                # spec_dict.update({"max_price":max_price}) 
                    # product_spec_list.append(productSpecInfo)
                # responseData['data'].append(spec_dict)
                # responseData['data'].append(spec_price_dict)

                v1 = []
                spec_desc_1=[]
                spec_desc_2=[]
                spec_dec_1_items=[]
                spec_dec_2_items=[]
                spec_quantity=[]
                shipment_desc=[]
                shipment_price=[]
                onoff=[]
                v2=[]
                spec_price=[]
                quantity_range=[]
                for obj in productSpecs:
                    v1.append(getattr(obj,'price'))
                    spec_desc_1.append(getattr(obj,'spec_desc_1'))
                    spec_desc_2.append(getattr(obj,'spec_desc_2'))
                    spec_dec_1_items.append(getattr(obj,'spec_dec_1_items'))
                    spec_dec_2_items.append(getattr(obj,'spec_dec_2_items'))
                    spec_quantity.append(getattr(obj,'quantity'))

                    spec_price.append(getattr(obj,'price'))
                    quantity_range.append(getattr(obj,'quantity'))
                min_price=min(spec_price)
                max_price=max(spec_price)
                min_quantity=min(quantity_range)
                max_quantity=max(quantity_range)
                productSpecPriceInfo = {
                    "min_price":min_price,
                    "max_price":max_price
                }
                productSpecQuantityInfo = {
                    "min_quantity":min_quantity,
                    "max_quantity":max_quantity,
                    "sum_quantity":sum(spec_quantity)
                }
                spec_price_dict={"spec_price":[]}
                spec_price_dict["spec_price"].append(productSpecPriceInfo)
                spec_price_dict={"quantity_range":[]}
                spec_price_dict["quantity_range"].append(productSpecQuantityInfo)
                # for productShipment in productShipments:
                #     shipment_desc.append(getattr(productShipment,'shipment_desc'))
                #     shipment_price.append(getattr(productShipment,'price'))
                #     onoff.append(getattr(productShipment,'onoff'))

                for picObj in productPics:
                    v2.append(getattr(picObj,'product_pic'))

                productInfo.update({'price':v1})
                productInfo.update({'spec_desc_1':spec_desc_1})
                productInfo.update({'spec_desc_2':spec_desc_2})
                productInfo.update({'spec_dec_1_items':spec_dec_1_items})
                productInfo.update({'spec_dec_2_items':spec_dec_2_items})
                productInfo.update({'spec_quantity':spec_quantity})
                productInfo.update(productSpecPriceInfo)
                productInfo.update(productSpecQuantityInfo)
                # productInfo.update({'shipment_desc':shipment_desc})
                # productInfo.update({'shipment_price':shipment_price})
                # productInfo.update({'onoff':onoff})
                productInfo.update({'pic_path':v2})   
                responseData['data'].append(productInfo)
                # responseData['data'].append(spec_price_dict)
                # responseData['data'].append(productSpecPriceInfo)
                shipment_dict={"product_shipment_list":[]}
                
                shipment_price=[]

                for productShipment in productShipments:
                    productShipmentInfo = {
                        "shipment_desc":productShipment.shipment_desc,
                        "price":productShipment.price,
                        "onoff":productShipment.onoff,
                    }
                    shipment_dict["product_shipment_list"].append(productShipmentInfo)
                    shipment_price.append(productShipment.price)
                shipment_min_price=min(shipment_price)
                shipment_max_price=max(shipment_price)

                productInfo.update({'shipment_min_price':shipment_min_price})
                productInfo.update({'shipment_max_price':shipment_max_price})
                productInfo.update(shipment_dict)
                # responseData['data'].append(shipment_dict)

                responseData['ret_val'] = '已取得商品資訊!'
            elif products[0].product_spec_on=='n':
                
                productPics=models.Selected_Product_Pic.objects.filter(product_id=id)
                productSpecs=models.Product_Spec.objects.filter(product_id=id)
                productShipments=models.Product_Shipment_Method.objects.filter(product_id=id)
                productCategorys=models.Product_Category.objects.filter(id=getCategoryID[0])
                productSubCategorys=models.Product_Sub_Category.objects.filter(id=getSubCategoryID[0])
                
                for product in products:       
                    productInfo = {
                        'id': product.id,
                        'product_category_id': product.product_category_id,
                        'product_sub_category_id': product.product_sub_category_id,  
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
                        'product_status':product.product_status,
                        'length':product.length,
                        'width':product.width,
                        'height':product.height,
                        'like':product.like,
                        'seen':product.seen,
                        'sold_quantity':product.sold_quantity,
                        'product_spec_on':product.product_spec_on,
                        # 'c_category_name':productCategorys.c_product_category,
                        # 'c_sub_category_name':productSubCategorys.c_product_sub_category
                    }
                # category_name=[]
                # sub_category_name=[]
                print(productCategorys)
                for productCategory in productCategorys:
                    category_name=(getattr(productCategory,'c_product_category'))
                productInfo.update({'c_product_category':category_name}) 
                
                for productSubCategory in productSubCategorys:
                    sub_category_name=(getattr(productSubCategory,'c_product_sub_category'))
                productInfo.update({'c_sub_product_category':sub_category_name}) 
                v2=[]
                for picObj in productPics:
                    v2.append(getattr(picObj,'product_pic'))

                productInfo.update({'pic_path':v2})   
                responseData['data'].append(productInfo)
                shipment_dict={"product_shipment_list":[]}
                print(productShipments)
                shipment_price=[]

                for productShipment in productShipments:
                    productShipmentInfo = {
                        "shipment_desc":productShipment.shipment_desc,
                        "price":productShipment.price,
                        "onoff":productShipment.onoff,
                    }
                    shipment_dict["product_shipment_list"].append(productShipmentInfo)
                    shipment_price.append(productShipment.price)
                shipment_min_price=min(shipment_price)
                shipment_max_price=max(shipment_price)

                productInfo.update({'shipment_min_price':shipment_min_price})
                productInfo.update({'shipment_max_price':shipment_max_price})
                productInfo.update(shipment_dict)
                # responseData['data'].append(shipment_dict)

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
        quantity = request.POST.get('quantity', 0)
        product_description = request.POST.get('product_description', '')
        product_price = request.POST.get('product_price', 0)
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
        # 商品規格
        product_spec_list=json.loads(request.POST.get('product_spec_list'))
        
        # print(product_spec_list["product_spec_list"][3]["price"])
        
        # 商品運送方式
        shipment_method=json.loads(request.POST.get('shipment_method'))
        
        if response_data['status'] == 0:
            if not(product_title):
                response_data['status'] = -1
                response_data['ret_val'] = '未填寫產品標題!'
            elif len(product_title)>50:
                response_data['status'] = -1
                response_data['ret_val'] = '產品標題過長'
                

        if response_data['status'] == 0:
            try:
                product = models.Product.objects.get(id=id)
                # productSpec= models.Product_Spec.objects.filter(product_id=id)
                # productShipment= models.Product_Shipment_Method.objects.filter(product_id=id)
            except:
                response_data['status'] = -1
                response_data['ret_val'] = '找不到此編號的商品!'
        if response_data['status'] == 0:
            if product_spec_on=='y':
                product = models.Product.objects.get(id=id)
                product.product_category_id = product_category_id
                product.product_sub_category_id = product_sub_category_id
                product.product_title = product_title
                product.quantity=-1
                product.product_price=-1
                product.product_description = product_description
                product.shipping_fee = shipping_fee
                product.weight = weight
                product.new_secondhand=new_secondhand
                product.length=length
                product.width=width
                product.height=height
                product.longterm_stock_up=longterm_stock_up
                product.product_status=product_status
                product.product_spec_on=product_spec_on
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
                    if shipment_method[i]["onoff"]=="on" or shipment_method[i]["onoff"]=="True" or shipment_method[i]["onoff"]==True or shipment_method[i]["onoff"]=="true":
                        models.Product_Shipment_Method.objects.create(
                            product_id=id,
                            shipment_desc=shipment_method[i]["shipment_desc"],
                            price=shipment_method[i]["price"],
                            onoff="on",
                            shop_id=shipment_method[i]["shop_id"]
                        )
                    elif shipment_method[i]["onoff"]=="off" or shipment_method[i]["onoff"]=="False" or shipment_method[i]["onoff"]==False or shipment_method[i]["onoff"]=="false":
                        models.Product_Shipment_Method.objects.create(
                            product_id=id,
                            shipment_desc=shipment_method[i]["shipment_desc"],
                            price=shipment_method[i]["price"],
                            onoff="off",
                            shop_id=shipment_method[i]["shop_id"]
                        )
                response_data['status'] = 0
                response_data['ret_val'] = '商品更新成功!'
            elif product_spec_on=='n':
                product = models.Product.objects.get(id=id)
                product.product_category_id = product_category_id
                product.product_sub_category_id = product_sub_category_id
                product.product_title = product_title
                product.quantity=quantity
                product.product_price=product_price
                product.product_description = product_description
                product.shipping_fee = shipping_fee
                product.weight = weight
                product.new_secondhand=new_secondhand
                product.length=length
                product.width=width
                product.height=height
                product.longterm_stock_up=longterm_stock_up
                product.product_status=product_status
                product.product_spec_on=product_spec_on
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
                    
                # models.Product_Spec.objects.filter(product_id=id).delete()
                models.Product_Shipment_Method.objects.filter(product_id=id).delete()
                #     # 寫入資料庫(規格)
                # for i in range(len(product_spec_list["product_spec_list"])):
                #     models.Product_Spec.objects.create(
                #         product_id=id,
                #         spec_desc_1=product_spec_list["product_spec_list"][i]["spec_desc_1"],
                #         spec_desc_2=product_spec_list["product_spec_list"][i]["spec_desc_2"],
                #         spec_dec_1_items=product_spec_list["product_spec_list"][i]["spec_dec_1_items"],
                #         spec_dec_2_items=product_spec_list["product_spec_list"][i]["spec_dec_2_items"],
                #         price=product_spec_list["product_spec_list"][i]["price"],
                #         quantity=product_spec_list["product_spec_list"][i]["quantity"],
                #     )
                
                for i in range(len(shipment_method)):
                    if shipment_method[i]["onoff"]=="on" or shipment_method[i]["onoff"]=="True" or shipment_method[i]["onoff"]==True or shipment_method[i]["onoff"]=="true":
                        models.Product_Shipment_Method.objects.create(
                            product_id=id,
                            shipment_desc=shipment_method[i]["shipment_desc"],
                            price=shipment_method[i]["price"],
                            onoff="on",
                            shop_id=shipment_method[i]["shop_id"]
                        )
                    elif shipment_method[i]["onoff"]=="off" or shipment_method[i]["onoff"]=="False" or shipment_method[i]["onoff"]==False or shipment_method[i]["onoff"]=="false":
                        models.Product_Shipment_Method.objects.create(
                            product_id=id,
                            shipment_desc=shipment_method[i]["shipment_desc"],
                            price=shipment_method[i]["price"],
                            onoff="off",
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
        product_price = request.POST.get('product_price', 0)
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
            elif len(product_title)>50:
                response_data['status'] = -4
                response_data['ret_val'] = '產品標題過長'

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


        # if response_data['status']==0:
        #     if product_spec_list["product_spec_list"][0]["spec_desc_1"]=="" and product_spec_list["product_spec_list"][0]["spec_desc_2"]=="" and product_spec_list["product_spec_list"][0]["price"]==0 and product_spec_list["product_spec_list"][0]["quantity"]==0:
        #         response_data['status'] = -87
        #         response_data['ret_val'] = '未傳送商品規格!'
        # if response_data['status']==0:
        #     if shipment_method[0]["price"]==0 and shipment_method[0]["shop_id"]==0 and shipment_method[0]["shipment_desc"]=="" and shipment_method[0]["onoff"]=="on":
        #         response_data['status'] = -88
        #         response_data['ret_val'] = '未傳送商品運輸方式!'

        productPicURL=[]
        
        if response_data['status'] == 0:
            for filename, product_pic_list in request.FILES.lists():
                print(filename,product_pic_list)
                name = request.FILES[filename].name
                print(name)
                for f in product_pic_list:

                    # upload_file(product_pic,'images/product/',suffix="img")
                    productPicURL.append(upload_file(f,'images/product_test/',suffix="img"))
            if product_spec_on=="y":    

                models.Product.objects.create(
                    shop_id=shop_id, 
                    product_category_id=product_category_id, 
                    product_sub_category_id=product_sub_category_id, 
                    product_title=product_title, 
                    quantity=-1, 
                    product_description=product_description, 
                    # product_country_code=product_country_code, 
                    # product_price=product_price, 
                    product_price=-1, 
                    shipping_fee=shipping_fee, 
                    weight=weight,
                    new_secondhand=new_secondhand,
                    user_id=user_id,
                    length=length, 
                    width=width, 
                    height=height,
                    longterm_stock_up=longterm_stock_up,
                    product_status=product_status,
                    product_spec_on=product_spec_on,
                    like=0,
                    seen=0,
                    sold_quantity=0
                )
                #傳回product_id
                products=models.Product.objects.filter(
                    shop_id=shop_id, 
                    product_category_id=product_category_id, 
                    product_sub_category_id=product_sub_category_id, 
                    product_title=product_title, 
                    # quantity=quantity, 
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
            elif product_spec_on=="n":   
                models.Product.objects.create(
                    shop_id=shop_id, 
                    product_category_id=product_category_id, 
                    product_sub_category_id=product_sub_category_id, 
                    product_title=product_title, 
                    quantity=quantity, 
                    product_description=product_description, 
                    # product_country_code=product_country_code, 
                    # product_price=product_price, 
                    product_price=product_price, 
                    shipping_fee=shipping_fee, 
                    weight=weight,
                    new_secondhand=new_secondhand,
                    user_id=user_id,
                    length=length, 
                    width=width, 
                    height=height,
                    longterm_stock_up=longterm_stock_up,
                    product_status=product_status,
                    product_spec_on=product_spec_on,
                    like=0,
                    seen=0,
                    sold_quantity=0
                )
                #傳回product_id
                products=models.Product.objects.filter(
                    shop_id=shop_id, 
                    product_category_id=product_category_id, 
                    product_sub_category_id=product_sub_category_id, 
                    product_title=product_title, 
                    # quantity=quantity, 
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
            
            for i in range(len(shipment_method)):
                if shipment_method[i]["onoff"]=="on" or shipment_method[i]["onoff"]=="True" or shipment_method[i]["onoff"]==True or shipment_method[i]["onoff"]=="true":
                    
                    models.Product_Shipment_Method.objects.create(
                        product_id=getProductID[0]['id'],
                        shipment_desc=shipment_method[i]["shipment_desc"],
                        price=shipment_method[i]["price"],
                        onoff="on",
                        shop_id=shipment_method[i]["shop_id"]
                    )
                elif shipment_method[i]["onoff"]=="off" or shipment_method[i]["onoff"]=="False" or shipment_method[i]["onoff"]==False or shipment_method[i]["onoff"]=="false":
                    
                    models.Product_Shipment_Method.objects.create(
                        product_id=getProductID[0]['id'],
                        shipment_desc=shipment_method[i]["shipment_desc"],
                        price=shipment_method[i]["price"],
                        onoff="off",
                        shop_id=shipment_method[i]["shop_id"]
                    )
                else:
                    print('error')
                    response_data['ret_val'] = '產品新增失敗!'
                    response_data['status'] = -1

            response_data['ret_val'] = '產品新增成功!'
            response_data['status'] = 0
                    # response_data['pic_upload'] = 'success'
          
        #------------
    return JsonResponse(response_data)

# 上架/下架
def update_product_status(request): 
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        id=request.POST.get('id')
        status=request.POST.get('status')
        products=models.Product.objects.filter(id=id)
        if status=="draft":
            for product in products:
                product.product_status='active'
                product.save()
        elif status=="active":
            for product in products:
                product.product_status='draft'
                product.save()

        responseData['status'] =0
        responseData['ret_val'] = '上架/下架成功!'

    return JsonResponse(responseData)
    # pass
# 上架/下架
def update_product_status_forAndroid(request): 
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        id=request.POST.get('id')
        status=request.POST.get('status')
        products=models.Product.objects.filter(id=id)
        if status=="draft":
            for product in products:
                product.product_status='draft'
                product.save()
        elif status=="active":
            for product in products:
                product.product_status='active'
                product.save()

        responseData['status'] =0
        responseData['ret_val'] = '上架/下架成功!'

    return JsonResponse(responseData)
    # pass

# 上架/下架
def delete_product(request,id): 
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        products=models.Product.objects.filter(id=id).filter(is_delete='N')
        for product in products:
            product.is_delete='Y'
            product.save()

        products_check=models.Product.objects.filter(id=id).filter(is_delete='Y')
        if len(products_check)==1:

            responseData['status'] =0
            responseData['ret_val'] = '刪除商品成功!'
        else:
            responseData['status'] =-1
            responseData['ret_val'] = '刪除商品失敗!'

    return JsonResponse(responseData)
    # pass
    
# 取得首頁的推薦商品清單
def product_analytics(request,id): #userid
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }

    if request.method == 'GET':
        if responseData['status'] == 0:
            if id=="null" or id is None:
                # shop=models.Shop.objects.get(id=id)
                products = models.Product.objects.filter(product_status='active').filter(is_delete='N').order_by('-created_at')[:12]#.filter(like__gt=0) 
                getProductID=[]
                getShopID=[]
                for product in products:
                    getProductID.append(product.id)
                for shop in products:
                    getShopID.append(shop.id)

                productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                for product in products:   
                    if product.product_spec_on=='y':
                        for productPic in productPics:
                            # for productSpec in productSpecs:    
                            if product.id==productPic.product_id : 
                                productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                productShopId=models.Shop.objects.get(id=product.shop_id)

                                productInfo = {
                                    'product_id': product.id,
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
                                    'product_status':product.product_status,
                                    'pic_path':productPic.product_pic,
                                    'product_spec_on':product.product_spec_on,
                                    'shop_id':productShopId.id,
                                    'shop_title':productShopId.shop_title,
                                    'liked':'N'
                                    # 'price' : productSpec.price
                                }
                                #responseData['data'].append(productInfo)    
                                # responseData['data']['price'] = {}
                                v = []
                                price_range=[]
                                quantity_range=[]
                                quantity_sum=[]
                                for obj in productSpecs:
                                    # if product.id==productSpecs.product.id:
                                    # responseData['data'].update({'price':obj.price})
                                    v.append(getattr(obj,'price'))
                                    price_range.append(getattr(obj,'price'))
                                    quantity_range.append(getattr(obj,'quantity'))
                                    quantity_sum.append(getattr(obj,'quantity'))
                                min_price=min(price_range)
                                max_price=max(price_range)
                            
                                productInfo.update({'price':v})   
                                productInfo.update({'min_price':min_price})   
                                productInfo.update({'max_price':max_price})  
                                productInfo.update({'min_quantity':min(quantity_range)}) 
                                productInfo.update({'max_quantity':max(quantity_range)})
                                productInfo.update({'sum_quantity': sum(quantity_sum)}) 
                                responseData['data'].append(productInfo)

                                models.Product_Browsed.objects.create(
                                    id=uuid.uuid4(),
                                    product_id=product.id
                                )

                    elif product.product_spec_on=='n':   
                        for productPic in productPics:
                            # for productSpec in productSpecs:    
                            if product.id==productPic.product_id : 
                                # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                productShopId=models.Shop.objects.get(id=product.shop_id)
                                productInfo = {
                                    'product_id': product.id,
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
                                    'product_status':product.product_status,
                                    'pic_path':productPic.product_pic,
                                    'product_spec_on':product.product_spec_on,
                                    'shop_id':productShopId.id,
                                    'shop_title':productShopId.shop_title,
                                    'liked':'N'
                                    # 'price' : productSpec.price
                                }
                                #responseData['data'].append(productInfo)    
                                # responseData['data']['price'] = {}
                                productInfo.update({'min_price':product.product_price}) 
                                productInfo.update({'max_price':product.product_price}) 
                                productInfo.update({'min_quantity':product.quantity}) 
                                productInfo.update({'max_quantity':product.quantity})
                                productInfo.update({'sum_quantity':product.quantity})
                                responseData['data'].append(productInfo) 
                                models.Product_Browsed.objects.create(
                                    id=uuid.uuid4(),
                                    product_id=product.id
                                )            

                responseData['ret_val'] = '已取得商品清單!'
            else:
                print("userID登入")
                # shop=models.Shop.objects.get(id=id)
                products = models.Product.objects.filter(product_status='active').filter(is_delete='N').order_by('-created_at')[:12]#.filter(like__gt=0) 
                getProductID=[]
                getShopID=[]
                for product in products:
                    getProductID.append(product.id)
                for shop in products:
                    getShopID.append(shop.id)

                productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')
                for product in products:   
                    if product.product_spec_on=='y':
                        for productPic in productPics:
  
                            if product.id==productPic.product_id : 
                                
                                productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                productShopId=models.Shop.objects.get(id=product.shop_id)
                                productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=id)

                                productInfo = {
                                    'product_id': product.id,
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
                                    'product_status':product.product_status,
                                    'pic_path':productPic.product_pic,
                                    'product_spec_on':product.product_spec_on,
                                    'shop_id':productShopId.id,
                                    'shop_title':productShopId.shop_title,
                                    'liked':'N'
                                }

                                v = []
                                price_range=[]
                                quantity_range=[]
                                quantity_sum=[]
                                for obj in productSpecs:
                                    v.append(getattr(obj,'price'))
                                    price_range.append(getattr(obj,'price'))
                                    quantity_range.append(getattr(obj,'quantity'))
                                    quantity_sum.append(getattr(obj,'quantity'))
                                min_price=min(price_range)
                                max_price=max(price_range)
                            
                                productInfo.update({'price':v})   
                                productInfo.update({'min_price':min_price})   
                                productInfo.update({'max_price':max_price})  
                                productInfo.update({'min_quantity':min(quantity_range)}) 
                                productInfo.update({'max_quantity':max(quantity_range)})
                                productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                for productLike in productLikes:
                                    if productLike.product_id==product.id :
                                        productInfo.update({'liked': 'Y'})
                                    else:
                                        productInfo.update({'liked': 'N'})

                                responseData['data'].append(productInfo)

                                models.Product_Browsed.objects.create(
                                    id=uuid.uuid4(),
                                    product_id=product.id, 
                                    user_id=id
                                )

                    elif product.product_spec_on=='n':   
                        for productPic in productPics:  
                            if product.id==productPic.product_id : 
                                
                                productShopId=models.Shop.objects.get(id=product.shop_id)
                                productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=id)
                                
                                productInfo = {
                                    'product_id': product.id,
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
                                    'product_status':product.product_status,
                                    'pic_path':productPic.product_pic,
                                    'product_spec_on':product.product_spec_on,
                                    'shop_id':productShopId.id,
                                    'shop_title':productShopId.shop_title,
                                    'liked':'N'
                                }

                                productInfo.update({'min_price':product.product_price}) 
                                productInfo.update({'max_price':product.product_price}) 
                                productInfo.update({'min_quantity':product.quantity}) 
                                productInfo.update({'max_quantity':product.quantity})
                                productInfo.update({'sum_quantity':product.quantity})
                                
                                for productLike in productLikes:
                                    if productLike.product_id==product.id :
                                        productInfo.update({'liked': 'Y'})
                                    else:
                                        productInfo.update({'liked': 'N'})

                                responseData['data'].append(productInfo)

                                models.Product_Browsed.objects.create(
                                    id=uuid.uuid4(),
                                    product_id=product.id, 
                                    user_id=id
                                )      
               
                responseData['ret_val'] = '已取得商品清單!'
    return JsonResponse(responseData)
# 取得買家商店商品清單
def shop_product_analytics(request,shop_id,mode): #userid
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }

    if request.method == 'POST':
        if responseData['status'] == 0:
            user_id=request.POST.get('user_id', '')
            if mode=="new":
                if user_id is None or user_id=='' or user_id=="":
                    # shop=models.Shop.objects.get(id=id)
                    products = models.Product.objects.filter(shop_id=shop_id).filter(product_status='active').filter(is_delete='N').order_by('-created_at')[:12]#.filter(like__gt=0) 
                    getProductID=[]
                    getShopID=[]
                    for product in products:
                        getProductID.append(product.id)
                    for shop in products:
                        getShopID.append(shop.id)
                    
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products:   
                        if product.product_spec_on=='y':
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)

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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'liked':'N',
                                        'rating':0
                                        # 'price' : productSpec.price
                                    }
                                    #responseData['data'].append(productInfo)    
                                    # responseData['data']['price'] = {}
                                    v = []
                                    price_range=[]
                                    quantity_range=[]
                                    quantity_sum=[]
                                    for obj in productSpecs:
                                        # if product.id==productSpecs.product.id:
                                        # responseData['data'].update({'price':obj.price})
                                        v.append(getattr(obj,'price'))
                                        price_range.append(getattr(obj,'price'))
                                        quantity_range.append(getattr(obj,'quantity'))
                                        quantity_sum.append(getattr(obj,'quantity'))
                                    min_price=min(price_range)
                                    max_price=max(price_range)
                                
                                    productInfo.update({'price':v})   
                                    productInfo.update({'min_price':min_price})   
                                    productInfo.update({'max_price':max_price})  
                                    productInfo.update({'min_quantity':min(quantity_range)}) 
                                    productInfo.update({'max_quantity':max(quantity_range)})
                                    productInfo.update({'sum_quantity': sum(quantity_sum)}) 
                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id
                                    )

                        elif product.product_spec_on=='n':   
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'liked':'N',
                                        'rating':0
                                        # 'price' : productSpec.price
                                    }
                                    #responseData['data'].append(productInfo)    
                                    # responseData['data']['price'] = {}
                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    productInfo.update({'min_quantity':product.quantity}) 
                                    productInfo.update({'max_quantity':product.quantity})
                                    productInfo.update({'sum_quantity':product.quantity})
                                    responseData['data'].append(productInfo) 
                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id
                                    )            

                    responseData['ret_val'] = '已取得商品清單!'
                else:
                    print("userID登入")
                    # shop=models.Shop.objects.get(id=id)
                    products = models.Product.objects.filter(product_status='active').filter(is_delete='N').order_by('-created_at')[:12]#.filter(like__gt=0) 
                    getProductID=[]
                    getShopID=[]
                    for product in products:
                        getProductID.append(product.id)
                    for shop in products:
                        getShopID.append(shop.id)

                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')
                    for product in products:   
                        if product.product_spec_on=='y':
                            for productPic in productPics:
    
                                if product.id==productPic.product_id : 
                                    
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
                                    productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)

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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'rating':0
                                    }

                                    v = []
                                    price_range=[]
                                    quantity_range=[]
                                    quantity_sum=[]
                                    for obj in productSpecs:
                                        v.append(getattr(obj,'price'))
                                        price_range.append(getattr(obj,'price'))
                                        quantity_range.append(getattr(obj,'quantity'))
                                        quantity_sum.append(getattr(obj,'quantity'))
                                    min_price=min(price_range)
                                    max_price=max(price_range)
                                
                                    productInfo.update({'price':v})   
                                    productInfo.update({'min_price':min_price})   
                                    productInfo.update({'max_price':max_price})  
                                    productInfo.update({'min_quantity':min(quantity_range)}) 
                                    productInfo.update({'max_quantity':max(quantity_range)})
                                    productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                    for productLike in productLikes:
                                        if productLike.product_id==product.id :
                                            productInfo.update({'liked': 'Y'})
                                        else:
                                            productInfo.update({'liked': 'N'})

                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id, 
                                        user_id=user_id
                                    )

                        elif product.product_spec_on=='n':   
                            for productPic in productPics:  
                                if product.id==productPic.product_id : 
                                    
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
                                    productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                    
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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'rating':0
                                    }

                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    productInfo.update({'min_quantity':product.quantity}) 
                                    productInfo.update({'max_quantity':product.quantity})
                                    productInfo.update({'sum_quantity':product.quantity})
                                    
                                    for productLike in productLikes:
                                        if productLike.product_id==product.id :
                                            productInfo.update({'liked': 'Y'})
                                        else:
                                            productInfo.update({'liked': 'N'})

                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id, 
                                        user_id=user_id
                                    )      
                                            
                    responseData['ret_val'] = '已取得商品清單!'
            elif mode=="top_sale":
                if user_id is None or user_id=='' or user_id=="":
                    # shop=models.Shop.objects.get(id=id)
                    products = models.Product.objects.filter(shop_id=shop_id).filter(product_status='active').filter(is_delete='N')[:12]#.filter(like__gt=0) 
                    
                    getProductID=[]
                    getShopID=[]
                    for product in products:
                        getProductID.append(product.id)
                    for shop in products:
                        getShopID.append(shop.id)

                    # productQuantitys=models.Shop_Order_Details.objects.filter(product_id__in=getProductID).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
                    # print(productQuantitys)
                    # from django.db.models import Avg
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products:   
                        if product.product_spec_on=='y':
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
                                    productOveralls=models.Product_Rate.objects.filter(product_id=product.id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
                                    productQuantitys=models.Shop_Order_Details.objects.filter(product_id=product.id).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
                                    productInfo = {
                                        'id': product.id,
                                        'product_category_id': product.product_category_id, 
                                        'product_title': product.product_title,
                                        'quantity': product.quantity, 
                                        'product_description': product.product_description, 
                                        'product_price': product.product_price, 
                                        'shipping_fee': product.shipping_fee, 
                                        # 'created_at': product.created_at, 
                                        # 'updated_at': product.updated_at,
                                        'weight':product.weight,
                                        'longterm_stock_up':product.longterm_stock_up,
                                        'new_secondhand':product.new_secondhand,
                                        'length':product.length,
                                        'width':product.width,
                                        'height':product.height,
                                        'like':product.like,
                                        'seen':product.seen,
                                        'sold_quantity':product.sold_quantity,
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'liked':'N',
                                        'rating':0,
                                        'productQuantity':0
                                    }
                                    #responseData['data'].append(productInfo)    
                                    # responseData['data']['price'] = {}
                                    v = []
                                    price_range=[]
                                    quantity_range=[]
                                    quantity_sum=[]
                                    for obj in productSpecs:
                                        # if product.id==productSpecs.product.id:
                                        # responseData['data'].update({'price':obj.price})
                                        v.append(getattr(obj,'price'))
                                        price_range.append(getattr(obj,'price'))
                                        quantity_range.append(getattr(obj,'quantity'))
                                        quantity_sum.append(getattr(obj,'quantity'))
                                    min_price=min(price_range)
                                    max_price=max(price_range)
                                
                                    productInfo.update({'price':v})   
                                    productInfo.update({'min_price':min_price})   
                                    productInfo.update({'max_price':max_price})  
                                    productInfo.update({'min_quantity':min(quantity_range)}) 
                                    productInfo.update({'max_quantity':max(quantity_range)})
                                    productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                    for productOverall in productOveralls:
                                        if productOverall["product_id"]==product.id :
                                            productInfo.update({'rating': productOverall["rating"]})
                                        else:
                                            productInfo.update({'rating': 0})
                                    
                                    for productQuantity in productQuantitys:
                                        if productQuantity["product_id"]==product.id :
                                            productInfo.update({'productQuantity': productQuantity["sale_quantity"]})
                                        else:
                                            productInfo.update({'productQuantity': 0})
                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id
                                    )

                        elif product.product_spec_on=='n':   
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
                                    productOveralls=models.Product_Rate.objects.filter(product_id=product.id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
                                    productQuantitys=models.Shop_Order_Details.objects.filter(product_id=product.id).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
                                    productInfo = {
                                        'id': product.id,
                                        'product_category_id': product.product_category_id, 
                                        'product_title': product.product_title,
                                        'quantity': product.quantity, 
                                        'product_description': product.product_description, 
                                        'product_price': product.product_price, 
                                        'shipping_fee': product.shipping_fee, 
                                        # 'created_at': product.created_at, 
                                        # 'updated_at': product.updated_at,
                                        'weight':product.weight,
                                        'longterm_stock_up':product.longterm_stock_up,
                                        'new_secondhand':product.new_secondhand,
                                        'length':product.length,
                                        'width':product.width,
                                        'height':product.height,
                                        'like':product.like,
                                        'seen':product.seen,
                                        'sold_quantity':product.sold_quantity,
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'liked':'N',
                                        'rating':0,
                                        'productQuantity':0
                                    }
                                    #responseData['data'].append(productInfo)    
                                    # responseData['data']['price'] = {}
                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    productInfo.update({'min_quantity':product.quantity}) 
                                    productInfo.update({'max_quantity':product.quantity})
                                    productInfo.update({'sum_quantity':product.quantity})

                                    for productOverall in productOveralls:
                                        if productOverall["product_id"]==product.id :
                                            productInfo.update({'rating': productOverall["rating"]})
                                            
                                        else:
                                            productInfo.update({'rating': 0})
                                    
                                    for productQuantity in productQuantitys:
                                        if productQuantity["product_id"]==product.id :
                                            productInfo.update({'productQuantity': productQuantity["sale_quantity"]})
                                        else:
                                            productInfo.update({'productQuantity': 0})

                                    responseData['data'].append(productInfo) 
                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id
                                    )      
                    # print(responseData['data'])                      
                    responseData['data']=sorted(responseData['data'], key=lambda quantitySort : quantitySort['productQuantity'],reverse=True)
                    responseData['ret_val'] = '已取得商品清單!'
                else:
                    print("userID登入")
                    # shop=models.Shop.objects.get(id=id)
                    products = models.Product.objects.filter(shop_id=shop_id).filter(product_status='active').filter(is_delete='N')[:12]#.filter(like__gt=0) 
                    getProductID=[]
                    getShopID=[]
                    for product in products:
                        getProductID.append(product.id)
                    for shop in products:
                        getShopID.append(shop.id)

                    productOveralls=models.Product_Rate.objects.filter(product_id__in=getProductID).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
                    
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')
                    for product in products:   
                        if product.product_spec_on=='y':
                            for productPic in productPics:
    
                                if product.id==productPic.product_id : 
                                    # print(product.id)
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
                                    productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                    productQuantitys=models.Shop_Order_Details.objects.filter(product_id=product.id).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'rating':0,
                                        'liked':'N',
                                        'productQuantity':0
                                    }

                                    v = []
                                    price_range=[]
                                    quantity_range=[]
                                    quantity_sum=[]
                                    for obj in productSpecs:
                                        v.append(getattr(obj,'price'))
                                        price_range.append(getattr(obj,'price'))
                                        quantity_range.append(getattr(obj,'quantity'))
                                        quantity_sum.append(getattr(obj,'quantity'))
                                    min_price=min(price_range)
                                    max_price=max(price_range)
                                
                                    productInfo.update({'price':v})   
                                    productInfo.update({'min_price':min_price})   
                                    productInfo.update({'max_price':max_price})  
                                    productInfo.update({'min_quantity':min(quantity_range)}) 
                                    productInfo.update({'max_quantity':max(quantity_range)})
                                    productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                    for productLike in productLikes:
                                        if productLike.product_id==product.id :
                                            productInfo.update({'liked': 'Y'})
                                        else:
                                            productInfo.update({'liked': 'N'})
                                    
                                    for productQuantity in productQuantitys:
                                        
                                        if productQuantity["product_id"]==product.id :
                                            
                                            productInfo.update({'productQuantity': productQuantity["sale_quantity"]})
                                        else:
                                            
                                            productInfo.update({'productQuantity': 0})

                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id, 
                                        user_id=user_id
                                    )

                        elif product.product_spec_on=='n':   
                            for productPic in productPics:  
                                if product.id==productPic.product_id : 
                                    
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
                                    productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                    productQuantitys=models.Shop_Order_Details.objects.filter(product_id=product.id).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'rating':0,
                                        'liked':'N',
                                        'productQuantity':0
                                    }

                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    productInfo.update({'min_quantity':product.quantity}) 
                                    productInfo.update({'max_quantity':product.quantity})
                                    productInfo.update({'sum_quantity':product.quantity})
                                    
                                    for productLike in productLikes:
                                      
                                        if productLike.product_id==product.id :
                                            productInfo.update({'liked': 'Y'})
                                        else:
                                            productInfo.update({'liked': 'N'})
                                    
                                    for productQuantity in productQuantitys:
                                        if productQuantity["product_id"]==product.id :
                                            
                                            productInfo.update({'productQuantity': productQuantity["sale_quantity"]})
                                        else:
                                            
                                            productInfo.update({'productQuantity': 0})

                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id, 
                                        user_id=user_id
                                    )      
                    responseData['data']=sorted(responseData['data'], key=lambda ratingSort : ratingSort['productQuantity'],reverse=True)                        
                    responseData['ret_val'] = '已取得商品清單!'
            elif mode=="lower_price":
                if user_id is None or user_id=='' or user_id=="":
                    # shop=models.Shop.objects.get(id=id)
                    products = models.Product.objects.filter(shop_id=shop_id).filter(product_status='active').filter(is_delete='N')#.order_by('-price')[:12]#.filter(like__gt=0) 
                    getProductID=[]
                    getShopID=[]
                    for product in products:
                        getProductID.append(product.id)
                    for shop in products:
                        getShopID.append(shop.id)

                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products:   
                        if product.product_spec_on=='y':
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)

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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'liked':'N',
                                        'rating':0
                                        # 'price' : productSpec.price
                                    }
                                    #responseData['data'].append(productInfo)    
                                    # responseData['data']['price'] = {}
                                    v = []
                                    price_range=[]
                                    quantity_range=[]
                                    quantity_sum=[]
                                    for obj in productSpecs:
                                        # if product.id==productSpecs.product.id:
                                        # responseData['data'].update({'price':obj.price})
                                        v.append(getattr(obj,'price'))
                                        price_range.append(getattr(obj,'price'))
                                        quantity_range.append(getattr(obj,'quantity'))
                                        quantity_sum.append(getattr(obj,'quantity'))
                                    min_price=min(price_range)
                                    max_price=max(price_range)
                                
                                    productInfo.update({'price':v})   
                                    productInfo.update({'min_price':min_price})   
                                    productInfo.update({'max_price':max_price})  
                                    productInfo.update({'min_quantity':min(quantity_range)}) 
                                    productInfo.update({'max_quantity':max(quantity_range)})
                                    productInfo.update({'sum_quantity': sum(quantity_sum)}) 
                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id
                                    )

                        elif product.product_spec_on=='n':   
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'liked':'N',
                                        'rating':0
                                        # 'price' : productSpec.price
                                    }
                                    #responseData['data'].append(productInfo)    
                                    # responseData['data']['price'] = {}
                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    productInfo.update({'min_quantity':product.quantity}) 
                                    productInfo.update({'max_quantity':product.quantity})
                                    productInfo.update({'sum_quantity':product.quantity})
                                    responseData['data'].append(productInfo) 
                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id
                                    )            
                    # print(sorted(responseData['data'], key=lambda priceSort : priceSort['max_price'],reverse=True)) #,reverse=True
                    responseData['data']=sorted(responseData['data'], key=lambda priceSort : priceSort['max_price'])
                    responseData['ret_val'] = '已取得商品清單!'
                else:
                    print("userID登入")
                    # shop=models.Shop.objects.get(id=id)
                    products = models.Product.objects.filter(product_status='active').filter(is_delete='N').order_by('-created_at')[:12]#.filter(like__gt=0) 
                    getProductID=[]
                    getShopID=[]
                    for product in products:
                        getProductID.append(product.id)
                    for shop in products:
                        getShopID.append(shop.id)

                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')
                    for product in products:   
                        if product.product_spec_on=='y':
                            for productPic in productPics:
    
                                if product.id==productPic.product_id : 
                                    
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
                                    productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)

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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'rating':0
                                    }

                                    v = []
                                    price_range=[]
                                    quantity_range=[]
                                    quantity_sum=[]
                                    for obj in productSpecs:
                                        v.append(getattr(obj,'price'))
                                        price_range.append(getattr(obj,'price'))
                                        quantity_range.append(getattr(obj,'quantity'))
                                        quantity_sum.append(getattr(obj,'quantity'))
                                    min_price=min(price_range)
                                    max_price=max(price_range)
                                
                                    productInfo.update({'price':v})   
                                    productInfo.update({'min_price':min_price})   
                                    productInfo.update({'max_price':max_price})  
                                    productInfo.update({'min_quantity':min(quantity_range)}) 
                                    productInfo.update({'max_quantity':max(quantity_range)})
                                    productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                    for productLike in productLikes:
                                        if productLike.product_id==product.id :
                                            productInfo.update({'liked': 'Y'})
                                        else:
                                            productInfo.update({'liked': 'N'})

                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id, 
                                        user_id=user_id
                                    )

                        elif product.product_spec_on=='n':   
                            for productPic in productPics:  
                                if product.id==productPic.product_id : 
                                    
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
                                    productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                    
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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'rating':0
                                    }

                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    productInfo.update({'min_quantity':product.quantity}) 
                                    productInfo.update({'max_quantity':product.quantity})
                                    productInfo.update({'sum_quantity':product.quantity})
                                    
                                    for productLike in productLikes:
                                        if productLike.product_id==product.id :
                                            productInfo.update({'liked': 'Y'})
                                        else:
                                            productInfo.update({'liked': 'N'})

                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id, 
                                        user_id=user_id
                                    )      

                    # sorted(A, key = lambda user: user['name'])
                    # print(sorted(responseData['data'], key=lambda priceSort : priceSort['max_price'],reverse=True)) #,reverse=True
                    responseData['data']=sorted(responseData['data'], key=lambda priceSort : priceSort['max_price'])
                    responseData['ret_val'] = '已取得商品清單!'


            elif mode=="higher_price":
                if user_id is None or user_id=='' or user_id=="":
                    # shop=models.Shop.objects.get(id=id)
                    products = models.Product.objects.filter(shop_id=shop_id).filter(product_status='active').filter(is_delete='N')#.order_by('-price')[:12]#.filter(like__gt=0) 
                    getProductID=[]
                    getShopID=[]
                    for product in products:
                        getProductID.append(product.id)
                    for shop in products:
                        getShopID.append(shop.id)

                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products:   
                        if product.product_spec_on=='y':
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)

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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'liked':'N',
                                        'rating':0
                                        # 'price' : productSpec.price
                                    }
                                    #responseData['data'].append(productInfo)    
                                    # responseData['data']['price'] = {}
                                    v = []
                                    price_range=[]
                                    quantity_range=[]
                                    quantity_sum=[]
                                    for obj in productSpecs:
                                        # if product.id==productSpecs.product.id:
                                        # responseData['data'].update({'price':obj.price})
                                        v.append(getattr(obj,'price'))
                                        price_range.append(getattr(obj,'price'))
                                        quantity_range.append(getattr(obj,'quantity'))
                                        quantity_sum.append(getattr(obj,'quantity'))
                                    min_price=min(price_range)
                                    max_price=max(price_range)
                                
                                    productInfo.update({'price':v})   
                                    productInfo.update({'min_price':min_price})   
                                    productInfo.update({'max_price':max_price})  
                                    productInfo.update({'min_quantity':min(quantity_range)}) 
                                    productInfo.update({'max_quantity':max(quantity_range)})
                                    productInfo.update({'sum_quantity': sum(quantity_sum)}) 
                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id
                                    )

                        elif product.product_spec_on=='n':   
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'liked':'N',
                                        'rating':0
                                        # 'price' : productSpec.price
                                    }
                                    #responseData['data'].append(productInfo)    
                                    # responseData['data']['price'] = {}
                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    productInfo.update({'min_quantity':product.quantity}) 
                                    productInfo.update({'max_quantity':product.quantity})
                                    productInfo.update({'sum_quantity':product.quantity})
                                    responseData['data'].append(productInfo) 
                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id
                                    )            
                    # print(sorted(responseData['data'], key=lambda priceSort : priceSort['max_price'])) #,reverse=True
                    responseData['data']=sorted(responseData['data'], key=lambda priceSort : priceSort['max_price'],reverse=True)
                    responseData['ret_val'] = '已取得商品清單!'
                else:
                    print("userID登入")
                    # shop=models.Shop.objects.get(id=id)
                    products = models.Product.objects.filter(product_status='active').filter(is_delete='N').order_by('-created_at')[:12]#.filter(like__gt=0) 
                    getProductID=[]
                    getShopID=[]
                    for product in products:
                        getProductID.append(product.id)
                    for shop in products:
                        getShopID.append(shop.id)

                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')
                    for product in products:   
                        if product.product_spec_on=='y':
                            for productPic in productPics:
    
                                if product.id==productPic.product_id : 
                                    
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
                                    productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)

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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'rating':0
                                    }

                                    v = []
                                    price_range=[]
                                    quantity_range=[]
                                    quantity_sum=[]
                                    for obj in productSpecs:
                                        v.append(getattr(obj,'price'))
                                        price_range.append(getattr(obj,'price'))
                                        quantity_range.append(getattr(obj,'quantity'))
                                        quantity_sum.append(getattr(obj,'quantity'))
                                    min_price=min(price_range)
                                    max_price=max(price_range)
                                
                                    productInfo.update({'price':v})   
                                    productInfo.update({'min_price':min_price})   
                                    productInfo.update({'max_price':max_price})  
                                    productInfo.update({'min_quantity':min(quantity_range)}) 
                                    productInfo.update({'max_quantity':max(quantity_range)})
                                    productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                    for productLike in productLikes:
                                        if productLike.product_id==product.id :
                                            productInfo.update({'liked': 'Y'})
                                        else:
                                            productInfo.update({'liked': 'N'})

                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id, 
                                        user_id=user_id
                                    )

                        elif product.product_spec_on=='n':   
                            for productPic in productPics:  
                                if product.id==productPic.product_id : 
                                    
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
                                    productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                    
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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'rating':0
                                    }

                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    productInfo.update({'min_quantity':product.quantity}) 
                                    productInfo.update({'max_quantity':product.quantity})
                                    productInfo.update({'sum_quantity':product.quantity})
                                    
                                    for productLike in productLikes:
                                        if productLike.product_id==product.id :
                                            productInfo.update({'liked': 'Y'})
                                        else:
                                            productInfo.update({'liked': 'N'})

                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id, 
                                        user_id=user_id
                                    )      

                    # sorted(A, key = lambda user: user['name'])
                    # print(sorted(responseData['data'], key=lambda priceSort : priceSort['max_price'])) #,reverse=True
                    responseData['data']=sorted(responseData['data'], key=lambda priceSort : priceSort['max_price'],reverse=True)
                    responseData['ret_val'] = '已取得商品清單!'
            elif mode=="overall":
                if user_id is None or user_id=='' or user_id=="":
                    # shop=models.Shop.objects.get(id=id)
                    products = models.Product.objects.filter(shop_id=shop_id).filter(product_status='active').filter(is_delete='N')[:12]#.filter(like__gt=0) 
                    
                    getProductID=[]
                    getShopID=[]
                    for product in products:
                        getProductID.append(product.id)
                    for shop in products:
                        getShopID.append(shop.id)

                    # productOveralls=models.Product_Rate.objects.filter(product_id__in=getProductID).values('product_id').annotate(ratings=Avg('rating')).order_by('-rating')
                    # from django.db.models import Avg
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                    for product in products:   
                        if product.product_spec_on=='y':
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
                                    productOveralls=models.Product_Rate.objects.filter(product_id=product.id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'liked':'N',
                                        'rating':0
                                    }
                                    #responseData['data'].append(productInfo)    
                                    # responseData['data']['price'] = {}
                                    v = []
                                    price_range=[]
                                    quantity_range=[]
                                    quantity_sum=[]
                                    for obj in productSpecs:
                                        # if product.id==productSpecs.product.id:
                                        # responseData['data'].update({'price':obj.price})
                                        v.append(getattr(obj,'price'))
                                        price_range.append(getattr(obj,'price'))
                                        quantity_range.append(getattr(obj,'quantity'))
                                        quantity_sum.append(getattr(obj,'quantity'))
                                    min_price=min(price_range)
                                    max_price=max(price_range)
                                
                                    productInfo.update({'price':v})   
                                    productInfo.update({'min_price':min_price})   
                                    productInfo.update({'max_price':max_price})  
                                    productInfo.update({'min_quantity':min(quantity_range)}) 
                                    productInfo.update({'max_quantity':max(quantity_range)})
                                    productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                    for productOverall in productOveralls:
                                        if productOverall["product_id"]==product.id :
                                            productInfo.update({'rating': productOverall["rating"]})
                                        else:
                                            productInfo.update({'rating': 0})

                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id
                                    )

                        elif product.product_spec_on=='n':   
                            for productPic in productPics:
                                # for productSpec in productSpecs:    
                                if product.id==productPic.product_id : 
                                    # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
                                    productOveralls=models.Product_Rate.objects.filter(product_id=product.id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'liked':'N',
                                        'rating':0
                                    }
                                    #responseData['data'].append(productInfo)    
                                    # responseData['data']['price'] = {}
                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    productInfo.update({'min_quantity':product.quantity}) 
                                    productInfo.update({'max_quantity':product.quantity})
                                    productInfo.update({'sum_quantity':product.quantity})

                                    for productOverall in productOveralls:
                                        if productOverall["product_id"]==product.id :
                                            productInfo.update({'rating': productOverall["rating"]})
                                        else:
                                            productInfo.update({'rating': 0})

                                    responseData['data'].append(productInfo) 
                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id
                                    )            
                    responseData['data']=sorted(responseData['data'], key=lambda ratingSort : ratingSort['rating'],reverse=True)
                    responseData['ret_val'] = '已取得商品清單!'
                else:
                    print("userID登入")
                    # shop=models.Shop.objects.get(id=id)
                    products = models.Product.objects.filter(shop_id=shop_id).filter(product_status='active').filter(is_delete='N')[:12]#.filter(like__gt=0) 
                    getProductID=[]
                    getShopID=[]
                    for product in products:
                        getProductID.append(product.id)
                    for shop in products:
                        getShopID.append(shop.id)

                    # productOveralls=models.Product_Rate.objects.filter(product_id__in=getProductID).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
                    # print(productOveralls)
                    productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')
                    for product in products:   
                        if product.product_spec_on=='y':
                            for productPic in productPics:
    
                                if product.id==productPic.product_id : 
                                    # print(product.id)
                                    productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
                                    productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                    productOveralls=models.Product_Rate.objects.filter(product_id=product.id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'liked':'N',
                                        'rating':0
                                    }

                                    v = []
                                    price_range=[]
                                    quantity_range=[]
                                    quantity_sum=[]
                                    for obj in productSpecs:
                                        v.append(getattr(obj,'price'))
                                        price_range.append(getattr(obj,'price'))
                                        quantity_range.append(getattr(obj,'quantity'))
                                        quantity_sum.append(getattr(obj,'quantity'))
                                    min_price=min(price_range)
                                    max_price=max(price_range)
                                
                                    productInfo.update({'price':v})   
                                    productInfo.update({'min_price':min_price})   
                                    productInfo.update({'max_price':max_price})  
                                    productInfo.update({'min_quantity':min(quantity_range)}) 
                                    productInfo.update({'max_quantity':max(quantity_range)})
                                    productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                    for productLike in productLikes:
                                        if productLike.product_id==product.id :
                                            productInfo.update({'liked': 'Y'})
                                        else:
                                            productInfo.update({'liked': 'N'})
                                    
                                    for productOverall in productOveralls:
                                        
                                        if productOverall["product_id"]==product.id :
                                            
                                            productInfo.update({'rating': productOverall["rating"]})
                                        else:
                                            
                                            productInfo.update({'rating': 0})

                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id, 
                                        user_id=user_id
                                    )

                        elif product.product_spec_on=='n':   
                            for productPic in productPics:  
                                if product.id==productPic.product_id : 
                                    # print(product.id)
                                    productShopId=models.Shop.objects.get(id=product.shop_id)
                                    productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                    productOveralls=models.Product_Rate.objects.filter(product_id=product.id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
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
                                        'product_status':product.product_status,
                                        'pic_path':productPic.product_pic,
                                        'product_spec_on':product.product_spec_on,
                                        'shop_id':productShopId.id,
                                        'shop_title':productShopId.shop_title,
                                        'liked':'N',
                                        'rating':0
                                    }

                                    productInfo.update({'min_price':product.product_price}) 
                                    productInfo.update({'max_price':product.product_price}) 
                                    productInfo.update({'min_quantity':product.quantity}) 
                                    productInfo.update({'max_quantity':product.quantity})
                                    productInfo.update({'sum_quantity':product.quantity})
                                    
                                    for productLike in productLikes:
                                        # print(productLike)
                                        if productLike.product_id==product.id :
                                            productInfo.update({'liked': 'Y'})
                                        else:
                                            productInfo.update({'liked': 'N'})
                                    
                                    for productOverall in productOveralls:
                                       
                                        # print(product.id)
                                        if productOverall["product_id"]==product.id :
                                            
                                            productInfo.update({'rating': productOverall["rating"]})
                                        else:
                                            
                                            productInfo.update({'rating': 0})

                                    responseData['data'].append(productInfo)

                                    models.Product_Browsed.objects.create(
                                        id=uuid.uuid4(),
                                        product_id=product.id, 
                                        user_id=user_id
                                    )      
                    responseData['data']=sorted(responseData['data'], key=lambda ratingSort : ratingSort['rating'],reverse=True)                        
                    responseData['ret_val'] = '已取得商品清單!'
            else:
                responseData['status'] =-1
                responseData['ret_val'] = '未輸入排序規則'
    return JsonResponse(responseData)

# 取得首頁的推薦商品清單(分頁)
def product_analytics_pages(request,mode): #userid
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    
    if request.method == 'POST':
        if responseData['status'] == 0:
            user_id=request.POST.get('user_id','')
            max_seq=request.POST.get('max_seq', '')
            
            # key_word=request.POST.get('key_word', '')
            # print(key_word)
            if int(max_seq)==0:                 
                if mode=="new":
                    print("new")
                    if user_id=='' or user_id is None or user_id=="":
                        user_tempID=uuid.uuid4()
                        models.Product_Analytics.objects.filter(user_id=user_tempID).delete() 
                        # products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_title__contains=key_word).order_by('-created_at') 
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N').order_by('-created_at') 

                        for i in range(len(products)):
                            productPics=models.Selected_Product_Pic.objects.filter(product_id=products[i].id).filter(cover='y')      
                            if products[i].product_spec_on=='y':
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if products[i].id==productPic.product_id : 
                                        productSpecs=models.Product_Spec.objects.filter(product_id=products[i].id)
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                        models.Product_Browsed.objects.create(
                                            id=uuid.uuid4(),
                                            product_id=products[i].id
                                        )
                                
                                        models.Product_Analytics.objects.create(
                                            id=uuid.uuid4(),                                            
                                            product_id=products[i].id,
                                            user_id=user_tempID,
                                            seq=i,
                                            pic_path=productPic.product_pic,
                                            product_title=products[i].product_title,
                                            shop_title=productShopId.shop_title,
                                            min_price=min_price,
                                            max_price=max_price,
                                            liked='N'
                                        )


                            elif products[i].product_spec_on=='n':   
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if products[i].id==productPic.product_id : 
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        
                                        models.Product_Browsed.objects.create(
                                            id=uuid.uuid4(),
                                            product_id=products[i].id
                                        )    
                                        models.Product_Analytics.objects.create(
                                            id=uuid.uuid4(),
                                            product_id=products[i].id,
                                            user_id=user_tempID,
                                            seq=i,
                                            pic_path=productPic.product_pic,
                                            product_title=products[i].product_title,
                                            shop_title=productShopId.shop_title,
                                            min_price=products[i].product_price,
                                            max_price=products[i].product_price,                                            
                                            liked='N'
                                        )        
                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_tempID).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage)
                        responseData['ret_val'] = '取得商品分頁資訊'
                        # responseData['ret_val'] = '已取得商品清單!'
                        
                    else:
                        print("userID登入")
                        # shop=models.Shop.objects.get(id=id)
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N').order_by('-created_at')#.filter(like__gt=0) 
                        models.Product_Analytics.objects.filter(user_id=user_id).delete() 

                        for i in range(len(products)):   
                            productPics=models.Selected_Product_Pic.objects.filter(product_id=products[i].id).filter(cover='y') 
                            if products[i].product_spec_on=='y':
                                for productPic in productPics:
        
                                    if products[i].id==productPic.product_id : 
                                        productSpecs=models.Product_Spec.objects.filter(product_id=products[i].id)
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=products[i].id).filter(user_id=user_id)

                                        productInfo = {
                                            'id': products[i].id,
                                            'product_title': products[i].product_title,
                                            'product_price': products[i].product_price, 
                                            'pic_path':productPic.product_pic,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0,
                                            'liked':'N'
                                        }

                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                        for productLike in productLikes:
                                            if productLike.product_id==products[i].id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})

                                        # responseData['data'].append(productInfo)
                                        models.Product_Browsed.objects.create(
                                            id=uuid.uuid4(),
                                            product_id=products[i].id, 
                                            user_id=user_id
                                        )

                                        models.Product_Analytics.objects.create(
                                            id=uuid.uuid4(),
                                            product_id=productInfo["id"],
                                            user_id=user_id,
                                            seq=i,
                                            pic_path=productInfo["pic_path"],
                                            product_title=productInfo["product_title"],
                                            shop_title=productInfo["shop_title"],
                                            min_price=productInfo["min_price"],
                                            max_price=productInfo["max_price"],
                                            liked=productInfo["liked"]
                                        ) 
                            elif products[i].product_spec_on=='n':   
                                for productPic in productPics:  
                                    if products[i].id==productPic.product_id : 
                                    
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=products[i].id).filter(user_id=user_id)
                                        
                                        productInfo = {
                                            'id': products[i].id,
                                            'product_title': products[i].product_title,
                                            'product_price': products[i].product_price, 
                                            'pic_path':productPic.product_pic,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0,
                                            'liked':'N'
                                        }

                                        productInfo.update({'min_price':products[i].product_price}) 
                                        productInfo.update({'max_price':products[i].product_price}) 
                                        productInfo.update({'min_quantity':products[i].quantity}) 
                                        productInfo.update({'max_quantity':products[i].quantity})
                                        productInfo.update({'sum_quantity':products[i].quantity})
                                        
                                        for productLike in productLikes:
                                            if productLike.product_id==products[i].id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})

                                        # responseData['data'].append(productInfo)

                                        models.Product_Browsed.objects.create(
                                            id=uuid.uuid4(),
                                            product_id=products[i].id, 
                                            user_id=user_id
                                        )     

                                        models.Product_Analytics.objects.create(
                                            id=uuid.uuid4(),
                                            product_id=productInfo["id"],
                                            user_id=user_id,                                    
                                            seq=i,
                                            pic_path=productInfo["pic_path"],
                                            product_title=productInfo["product_title"],
                                            shop_title=productInfo["shop_title"],
                                            min_price=productInfo["min_price"],
                                            max_price=productInfo["max_price"],
                                            liked=productInfo["liked"]
                                        )         
                        
                        

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_id).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage)

                        responseData['ret_val'] = '取得商品分頁資訊'
                elif mode=="top_sale":
                    top_sale_data=[] #for sorting
                    if user_id=='' or user_id is None or user_id=="":
                        # shop=models.Shop.objects.get(id=id)
                        user_tempID=uuid.uuid4()
                        models.Product_Analytics.objects.filter(user_id=user_tempID).delete() 
                        # products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_title__contains=key_word)
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N')
                        # getProductID=[]
                        # getShopID=[]
                        # for product in products:
                        #     getProductID.append(product.id)
                        # for shop in products:
                        #     getShopID.append(shop.id)

                        # productQuantitys=models.Shop_Order_Details.objects.filter(product_id__in=getProductID).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
                        # from django.db.models import Avg
                        
                        for i in range(len(products)):  
                            productPics=models.Selected_Product_Pic.objects.filter(product_id=products[i].id).filter(cover='y')     
                            if products[i].product_spec_on=='y':
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if products[i].id==productPic.product_id : 
                                        productSpecs=models.Product_Spec.objects.filter(product_id=products[i].id)
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        productQuantitys=models.Shop_Order_Details.objects.filter(product_id=products[i].id).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
                                        productOveralls=models.Product_Rate.objects.filter(product_id=products[i].id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
                                        productInfo = {
                                            'id': products[i].id,
                                            # 'product_category_id': product.product_category_id, 
                                            'product_title': products[i].product_title,
                                            'quantity': products[i].quantity, 
                                            # 'product_description': product.product_description, 
                                            'product_price': products[i].product_price, 
                                            # 'shipping_fee': product.shipping_fee, 
                                            # 'created_at': product.created_at, 
                                            # 'updated_at': product.updated_at,
                                            # 'weight':product.weight,
                                            # 'longterm_stock_up':product.longterm_stock_up,
                                            # 'new_secondhand':product.new_secondhand,
                                            # 'length':product.length,
                                            # 'width':product.width,
                                            # 'height':product.height,
                                            # 'like':product.like,
                                            # 'seen':product.seen,
                                            # 'sold_quantity':product.sold_quantity,
                                            # 'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':products[i].product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0,
                                            'productQuantity':0
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            # if product.id==productSpecs.product.id:
                                            # responseData['data'].update({'price':obj.price})
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        # productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                        for productOverall in productOveralls:
                                            if productOverall["product_id"]==products[i].id :
                                                productInfo.update({'rating': productOverall["rating"]})
                                            else:
                                                productInfo.update({'rating': 0})

                                        for productQuantity in productQuantitys:
                                            if productQuantity["product_id"]==products[i].id :
                                                
                                                productInfo.update({'productQuantity': productQuantity["sale_quantity"]})
                                            else:
                                                
                                                productInfo.update({'productQuantity': 0})          
                                        top_sale_data.append(productInfo) 

                            elif products[i].product_spec_on=='n':   
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if products[i].id==productPic.product_id : 
                                        # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        productQuantitys=models.Shop_Order_Details.objects.filter(product_id=products[i].id).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
                                        productOveralls=models.Product_Rate.objects.filter(product_id=products[i].id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
                                        productInfo = {
                                            'id': products[i].id,
                                            # 'product_category_id': product.product_category_id, 
                                            'product_title': products[i].product_title,
                                            'quantity': products[i].quantity, 
                                            # 'product_description': product.product_description, 
                                            'product_price': products[i].product_price, 
                                            # 'shipping_fee': product.shipping_fee, 
                                            # 'created_at': product.created_at, 
                                            # 'updated_at': product.updated_at,
                                            # 'weight':product.weight,
                                            # 'longterm_stock_up':product.longterm_stock_up,
                                            # 'new_secondhand':product.new_secondhand,
                                            # 'length':product.length,
                                            # 'width':product.width,
                                            # 'height':product.height,
                                            # 'like':product.like,
                                            # 'seen':product.seen,
                                            # 'sold_quantity':product.sold_quantity,
                                            # 'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':products[i].product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0,
                                            'productQuantity':0
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        productInfo.update({'min_price':products[i].product_price}) 
                                        productInfo.update({'max_price':products[i].product_price}) 
                                        productInfo.update({'min_quantity':products[i].quantity}) 
                                        productInfo.update({'max_quantity':products[i].quantity})
                                        productInfo.update({'sum_quantity':products[i].quantity})

                                        for productOverall in productOveralls:
                                            
                                            if productOverall["product_id"]==products[i].id :
                                                productInfo.update({'rating': productOverall["rating"]})
                                            else:
                                                productInfo.update({'rating': 0})
                                        for productQuantity in productQuantitys:
                                          
                                            if productQuantity["product_id"]==products[i].id :
                                               
                                                productInfo.update({'productQuantity': productQuantity["sale_quantity"]})
                                            else:
                                                
                                                productInfo.update({'productQuantity': 0})
                                        
                                        top_sale_data.append(productInfo)       
                        top_sale_dataFinal=sorted(top_sale_data , key=lambda quantitySort : quantitySort['productQuantity'],reverse=True)
                        for i in range(len(sorted(top_sale_data , key=lambda quantitySort : quantitySort['productQuantity'],reverse=True))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=top_sale_dataFinal[i]["id"],
                                        user_id=user_tempID,
                                        seq=i,
                                        pic_path=top_sale_dataFinal[i]["pic_path"],
                                        product_title=top_sale_dataFinal[i]["product_title"],
                                        shop_title=top_sale_dataFinal[i]["shop_title"],
                                        min_price=top_sale_dataFinal[i]["min_price"],
                                        max_price=top_sale_dataFinal[i]["max_price"],
                                        liked='N'
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=top_sale_dataFinal[i]["id"]
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_tempID).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage)         
                        # responseData['data']=sorted(responseData['data'], key=lambda ratingSort : ratingSort['rating'],reverse=True)
                        responseData['ret_val'] = '已取得商品清單!'
                    else:
                        print("userID登入")
                        models.Product_Analytics.objects.filter(user_id=user_id).delete() 
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N') 
                        # productOveralls=models.Product_Rate.objects.filter(product_id__in=getProductID).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
                        # print(productOveralls)
                        
                        for i in range(len(products)):   
                            productPics=models.Selected_Product_Pic.objects.filter(product_id=products[i].id).filter(cover='y')
                            if products[i].product_spec_on=='y':
                                for productPic in productPics:
        
                                    if products[i].id==productPic.product_id : 
                                        # print(product.id)
                                        productSpecs=models.Product_Spec.objects.filter(product_id=products[i].id)
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=products[i].id).filter(user_id=user_id)
                                        productQuantitys=models.Shop_Order_Details.objects.filter(product_id=products[i].id).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
                                        productInfo = {
                                            'id': products[i].id,
                                            'product_title': products[i].product_title,
                                            'quantity': products[i].quantity, 
                                            'product_price': products[i].product_price,
                                            'pic_path':productPic.product_pic,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0,
                                            'liked':'N',
                                            'productQuantity':0
                                        }

                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                        for productLike in productLikes:
                                            if productLike.product_id==products[i].id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        
                                        for productQuantity in productQuantitys:
                                            print(productQuantity)
                                            # print(product.id)
                                            if productQuantity["product_id"]==products[i].id :
                                                print("success")
                                                productInfo.update({'productQuantity': productQuantity["sale_quantity"]})
                                            else:
                                                print("no sale_quantity")
                                                productInfo.update({'productQuantity': 0})

                                        # responseData['data'].append(productInfo)
                                        top_sale_data.append(productInfo) 


                            elif products[i].product_spec_on=='n':   
                                for productPic in productPics:  
                                    if products[i].id==productPic.product_id : 
                                        # print(product.id)
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=products[i].id).filter(user_id=user_id)
                                        productQuantitys=models.Shop_Order_Details.objects.filter(product_id=products[i].id).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
                                        productInfo = {
                                            'id': products[i].id,
                                            'product_title': products[i].product_title,
                                            'quantity': products[i].quantity, 
                                            'product_price': products[i].product_price,
                                            'pic_path':productPic.product_pic,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0,
                                            'liked':'N',
                                            'productQuantity':0
                                        }

                                        productInfo.update({'min_price':products[i].product_price}) 
                                        productInfo.update({'max_price':products[i].product_price}) 
                                        productInfo.update({'min_quantity':products[i].quantity}) 
                                        productInfo.update({'max_quantity':products[i].quantity})
                                        productInfo.update({'sum_quantity':products[i].quantity})
                                        
                                        for productLike in productLikes:
                                            
                                            if productLike.product_id==products[i].id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        
                                        for productQuantity in productQuantitys:         
                                            if productQuantity["product_id"]==products[i].id :
                                              
                                                productInfo.update({'productQuantity': productQuantity["sale_quantity"]})
                                            else:
                                                
                                                productInfo.update({'productQuantity': 0})

                                        top_sale_data.append(productInfo)

                        top_sale_dataFinal=sorted(top_sale_data , key=lambda quantitySort : quantitySort['productQuantity'],reverse=True)
                        for i in range(len(sorted(top_sale_data , key=lambda quantitySort : quantitySort['productQuantity'],reverse=True))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=top_sale_dataFinal[i]["id"],
                                        user_id=user_id,
                                        seq=i,
                                        pic_path=top_sale_dataFinal[i]["pic_path"],
                                        product_title=top_sale_dataFinal[i]["product_title"],
                                        shop_title=top_sale_dataFinal[i]["shop_title"],
                                        min_price=top_sale_dataFinal[i]["min_price"],
                                        max_price=top_sale_dataFinal[i]["max_price"],
                                        liked=top_sale_dataFinal[i]["liked"]
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=top_sale_data[i]["id"],
                                user_id=user_id
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_id).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage)                         
                        responseData['ret_val'] = '已取得商品清單!'
                elif mode=="lower_price":
                    lower_price_data=[]
                    if user_id=='' or user_id is None or user_id=="":
                        user_tempID=uuid.uuid4()
                        models.Product_Analytics.objects.filter(user_id__isnull=user_tempID).delete() 
                        # products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_title__contains=key_word)

                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N')#.order_by('-price')[:12]#.filter(like__gt=0) 
                        getProductID=[]
                        getShopID=[]
                        for product in products:
                            getProductID.append(product.id)
                        for shop in products:
                            getShopID.append(shop.id)

                        productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                        for product in products:   
                            if product.product_spec_on=='y':
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if product.id==productPic.product_id : 
                                        productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)

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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                            # 'price' : productSpec.price
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            # if product.id==productSpecs.product.id:
                                            # responseData['data'].update({'price':obj.price})
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 
                                        # responseData['data'].append(productInfo)
                                        lower_price_data.append(productInfo) 
                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id
                                        # )

                            elif product.product_spec_on=='n':   
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if product.id==productPic.product_id : 
                                        # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                            # 'price' : productSpec.price
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        productInfo.update({'min_price':product.product_price}) 
                                        productInfo.update({'max_price':product.product_price}) 
                                        productInfo.update({'min_quantity':product.quantity}) 
                                        productInfo.update({'max_quantity':product.quantity})
                                        productInfo.update({'sum_quantity':product.quantity})
                                        # responseData['data'].append(productInfo) 
                                        lower_price_data.append(productInfo) 
     
                        lower_price_dataFinal=sorted(lower_price_data , key=lambda priceSort : priceSort['max_price'])
                        for i in range(len(sorted(lower_price_data , key=lambda priceSort : priceSort['max_price']))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=lower_price_dataFinal[i]["id"],
                                        user_id=user_tempID,
                                        seq=i,
                                        pic_path=lower_price_dataFinal[i]["pic_path"],
                                        product_title=lower_price_dataFinal[i]["product_title"],
                                        shop_title=lower_price_dataFinal[i]["shop_title"],
                                        min_price=lower_price_dataFinal[i]["min_price"],
                                        max_price=lower_price_dataFinal[i]["max_price"],
                                        liked='N'
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=lower_price_dataFinal[i]["id"]
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_tempID).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'price':productAnalytic.price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage)         
                        # responseData['data']=sorted(responseData['data'], key=lambda ratingSort : ratingSort['rating'],reverse=True)
                        responseData['ret_val'] = '已取得商品清單!'
                    else:
                        print("userID登入")
                        # shop=models.Shop.objects.get(id=id)
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N')#.filter(like__gt=0) 
                        models.Product_Analytics.objects.filter(user_id=user_id).delete() 
                        getProductID=[]
                        getShopID=[]
                        for product in products:
                            getProductID.append(product.id)
                        for shop in products:
                            getShopID.append(shop.id)

                        productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')
                        for product in products:   
                            if product.product_spec_on=='y':
                                for productPic in productPics:
        
                                    if product.id==productPic.product_id : 
                                        productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)

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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0
                                        }

                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                        for productLike in productLikes:
                                            if productLike.product_id==product.id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        lower_price_data.append(productInfo) 

                                        # responseData['data'].append(productInfo)

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id, 
                                        #     user_id=user_id
                                        # )

                            elif product.product_spec_on=='n':   
                                for productPic in productPics:  
                                    if product.id==productPic.product_id : 
                                        
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                        
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0
                                        }

                                        productInfo.update({'min_price':product.product_price}) 
                                        productInfo.update({'max_price':product.product_price}) 
                                        productInfo.update({'min_quantity':product.quantity}) 
                                        productInfo.update({'max_quantity':product.quantity})
                                        productInfo.update({'sum_quantity':product.quantity})
                                        
                                        for productLike in productLikes:
                                            if productLike.product_id==product.id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        lower_price_data.append(productInfo) 

                                        # responseData['data'].append(productInfo)

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id, 
                                        #     user_id=user_id
                                        # )      

                        lower_price_dataFinal=sorted(lower_price_data , key=lambda priceSort : priceSort['max_price'])
                        for i in range(len(sorted(lower_price_data , key=lambda priceSort : priceSort['max_price']))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=lower_price_dataFinal[i]["id"],
                                        user_id=user_id,
                                        seq=i,
                                        pic_path=lower_price_dataFinal[i]["pic_path"],
                                        product_title=lower_price_dataFinal[i]["product_title"],
                                        shop_title=lower_price_dataFinal[i]["shop_title"],
                                        min_price=lower_price_dataFinal[i]["min_price"],
                                        max_price=lower_price_dataFinal[i]["max_price"],
                                        liked='N'
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=lower_price_dataFinal[i]["id"],
                                user_id=user_id
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_id).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage) 
                        responseData['ret_val'] = '已取得商品清單!'


                elif mode=="higher_price":
                    lower_price_data=[]
                    if user_id=='' or user_id is None or user_id=="":
                        user_tempID=uuid.uuid4()
                        models.Product_Analytics.objects.filter(user_id=user_tempID).delete() 
                        # products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_title__contains=key_word)

                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N')#.order_by('-price')[:12]#.filter(like__gt=0) 
                        getProductID=[]
                        getShopID=[]
                        for product in products:
                            getProductID.append(product.id)
                        for shop in products:
                            getShopID.append(shop.id)

                        productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                        for product in products:   
                            if product.product_spec_on=='y':
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if product.id==productPic.product_id : 
                                        productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)

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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                            # 'price' : productSpec.price
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            # if product.id==productSpecs.product.id:
                                            # responseData['data'].update({'price':obj.price})
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 
                                        # responseData['data'].append(productInfo)
                                        lower_price_data.append(productInfo) 
                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id
                                        # )

                            elif product.product_spec_on=='n':   
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if product.id==productPic.product_id : 
                                        # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                        }

                                        productInfo.update({'min_price':product.product_price}) 
                                        productInfo.update({'max_price':product.product_price}) 
                                        productInfo.update({'min_quantity':product.quantity}) 
                                        productInfo.update({'max_quantity':product.quantity})
                                        productInfo.update({'sum_quantity':product.quantity})
                                        lower_price_data.append(productInfo) 
                        lower_price_dataFinal=sorted(lower_price_data , key=lambda priceSort : priceSort['max_price'],reverse=True)
                        for i in range(len(sorted(lower_price_data , key=lambda priceSort : priceSort['max_price']))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=lower_price_dataFinal[i]["id"],
                                        user_id=user_tempID,
                                        seq=i,
                                        pic_path=lower_price_dataFinal[i]["pic_path"],
                                        product_title=lower_price_dataFinal[i]["product_title"],
                                        shop_title=lower_price_dataFinal[i]["shop_title"],
                                        min_price=lower_price_dataFinal[i]["min_price"],
                                        max_price=lower_price_dataFinal[i]["max_price"],
                                        liked='N'
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=lower_price_dataFinal[i]["id"]
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_tempID).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage)         
                        # responseData['data']=sorted(responseData['data'], key=lambda ratingSort : ratingSort['rating'],reverse=True)
                        responseData['ret_val'] = '已取得商品清單!'
                    else:
                        print("userID登入")
                        # shop=models.Shop.objects.get(id=id)
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N')#.filter(like__gt=0) 
                        models.Product_Analytics.objects.filter(user_id=user_id).delete() 
                        getProductID=[]
                        getShopID=[]
                        for product in products:
                            getProductID.append(product.id)
                        for shop in products:
                            getShopID.append(shop.id)

                        productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')
                        for product in products:   
                            if product.product_spec_on=='y':
                                for productPic in productPics:
        
                                    if product.id==productPic.product_id : 
                                        
                                        productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)

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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0
                                        }

                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                        for productLike in productLikes:
                                            if productLike.product_id==product.id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        lower_price_data.append(productInfo) 

                                        # responseData['data'].append(productInfo)

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id, 
                                        #     user_id=user_id
                                        # )

                            elif product.product_spec_on=='n':   
                                for productPic in productPics:  
                                    if product.id==productPic.product_id : 
                                        
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                        
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0
                                        }

                                        productInfo.update({'min_price':product.product_price}) 
                                        productInfo.update({'max_price':product.product_price}) 
                                        productInfo.update({'min_quantity':product.quantity}) 
                                        productInfo.update({'max_quantity':product.quantity})
                                        productInfo.update({'sum_quantity':product.quantity})
                                        
                                        for productLike in productLikes:
                                            if productLike.product_id==product.id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        lower_price_data.append(productInfo) 

                                        # responseData['data'].append(productInfo)

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id, 
                                        #     user_id=user_id
                                        # )      

                        lower_price_dataFinal=sorted(lower_price_data , key=lambda priceSort : priceSort['max_price'],reverse=True)
                        for i in range(len(sorted(lower_price_data , key=lambda priceSort : priceSort['max_price']))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=lower_price_dataFinal[i]["id"],
                                        user_id=user_id,
                                        seq=i,
                                        pic_path=lower_price_dataFinal[i]["pic_path"],
                                        product_title=lower_price_dataFinal[i]["product_title"],
                                        shop_title=lower_price_dataFinal[i]["shop_title"],
                                        min_price=lower_price_dataFinal[i]["min_price"],
                                        max_price=lower_price_dataFinal[i]["max_price"],
                                        liked='N'
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=lower_price_dataFinal[i]["id"],
                                user_id=user_id
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_id).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage) 
                        responseData['ret_val'] = '已取得商品清單!'
                elif mode=="overall":
                    overall_data=[]
                    if user_id=='' or user_id is None or user_id=="":
                        # shop=models.Shop.objects.get(id=id)
                        user_tempID=uuid.uuid4()
                        models.Product_Analytics.objects.filter(user_id=user_tempID).delete() 
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N')#.filter(like__gt=0) 
                        
                        getProductID=[]
                        getShopID=[]
                        for product in products:
                            getProductID.append(product.id)
                        for shop in products:
                            getShopID.append(shop.id)

                        # productOveralls=models.Product_Rate.objects.filter(product_id__in=getProductID).values('product_id').annotate(ratings=Avg('rating')).order_by('-rating')
                        # from django.db.models import Avg
                        productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                        for product in products:   
                            if product.product_spec_on=='y':
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if product.id==productPic.product_id : 
                                        productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productOveralls=models.Product_Rate.objects.filter(product_id=product.id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            # if product.id==productSpecs.product.id:
                                            # responseData['data'].update({'price':obj.price})
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                        for productOverall in productOveralls:
                                            if productOverall["product_id"]==product.id :
                                                productInfo.update({'rating': productOverall["rating"]})
                                            else:
                                                productInfo.update({'rating': 0})

                                        # responseData['data'].append(productInfo)
                                        overall_data.append(productInfo) 

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id
                                        # )

                            elif product.product_spec_on=='n':   
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if product.id==productPic.product_id : 
                                        # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productOveralls=models.Product_Rate.objects.filter(product_id=product.id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        productInfo.update({'min_price':product.product_price}) 
                                        productInfo.update({'max_price':product.product_price}) 
                                        productInfo.update({'min_quantity':product.quantity}) 
                                        productInfo.update({'max_quantity':product.quantity})
                                        productInfo.update({'sum_quantity':product.quantity})

                                        for productOverall in productOveralls:
                                            if productOverall["product_id"]==product.id :
                                                productInfo.update({'rating': productOverall["rating"]})
                                            else:
                                                productInfo.update({'rating': 0})
                                        overall_data.append(productInfo)
                                        # responseData['data'].append(productInfo) 
                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id
                                        # )           
                                        #  
                        overall_data_dataFinal=sorted(overall_data , key=lambda rateSort : rateSort['rating'],reverse=True)
                        for i in range(len(sorted(overall_data , key=lambda rateSort : rateSort['rating']))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=overall_data_dataFinal[i]["id"],
                                        user_id=user_tempID,
                                        seq=i,
                                        pic_path=overall_data_dataFinal[i]["pic_path"],
                                        product_title=overall_data_dataFinal[i]["product_title"],
                                        shop_title=overall_data_dataFinal[i]["shop_title"],
                                        min_price=overall_data_dataFinal[i]["min_price"],
                                        max_price=overall_data_dataFinal[i]["max_price"],
                                        liked='N'
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=overall_data_dataFinal[i]["id"]
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_tempID).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage) 
                        responseData['ret_val'] = '已取得商品清單!'                
                        # responseData['data']=sorted(responseData['data'], key=lambda ratingSort : ratingSort['rating'],reverse=True)
                        # responseData['ret_val'] = '已取得商品清單!'
                    else:
                        print("userID登入")
                        # shop=models.Shop.objects.get(id=id)
                        # user_tempID=uuid.uuid4()
                        models.Product_Analytics.objects.filter(user_id=user_id).delete() 
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N')#.filter(like__gt=0) 
                        getProductID=[]
                        getShopID=[]
                        for product in products:
                            getProductID.append(product.id)
                        for shop in products:
                            getShopID.append(shop.id)

                        # productOveralls=models.Product_Rate.objects.filter(product_id__in=getProductID).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
                        # print(productOveralls)
                        productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')
                        for product in products:   
                            if product.product_spec_on=='y':
                                for productPic in productPics:
        
                                    if product.id==productPic.product_id : 
                                        # print(product.id)
                                        productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                        productOveralls=models.Product_Rate.objects.filter(product_id=product.id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                        }

                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                        for productLike in productLikes:
                                            if productLike.product_id==product.id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        
                                        for productOverall in productOveralls:
                                        
                                            # print(product.id)
                                            if productOverall["product_id"]==product.id :
                                                
                                                productInfo.update({'rating': productOverall["rating"]})
                                            else:
                                                
                                                productInfo.update({'rating': 0})

                                        # responseData['data'].append(productInfo)
                                        overall_data.append(productInfo)

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id, 
                                        #     user_id=user_id
                                        # )

                            elif product.product_spec_on=='n':   
                                for productPic in productPics:  
                                    if product.id==productPic.product_id : 
                                        # print(product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                        productOveralls=models.Product_Rate.objects.filter(product_id=product.id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                        }

                                        productInfo.update({'min_price':product.product_price}) 
                                        productInfo.update({'max_price':product.product_price}) 
                                        productInfo.update({'min_quantity':product.quantity}) 
                                        productInfo.update({'max_quantity':product.quantity})
                                        productInfo.update({'sum_quantity':product.quantity})
                                        
                                        for productLike in productLikes:
                                            # print(productLike)
                                            if productLike.product_id==product.id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        
                                        for productOverall in productOveralls:
                                            
                                            # print(product.id)
                                            if productOverall["product_id"]==product.id :
                                              
                                                productInfo.update({'rating': productOverall["rating"]})
                                            else:
                                                
                                                productInfo.update({'rating': 0})

                                        # responseData['data'].append(productInfo)
                                        overall_data.append(productInfo)

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id, 
                                        #     user_id=user_id
                                        # )      
                        overall_data_dataFinal=sorted(overall_data , key=lambda rateSort : rateSort['rating'],reverse=True)
                        for i in range(len(sorted(overall_data , key=lambda rateSort : rateSort['rating']))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=overall_data_dataFinal[i]["id"],
                                        user_id=user_id,
                                        seq=i,
                                        pic_path=overall_data_dataFinal[i]["pic_path"],
                                        product_title=overall_data_dataFinal[i]["product_title"],
                                        shop_title=overall_data_dataFinal[i]["shop_title"],
                                        min_price=overall_data_dataFinal[i]["min_price"],
                                        max_price=overall_data_dataFinal[i]["max_price"],
                                        liked='N'
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=overall_data_dataFinal[i]["id"],
                                user_id=user_id
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_id).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage) 
                        responseData['ret_val'] = '已取得商品清單!'   
                else:
                    responseData['status'] =-1
                    responseData['ret_val'] = '未輸入排序規則'
            else: #max_seq from 1 to .....
                pageSize=12
                pageStart=int(max_seq)*pageSize
                pageEnd=pageStart+pageSize-1
                if user_id=='' or user_id is None or user_id=="":
                    productAnalytics=models.Product_Analytics.objects.filter(user_id__isnull=True).filter(seq__gte=pageStart).filter(seq__lte=pageEnd).order_by('seq')
                    for productAnalytic in productAnalytics:
                        productInfo = {
                                    'id': productAnalytic.id,
                                    'product_id': productAnalytic.product_id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                        responseData['data'].append(productInfo)
                    responseData['ret_val'] = '取得商品分頁資訊'
                else : #login
                    productAnalytics=models.Product_Analytics.objects.filter(user_id=user_id).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                    for productAnalytic in productAnalytics:
                        productInfo = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                        responseData['data'].append(productInfo)
                    responseData['ret_val'] = '取得商品分頁資訊'

    return JsonResponse(responseData)

# 取得首頁的推薦商品清單(分頁)(含關鍵字)
def product_analytics_pages_keyword(request,mode): #userid
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    
    if request.method == 'POST':
        if responseData['status'] == 0:
            user_id=request.POST.get('user_id','')
            max_seq=request.POST.get('max_seq', '')
            
            key_word=request.POST.get('key_word', '')
            category_id=request.POST.get('category_id','')
            if category_id=='':
                categoryId=''
            else:
                categoryId=category_id
            # print(key_word)
            if int(max_seq)==0:                 
                if mode=="new":
                    print("new")
                    if user_id=='' or user_id is None or user_id=="":
                        user_tempID=uuid.uuid4()
                        models.Product_Analytics.objects.filter(user_id=user_tempID).delete() 
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_title__contains=key_word).filter(product_category_id__contains=categoryId).order_by('-created_at') 

                        for i in range(len(products)):
                            productPics=models.Selected_Product_Pic.objects.filter(product_id=products[i].id).filter(cover='y')      
                            if products[i].product_spec_on=='y':
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if products[i].id==productPic.product_id : 
                                        productSpecs=models.Product_Spec.objects.filter(product_id=products[i].id)
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                        models.Product_Browsed.objects.create(
                                            id=uuid.uuid4(),
                                            product_id=products[i].id
                                        )
                                
                                        models.Product_Analytics.objects.create(
                                            id=uuid.uuid4(),                                            
                                            product_id=products[i].id,
                                            user_id=user_tempID,
                                            seq=i,
                                            pic_path=productPic.product_pic,
                                            product_title=products[i].product_title,
                                            shop_title=productShopId.shop_title,
                                            min_price=min_price,
                                            max_price=max_price,
                                            liked='N'
                                        )


                            elif products[i].product_spec_on=='n':   
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if products[i].id==productPic.product_id : 
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        
                                        models.Product_Browsed.objects.create(
                                            id=uuid.uuid4(),
                                            product_id=products[i].id
                                        )    
                                        models.Product_Analytics.objects.create(
                                            id=uuid.uuid4(),
                                            product_id=products[i].id,
                                            user_id=user_tempID,
                                            seq=i,
                                            pic_path=productPic.product_pic,
                                            product_title=products[i].product_title,
                                            shop_title=productShopId.shop_title,
                                            min_price=products[i].product_price,
                                            max_price=products[i].product_price,
                                            liked='N'
                                        )        
                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_tempID).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage)

                        models.Search_History.objects.create(
                                            id=uuid.uuid4(),
                                            search_category='product',
                                            keyword=key_word
                                        )  
                        responseData['ret_val'] = '取得商品分頁資訊'
                        # responseData['ret_val'] = '已取得商品清單!'
                        
                    else:
                        print("userID登入")
                        # shop=models.Shop.objects.get(id=id)
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_title__contains=key_word).filter(product_category_id=categoryId).order_by('-created_at')#.filter(like__gt=0) 
                        models.Product_Analytics.objects.filter(user_id=user_id).delete() 

                        for i in range(len(products)):   
                            productPics=models.Selected_Product_Pic.objects.filter(product_id=products[i].id).filter(cover='y') 
                            if products[i].product_spec_on=='y':
                                for productPic in productPics:
        
                                    if products[i].id==productPic.product_id : 
                                        productSpecs=models.Product_Spec.objects.filter(product_id=products[i].id)
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=products[i].id).filter(user_id=user_id)

                                        productInfo = {
                                            'id': products[i].id,
                                            'product_title': products[i].product_title,
                                            'product_price': products[i].product_price, 
                                            'pic_path':productPic.product_pic,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0,
                                            'liked':'N'
                                        }

                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                        for productLike in productLikes:
                                            if productLike.product_id==products[i].id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})

                                        # responseData['data'].append(productInfo)
                                        models.Product_Browsed.objects.create(
                                            id=uuid.uuid4(),
                                            product_id=products[i].id, 
                                            user_id=user_id
                                        )

                                        models.Product_Analytics.objects.create(
                                            id=uuid.uuid4(),
                                            product_id=productInfo["id"],
                                            user_id=user_id,
                                            seq=i,
                                            pic_path=productInfo["pic_path"],
                                            product_title=productInfo["product_title"],
                                            shop_title=productInfo["shop_title"],
                                            min_price=min_price,
                                            max_price=max_price,
                                            liked=productInfo["liked"]
                                        ) 
                            elif products[i].product_spec_on=='n':   
                                for productPic in productPics:  
                                    if products[i].id==productPic.product_id : 
                                    
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=products[i].id).filter(user_id=user_id)
                                        
                                        productInfo = {
                                            'id': products[i].id,
                                            'product_title': products[i].product_title,
                                            'product_price': products[i].product_price, 
                                            'pic_path':productPic.product_pic,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0,
                                            'liked':'N'
                                        }

                                        productInfo.update({'min_price':products[i].product_price}) 
                                        productInfo.update({'max_price':products[i].product_price}) 
                                        productInfo.update({'min_quantity':products[i].quantity}) 
                                        productInfo.update({'max_quantity':products[i].quantity})
                                        productInfo.update({'sum_quantity':products[i].quantity})
                                        
                                        for productLike in productLikes:
                                            if productLike.product_id==products[i].id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})

                                        # responseData['data'].append(productInfo)

                                        models.Product_Browsed.objects.create(
                                            id=uuid.uuid4(),
                                            product_id=products[i].id, 
                                            user_id=user_id
                                        )     

                                        models.Product_Analytics.objects.create(
                                            id=uuid.uuid4(),
                                            product_id=productInfo["id"],
                                            user_id=user_id,                                    
                                            seq=i,
                                            pic_path=productInfo["pic_path"],
                                            product_title=productInfo["product_title"],
                                            shop_title=productInfo["shop_title"],
                                            min_price=productInfo["min_price"],
                                            max_price=productInfo["max_price"],
                                            liked=productInfo["liked"]
                                        )         
                        
                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_id).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage)
                        models.Search_History.objects.create(
                                            id=uuid.uuid4(),
                                            search_category='product',
                                            keyword=key_word
                                        )  
                        responseData['ret_val'] = '取得商品分頁資訊'
                elif mode=="top_sale":
                    top_sale_data=[] #for sorting
                    if user_id=='' or user_id is None or user_id=="":
                        # shop=models.Shop.objects.get(id=id)
                        user_tempID=uuid.uuid4()
                        models.Product_Analytics.objects.filter(user_id=user_tempID).delete() 
                        # products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_title__contains=key_word)
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_category_id__contains=categoryId).filter(product_title__contains=key_word)
                        # getProductID=[]
                        # getShopID=[]
                        # for product in products:
                        #     getProductID.append(product.id)
                        # for shop in products:
                        #     getShopID.append(shop.id)

                        # productQuantitys=models.Shop_Order_Details.objects.filter(product_id__in=getProductID).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
                        # from django.db.models import Avg
                        
                        for i in range(len(products)):  
                            productPics=models.Selected_Product_Pic.objects.filter(product_id=products[i].id).filter(cover='y')     
                            if products[i].product_spec_on=='y':
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if products[i].id==productPic.product_id : 
                                        productSpecs=models.Product_Spec.objects.filter(product_id=products[i].id)
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        productQuantitys=models.Shop_Order_Details.objects.filter(product_id=products[i].id).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
                                        productOveralls=models.Product_Rate.objects.filter(product_id=products[i].id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
                                        productInfo = {
                                            'id': products[i].id,
                                            # 'product_category_id': product.product_category_id, 
                                            'product_title': products[i].product_title,
                                            'quantity': products[i].quantity, 
                                            # 'product_description': product.product_description, 
                                            'product_price': products[i].product_price, 
                                            # 'shipping_fee': product.shipping_fee, 
                                            # 'created_at': product.created_at, 
                                            # 'updated_at': product.updated_at,
                                            # 'weight':product.weight,
                                            # 'longterm_stock_up':product.longterm_stock_up,
                                            # 'new_secondhand':product.new_secondhand,
                                            # 'length':product.length,
                                            # 'width':product.width,
                                            # 'height':product.height,
                                            # 'like':product.like,
                                            # 'seen':product.seen,
                                            # 'sold_quantity':product.sold_quantity,
                                            # 'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':products[i].product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0,
                                            'productQuantity':0
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            # if product.id==productSpecs.product.id:
                                            # responseData['data'].update({'price':obj.price})
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        # productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                        for productOverall in productOveralls:
                                            if productOverall["product_id"]==products[i].id :
                                                productInfo.update({'rating': productOverall["rating"]})
                                            else:
                                                productInfo.update({'rating': 0})

                                        for productQuantity in productQuantitys:
                                            if productQuantity["product_id"]==products[i].id :
                                                productInfo.update({'productQuantity': productQuantity["sale_quantity"]})
                                            else:
                                                productInfo.update({'productQuantity': 0})          
                                        top_sale_data.append(productInfo) 

                            elif products[i].product_spec_on=='n':   
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if products[i].id==productPic.product_id : 
                                        # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        productQuantitys=models.Shop_Order_Details.objects.filter(product_id=products[i].id).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
                                        productOveralls=models.Product_Rate.objects.filter(product_id=products[i].id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
                                        productInfo = {
                                            'id': products[i].id,
                                            # 'product_category_id': product.product_category_id, 
                                            'product_title': products[i].product_title,
                                            'quantity': products[i].quantity, 
                                            # 'product_description': product.product_description, 
                                            'product_price': products[i].product_price, 
                                            # 'shipping_fee': product.shipping_fee, 
                                            # 'created_at': product.created_at, 
                                            # 'updated_at': product.updated_at,
                                            # 'weight':product.weight,
                                            # 'longterm_stock_up':product.longterm_stock_up,
                                            # 'new_secondhand':product.new_secondhand,
                                            # 'length':product.length,
                                            # 'width':product.width,
                                            # 'height':product.height,
                                            # 'like':product.like,
                                            # 'seen':product.seen,
                                            # 'sold_quantity':product.sold_quantity,
                                            # 'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':products[i].product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0,
                                            'productQuantity':0
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        productInfo.update({'min_price':products[i].product_price}) 
                                        productInfo.update({'max_price':products[i].product_price}) 
                                        productInfo.update({'min_quantity':products[i].quantity}) 
                                        productInfo.update({'max_quantity':products[i].quantity})
                                        productInfo.update({'sum_quantity':products[i].quantity})

                                        for productOverall in productOveralls:
                                            if productOverall["product_id"]==products[i].id :
                                                productInfo.update({'rating': productOverall["rating"]})
                                            else:
                                                productInfo.update({'rating': 0})
                                        for productQuantity in productQuantitys:
                                            # print(product.id)
                                            if productQuantity["product_id"]==products[i].id :
                                                productInfo.update({'productQuantity': productQuantity["sale_quantity"]})
                                            else:
                                                productInfo.update({'productQuantity': 0})
                                        
                                        top_sale_data.append(productInfo) 
                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=products[i].id
                                        # )
                        # print(top_sale_data)  
                        # print(len(sorted(top_sale_data , key=lambda quantitySort : quantitySort['productQuantity'],reverse=True)))          
                        top_sale_dataFinal=sorted(top_sale_data , key=lambda quantitySort : quantitySort['productQuantity'],reverse=True)
                        for i in range(len(sorted(top_sale_data , key=lambda quantitySort : quantitySort['productQuantity'],reverse=True))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=top_sale_dataFinal[i]["id"],
                                        user_id=user_tempID,
                                        seq=i,
                                        pic_path=top_sale_dataFinal[i]["pic_path"],
                                        product_title=top_sale_dataFinal[i]["product_title"],
                                        shop_title=top_sale_dataFinal[i]["shop_title"],
                                        min_price=top_sale_dataFinal[i]["min_price"],
                                        max_price=top_sale_dataFinal[i]["max_price"],
                                        liked='N'
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=top_sale_dataFinal[i]["id"]
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_tempID).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage)         
                        models.Search_History.objects.create(
                                            id=uuid.uuid4(),
                                            search_category='product',
                                            keyword=key_word
                                        )  
                        responseData['ret_val'] = '已取得商品清單!'
                    else:
                        print("userID登入")
                        models.Product_Analytics.objects.filter(user_id=user_id).delete() 
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_category_id__contains=categoryId).filter(product_title__contains=key_word)
                        # productOveralls=models.Product_Rate.objects.filter(product_id__in=getProductID).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
                        # print(productOveralls)
                        
                        for i in range(len(products)):   
                            productPics=models.Selected_Product_Pic.objects.filter(product_id=products[i].id).filter(cover='y')
                            if products[i].product_spec_on=='y':
                                for productPic in productPics:
        
                                    if products[i].id==productPic.product_id : 
                                        # print(product.id)
                                        productSpecs=models.Product_Spec.objects.filter(product_id=products[i].id)
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=products[i].id).filter(user_id=user_id)
                                        productQuantitys=models.Shop_Order_Details.objects.filter(product_id=products[i].id).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
                                        productInfo = {
                                            'id': products[i].id,
                                            'product_title': products[i].product_title,
                                            'quantity': products[i].quantity, 
                                            'product_price': products[i].product_price,
                                            'pic_path':productPic.product_pic,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0,
                                            'liked':'N',
                                            'productQuantity':0
                                        }

                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                        for productLike in productLikes:
                                            if productLike.product_id==products[i].id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        
                                        for productQuantity in productQuantitys:
                                            if productQuantity["product_id"]==products[i].id :
                                                productInfo.update({'productQuantity': productQuantity["sale_quantity"]})
                                            else:
                                                productInfo.update({'productQuantity': 0})

                                        # responseData['data'].append(productInfo)
                                        top_sale_data.append(productInfo) 
                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id, 
                                        #     user_id=user_id
                                        # )

                            elif products[i].product_spec_on=='n':   
                                for productPic in productPics:  
                                    if products[i].id==productPic.product_id : 
                                        # print(product.id)
                                        productShopId=models.Shop.objects.get(id=products[i].shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=products[i].id).filter(user_id=user_id)
                                        productQuantitys=models.Shop_Order_Details.objects.filter(product_id=products[i].id).values('product_id').annotate(sale_quantity=Sum('purchasing_qty')).order_by('-sale_quantity')
                                        productInfo = {
                                            'id': products[i].id,
                                            'product_title': products[i].product_title,
                                            'quantity': products[i].quantity, 
                                            'product_price': products[i].product_price,
                                            'pic_path':productPic.product_pic,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0,
                                            'liked':'N',
                                            'productQuantity':0
                                        }

                                        productInfo.update({'min_price':products[i].product_price}) 
                                        productInfo.update({'max_price':products[i].product_price}) 
                                        productInfo.update({'min_quantity':products[i].quantity}) 
                                        productInfo.update({'max_quantity':products[i].quantity})
                                        productInfo.update({'sum_quantity':products[i].quantity})
                                        
                                        for productLike in productLikes:
                                            # print(productLike)
                                            if productLike.product_id==products[i].id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        
                                        for productQuantity in productQuantitys:
                                            
                                            # print(product.id)
                                            if productQuantity["product_id"]==products[i].id :
                                                
                                                productInfo.update({'productQuantity': productQuantity["sale_quantity"]})
                                            else:
                                                
                                                productInfo.update({'productQuantity': 0})

                                        top_sale_data.append(productInfo)

                                        # responseData['data'].append(productInfo)

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id, 
                                        #     user_id=user_id
                                        # )      
                        # responseData['data']=sorted(responseData['data'], key=lambda ratingSort : ratingSort['productQuantity'],reverse=True)  
                        # print(top_sale_data)  
                        # print(len(sorted(top_sale_data , key=lambda quantitySort : quantitySort['productQuantity'],reverse=True)))          
                        top_sale_dataFinal=sorted(top_sale_data , key=lambda quantitySort : quantitySort['productQuantity'],reverse=True)
                        for i in range(len(sorted(top_sale_data , key=lambda quantitySort : quantitySort['productQuantity'],reverse=True))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=top_sale_dataFinal[i]["id"],
                                        user_id=user_id,
                                        seq=i,
                                        pic_path=top_sale_dataFinal[i]["pic_path"],
                                        product_title=top_sale_dataFinal[i]["product_title"],
                                        shop_title=top_sale_dataFinal[i]["shop_title"],
                                        min_price=top_sale_dataFinal[i]["min_price"],
                                        max_price=top_sale_dataFinal[i]["max_price"],
                                        liked=top_sale_dataFinal[i]["liked"]
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=top_sale_data[i]["id"],
                                user_id=user_id
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_id).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage) 
                        models.Search_History.objects.create(
                                            id=uuid.uuid4(),
                                            search_category='product',
                                            keyword=key_word
                                        )                          
                        responseData['ret_val'] = '已取得商品清單!'
                elif mode=="lower_price":
                    lower_price_data=[]
                    if user_id=='' or user_id is None or user_id=="":
                        user_tempID=uuid.uuid4()
                        models.Product_Analytics.objects.filter(user_id=user_tempID).delete() 


                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_category_id__contains=categoryId).filter(product_title__contains=key_word)
                        getProductID=[]
                        getShopID=[]
                        for product in products:
                            getProductID.append(product.id)
                        for shop in products:
                            getShopID.append(shop.id)

                        productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                        for product in products:   
                            if product.product_spec_on=='y':
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if product.id==productPic.product_id : 
                                        productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)

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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                            # 'price' : productSpec.price
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            # if product.id==productSpecs.product.id:
                                            # responseData['data'].update({'price':obj.price})
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 
                                        # responseData['data'].append(productInfo)
                                        lower_price_data.append(productInfo) 
                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id
                                        # )

                            elif product.product_spec_on=='n':   
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if product.id==productPic.product_id : 
                                        # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                            # 'price' : productSpec.price
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        productInfo.update({'min_price':product.product_price}) 
                                        productInfo.update({'max_price':product.product_price}) 
                                        productInfo.update({'min_quantity':product.quantity}) 
                                        productInfo.update({'max_quantity':product.quantity})
                                        productInfo.update({'sum_quantity':product.quantity})
                                        # responseData['data'].append(productInfo) 
                                        lower_price_data.append(productInfo) 
                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id
                                        # )            
                        # print(sorted(responseData['data'], key=lambda priceSort : priceSort['max_price'],reverse=True)) #,reverse=True
                        # responseData['data']=sorted(responseData['data'], key=lambda priceSort : priceSort['max_price'])
                        # responseData['ret_val'] = '已取得商品清單!'
                        lower_price_dataFinal=sorted(lower_price_data , key=lambda priceSort : priceSort['max_price'])
                        for i in range(len(sorted(lower_price_data , key=lambda priceSort : priceSort['max_price']))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=lower_price_dataFinal[i]["id"],
                                        user_id=user_tempID,
                                        seq=i,
                                        pic_path=lower_price_dataFinal[i]["pic_path"],
                                        product_title=lower_price_dataFinal[i]["product_title"],
                                        shop_title=lower_price_dataFinal[i]["shop_title"],
                                        min_price=lower_price_dataFinal[i]["min_price"],
                                        max_price=lower_price_dataFinal[i]["max_price"],
                                        liked='N'
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=lower_price_dataFinal[i]["id"]
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_tempID).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage)         
                        models.Search_History.objects.create(
                                            id=uuid.uuid4(),
                                            search_category='product',
                                            keyword=key_word
                                        )  
                        responseData['ret_val'] = '已取得商品清單!'
                    else:
                        print("userID登入")
                        # shop=models.Shop.objects.get(id=id)
                        models.Product_Analytics.objects.filter(user_id=user_id).delete() 
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_category_id__contains=categoryId).filter(product_title__contains=key_word)
                        getProductID=[]
                        getShopID=[]
                        for product in products:
                            getProductID.append(product.id)
                        for shop in products:
                            getShopID.append(shop.id)

                        productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')
                        for product in products:   
                            if product.product_spec_on=='y':
                                for productPic in productPics:
        
                                    if product.id==productPic.product_id : 
                                       
                                        productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)

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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0
                                        }

                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                        for productLike in productLikes:
                                            if productLike.product_id==product.id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        lower_price_data.append(productInfo) 

                                        # responseData['data'].append(productInfo)

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id, 
                                        #     user_id=user_id
                                        # )

                            elif product.product_spec_on=='n':   
                                for productPic in productPics:  
                                    if product.id==productPic.product_id : 
                                        
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                        
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0
                                        }

                                        productInfo.update({'min_price':product.product_price}) 
                                        productInfo.update({'max_price':product.product_price}) 
                                        productInfo.update({'min_quantity':product.quantity}) 
                                        productInfo.update({'max_quantity':product.quantity})
                                        productInfo.update({'sum_quantity':product.quantity})
                                        
                                        for productLike in productLikes:
                                            if productLike.product_id==product.id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        lower_price_data.append(productInfo) 

                                        # responseData['data'].append(productInfo)

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id, 
                                        #     user_id=user_id
                                        # )      

                        lower_price_dataFinal=sorted(lower_price_data , key=lambda priceSort : priceSort['max_price'])
                        for i in range(len(sorted(lower_price_data , key=lambda priceSort : priceSort['max_price']))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=lower_price_dataFinal[i]["id"],
                                        user_id=user_id,
                                        seq=i,
                                        pic_path=lower_price_dataFinal[i]["pic_path"],
                                        product_title=lower_price_dataFinal[i]["product_title"],
                                        shop_title=lower_price_dataFinal[i]["shop_title"],
                                        min_price=lower_price_dataFinal[i]["min_price"],
                                        max_price=lower_price_dataFinal[i]["max_price"],
                                        liked='N'
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=lower_price_dataFinal[i]["id"],
                                user_id=user_id
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_id).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage)
                        models.Search_History.objects.create(
                                            id=uuid.uuid4(),
                                            search_category='product',
                                            keyword=key_word
                                        )   
                        responseData['ret_val'] = '已取得商品清單!'


                elif mode=="higher_price":
                    lower_price_data=[]
                    if user_id=='' or user_id is None or user_id=="":
                        user_tempID=uuid.uuid4()
                        models.Product_Analytics.objects.filter(user_id=user_tempID).delete() 
                        # products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_title__contains=key_word)

                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_category_id__contains=categoryId).filter(product_title__contains=key_word)#.order_by('-price')[:12]#.filter(like__gt=0) 
                        getProductID=[]
                        getShopID=[]
                        for product in products:
                            getProductID.append(product.id)
                        for shop in products:
                            getShopID.append(shop.id)

                        productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                        for product in products:   
                            if product.product_spec_on=='y':
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if product.id==productPic.product_id : 
                                        productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)

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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                            # 'price' : productSpec.price
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            # if product.id==productSpecs.product.id:
                                            # responseData['data'].update({'price':obj.price})
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 
                                        # responseData['data'].append(productInfo)
                                        lower_price_data.append(productInfo) 
                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id
                                        # )

                            elif product.product_spec_on=='n':   
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if product.id==productPic.product_id : 
                                        # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                            # 'price' : productSpec.price
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        productInfo.update({'min_price':product.product_price}) 
                                        productInfo.update({'max_price':product.product_price}) 
                                        productInfo.update({'min_quantity':product.quantity}) 
                                        productInfo.update({'max_quantity':product.quantity})
                                        productInfo.update({'sum_quantity':product.quantity})
                                        # responseData['data'].append(productInfo) 
                                        lower_price_data.append(productInfo) 
                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id
                                        # )            
                        # print(sorted(responseData['data'], key=lambda priceSort : priceSort['max_price'],reverse=True)) #,reverse=True
                        # responseData['data']=sorted(responseData['data'], key=lambda priceSort : priceSort['max_price'])
                        # responseData['ret_val'] = '已取得商品清單!'
                        lower_price_dataFinal=sorted(lower_price_data , key=lambda priceSort : priceSort['max_price'],reverse=True)
                        for i in range(len(sorted(lower_price_data , key=lambda priceSort : priceSort['max_price']))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=lower_price_dataFinal[i]["id"],
                                        user_id=user_tempID,
                                        seq=i,
                                        pic_path=lower_price_dataFinal[i]["pic_path"],
                                        product_title=lower_price_dataFinal[i]["product_title"],
                                        shop_title=lower_price_dataFinal[i]["shop_title"],
                                        min_price=lower_price_dataFinal[i]["min_price"],
                                        max_price=lower_price_dataFinal[i]["max_price"],
                                        liked='N'
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=lower_price_dataFinal[i]["id"]
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_tempID).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage)         
                        models.Search_History.objects.create(
                                            id=uuid.uuid4(),
                                            search_category='product',
                                            keyword=key_word
                                        )  
                        responseData['ret_val'] = '已取得商品清單!'
                    else:
                        print("userID登入")
                        # shop=models.Shop.objects.get(id=id)
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_category_id__contains=categoryId).filter(product_title__contains=key_word) 
                        getProductID=[]
                        getShopID=[]
                        for product in products:
                            getProductID.append(product.id)
                        for shop in products:
                            getShopID.append(shop.id)
                        models.Product_Analytics.objects.filter(user_id=user_id).delete() 
                        productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')
                        for product in products:   
                            if product.product_spec_on=='y':
                                for productPic in productPics:
        
                                    if product.id==productPic.product_id : 
                                        
                                        productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)

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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0
                                        }

                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                        for productLike in productLikes:
                                            if productLike.product_id==product.id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        lower_price_data.append(productInfo) 

                                        # responseData['data'].append(productInfo)

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id, 
                                        #     user_id=user_id
                                        # )

                            elif product.product_spec_on=='n':   
                                for productPic in productPics:  
                                    if product.id==productPic.product_id : 
                                        
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                        
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'rating':0
                                        }

                                        productInfo.update({'min_price':product.product_price}) 
                                        productInfo.update({'max_price':product.product_price}) 
                                        productInfo.update({'min_quantity':product.quantity}) 
                                        productInfo.update({'max_quantity':product.quantity})
                                        productInfo.update({'sum_quantity':product.quantity})
                                        
                                        for productLike in productLikes:
                                            if productLike.product_id==product.id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        lower_price_data.append(productInfo) 

                                        # responseData['data'].append(productInfo)

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id, 
                                        #     user_id=user_id
                                        # )      

                        lower_price_dataFinal=sorted(lower_price_data , key=lambda priceSort : priceSort['max_price'],reverse=True)
                        for i in range(len(sorted(lower_price_data , key=lambda priceSort : priceSort['max_price']))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=lower_price_dataFinal[i]["id"],
                                        user_id=user_id,
                                        seq=i,
                                        pic_path=lower_price_dataFinal[i]["pic_path"],
                                        product_title=lower_price_dataFinal[i]["product_title"],
                                        shop_title=lower_price_dataFinal[i]["shop_title"],
                                        min_price=lower_price_dataFinal[i]["min_price"],
                                        max_price=lower_price_dataFinal[i]["max_price"],
                                        liked='N'
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=lower_price_dataFinal[i]["id"],
                                user_id=user_id
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_id).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage) 
                        models.Search_History.objects.create(
                                            id=uuid.uuid4(),
                                            search_category='product',
                                            keyword=key_word
                                        )  
                        responseData['ret_val'] = '已取得商品清單!'
                elif mode=="overall":
                    overall_data=[]
                    if user_id=='' or user_id is None or user_id=="":
                        # shop=models.Shop.objects.get(id=id)
                        user_tempID=uuid.uuid4()
                        models.Product_Analytics.objects.filter(user_id=user_tempID).delete() 
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_category_id__contains=categoryId).filter(product_title__contains=key_word)#.filter(like__gt=0) 
                        
                        getProductID=[]
                        getShopID=[]
                        for product in products:
                            getProductID.append(product.id)
                        for shop in products:
                            getShopID.append(shop.id)

                        # productOveralls=models.Product_Rate.objects.filter(product_id__in=getProductID).values('product_id').annotate(ratings=Avg('rating')).order_by('-rating')
                        # from django.db.models import Avg
                        productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                        for product in products:   
                            if product.product_spec_on=='y':
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if product.id==productPic.product_id : 
                                        productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productOveralls=models.Product_Rate.objects.filter(product_id=product.id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            # if product.id==productSpecs.product.id:
                                            # responseData['data'].update({'price':obj.price})
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                        for productOverall in productOveralls:
                                            if productOverall["product_id"]==product.id :
                                                productInfo.update({'rating': productOverall["rating"]})
                                            else:
                                                productInfo.update({'rating': 0})

                                        # responseData['data'].append(productInfo)
                                        overall_data.append(productInfo) 

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id
                                        # )

                            elif product.product_spec_on=='n':   
                                for productPic in productPics:
                                    # for productSpec in productSpecs:    
                                    if product.id==productPic.product_id : 
                                        # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productOveralls=models.Product_Rate.objects.filter(product_id=product.id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                        }
                                        #responseData['data'].append(productInfo)    
                                        # responseData['data']['price'] = {}
                                        productInfo.update({'min_price':product.product_price}) 
                                        productInfo.update({'max_price':product.product_price}) 
                                        productInfo.update({'min_quantity':product.quantity}) 
                                        productInfo.update({'max_quantity':product.quantity})
                                        productInfo.update({'sum_quantity':product.quantity})

                                        for productOverall in productOveralls:
                                            if productOverall["product_id"]==product.id :
                                                productInfo.update({'rating': productOverall["rating"]})
                                            else:
                                                productInfo.update({'rating': 0})
                                        overall_data.append(productInfo)
                                        # responseData['data'].append(productInfo) 
                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id
                                        # )           
                                        #  
                        overall_data_dataFinal=sorted(overall_data , key=lambda rateSort : rateSort['rating'],reverse=True)
                        for i in range(len(sorted(overall_data , key=lambda rateSort : rateSort['rating']))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=overall_data_dataFinal[i]["id"],
                                        user_id=user_tempID,
                                        seq=i,
                                        pic_path=overall_data_dataFinal[i]["pic_path"],
                                        product_title=overall_data_dataFinal[i]["product_title"],
                                        shop_title=overall_data_dataFinal[i]["shop_title"],
                                        min_price=overall_data_dataFinal[i]["min_price"],
                                        max_price=overall_data_dataFinal[i]["max_price"],
                                        liked='N'
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=overall_data_dataFinal[i]["id"]
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_tempID).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage) 
                        models.Search_History.objects.create(
                                            id=uuid.uuid4(),
                                            search_category='product',
                                            keyword=key_word
                                        )  
                        responseData['ret_val'] = '已取得商品清單!'                
                    else:
                        
                        # shop=models.Shop.objects.get(id=id)
                        # user_tempID=uuid.uuid4()
                        models.Product_Analytics.objects.filter(user_id=user_id).delete() 
                        products = models.Product.objects.filter(product_status='active').filter(is_delete='N').filter(product_category_id__contains=categoryId).filter(product_title__contains=key_word)#.filter(like__gt=0) 
                        getProductID=[]
                        getShopID=[]
                        for product in products:
                            getProductID.append(product.id)
                        for shop in products:
                            getShopID.append(shop.id)

                        # productOveralls=models.Product_Rate.objects.filter(product_id__in=getProductID).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
                        # print(productOveralls)
                        productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')
                        for product in products:   
                            if product.product_spec_on=='y':
                                for productPic in productPics:
        
                                    if product.id==productPic.product_id : 
                                        # print(product.id)
                                        productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                        productOveralls=models.Product_Rate.objects.filter(product_id=product.id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                        }

                                        v = []
                                        price_range=[]
                                        quantity_range=[]
                                        quantity_sum=[]
                                        for obj in productSpecs:
                                            v.append(getattr(obj,'price'))
                                            price_range.append(getattr(obj,'price'))
                                            quantity_range.append(getattr(obj,'quantity'))
                                            quantity_sum.append(getattr(obj,'quantity'))
                                        min_price=min(price_range)
                                        max_price=max(price_range)
                                    
                                        productInfo.update({'price':v})   
                                        productInfo.update({'min_price':min_price})   
                                        productInfo.update({'max_price':max_price})  
                                        productInfo.update({'min_quantity':min(quantity_range)}) 
                                        productInfo.update({'max_quantity':max(quantity_range)})
                                        productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                        for productLike in productLikes:
                                            if productLike.product_id==product.id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        
                                        for productOverall in productOveralls:
                                            # print(product.id)
                                            if productOverall["product_id"]==product.id :
                                                productInfo.update({'rating': productOverall["rating"]})
                                            else:
                                                productInfo.update({'rating': 0})

                                        # responseData['data'].append(productInfo)
                                        overall_data.append(productInfo)

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id, 
                                        #     user_id=user_id
                                        # )

                            elif product.product_spec_on=='n':   
                                for productPic in productPics:  
                                    if product.id==productPic.product_id : 
                                        # print(product.id)
                                        productShopId=models.Shop.objects.get(id=product.shop_id)
                                        productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                                        productOveralls=models.Product_Rate.objects.filter(product_id=product.id).values('product_id').annotate(rating=Avg('rating')).order_by('-rating')
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
                                            'product_status':product.product_status,
                                            'pic_path':productPic.product_pic,
                                            'product_spec_on':product.product_spec_on,
                                            'shop_id':productShopId.id,
                                            'shop_title':productShopId.shop_title,
                                            'liked':'N',
                                            'rating':0
                                        }

                                        productInfo.update({'min_price':product.product_price}) 
                                        productInfo.update({'max_price':product.product_price}) 
                                        productInfo.update({'min_quantity':product.quantity}) 
                                        productInfo.update({'max_quantity':product.quantity})
                                        productInfo.update({'sum_quantity':product.quantity})
                                        
                                        for productLike in productLikes:
                                            # print(productLike)
                                            if productLike.product_id==product.id :
                                                productInfo.update({'liked': 'Y'})
                                            else:
                                                productInfo.update({'liked': 'N'})
                                        
                                        for productOverall in productOveralls:
                                            
                                            # print(product.id)
                                            if productOverall["product_id"]==product.id :
                                                
                                                productInfo.update({'rating': productOverall["rating"]})
                                            else:
                                                
                                                productInfo.update({'rating': 0})

                                        # responseData['data'].append(productInfo)
                                        overall_data.append(productInfo)

                                        # models.Product_Browsed.objects.create(
                                        #     id=uuid.uuid4(),
                                        #     product_id=product.id, 
                                        #     user_id=user_id
                                        # )      
                        overall_data_dataFinal=sorted(overall_data , key=lambda rateSort : rateSort['rating'],reverse=True)
                        for i in range(len(sorted(overall_data , key=lambda rateSort : rateSort['rating']))):            
                            models.Product_Analytics.objects.create(
                                        id=uuid.uuid4(),                                            
                                        product_id=overall_data_dataFinal[i]["id"],
                                        user_id=user_id,
                                        seq=i,
                                        pic_path=overall_data_dataFinal[i]["pic_path"],
                                        product_title=overall_data_dataFinal[i]["product_title"],
                                        shop_title=overall_data_dataFinal[i]["shop_title"],
                                        min_price=overall_data_dataFinal[i]["min_price"],
                                        max_price=overall_data_dataFinal[i]["max_price"],
                                        liked='N'
                                    )    
                            models.Product_Browsed.objects.create(
                                id=uuid.uuid4(),
                                product_id=overall_data_dataFinal[i]["id"],
                                user_id=user_id
                            )  

                        pageSize=12
                        pageStart=0
                        pageEnd=pageStart+pageSize-1
                        productAnalytics=models.Product_Analytics.objects.filter(user_id=user_id).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                        for productAnalytic in productAnalytics:
                            productFirstPage = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                            responseData['data'].append(productFirstPage) 
                        models.Search_History.objects.create(
                                            id=uuid.uuid4(),
                                            search_category='product',
                                            keyword=key_word
                                        )  
                        responseData['ret_val'] = '已取得商品清單!'   
                else:
                    responseData['status'] =-1
                    responseData['ret_val'] = '未輸入排序規則'
            else: #max_seq from 1 to .....
                pageSize=12
                pageStart=int(max_seq)*pageSize
                pageEnd=pageStart+pageSize-1
                if user_id=='' or user_id is None or user_id=="":
                    productAnalytics=models.Product_Analytics.objects.filter(user_id__isnull=True).filter(seq__gte=pageStart).filter(seq__lte=pageEnd).order_by('seq')
                    for productAnalytic in productAnalytics:
                        productInfo = {
                                    'id': productAnalytic.id,
                                    'product_id': productAnalytic.product_id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                        responseData['data'].append(productInfo)
                    responseData['ret_val'] = '取得商品分頁資訊'
                else : #login
                    productAnalytics=models.Product_Analytics.objects.filter(user_id=user_id).filter(seq__range=(pageStart,pageEnd)).order_by('seq')
                    for productAnalytic in productAnalytics:
                        productInfo = {
                                    'id': productAnalytic.id,
                                    'user_id': productAnalytic.user_id,
                                    'page_id' : int(max_seq)+1,
                                    'product_id': productAnalytic.product_id, 
                                    'seq':productAnalytic.seq,
                                    'pic_path':productAnalytic.pic_path,
                                    'product_title':productAnalytic.product_title,
                                    'shop_title':productAnalytic.shop_title,
                                    'min_price':productAnalytic.min_price,
                                    'max_price':productAnalytic.max_price,
                                    'liked':productAnalytic.liked
                                    }
                        responseData['data'].append(productInfo)
                    responseData['ret_val'] = '取得商品分頁資訊'

    return JsonResponse(responseData)
#取得類似推薦商品
def similar_product_list(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }

    if request.method == 'POST':
        if responseData['status'] == 0:
            user_id=request.POST.get('user_id','')
            product_id=request.POST.get('product_id','')

            if user_id=='' or user_id is None or user_id=="":

                categoryId=models.Product.objects.get(id=product_id)
                print(categoryId.product_category_id)
                products = models.Product.objects.filter(product_category_id=categoryId.product_category_id,is_delete='N',product_status='active')[:3]

                getProductID=[]
                getShopID=[]
                for product in products:
                    getProductID.append(product.id)
                for shop in products:
                    getShopID.append(shop.id)

                productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')     
                for product in products:   
                    if product.product_spec_on=='y':
                        for productPic in productPics:
                            # for productSpec in productSpecs:    
                            if product.id==productPic.product_id : 
                                productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                productShopId=models.Shop.objects.get(id=product.shop_id)

                                productInfo = {
                                    'id': product.id,
                                    'product_category_id': product.product_category_id, 
                                    'product_title': product.product_title,                                    
                                    'product_description': product.product_description, 
                                    'product_price': product.product_price,                                     
                                    'product_status':product.product_status,
                                    'pic_path':productPic.product_pic,
                                    'product_spec_on':product.product_spec_on,
                                    'shop_id':productShopId.id,
                                    'shop_title':productShopId.shop_title,
                                    'liked':'N'
                                    # 'price' : productSpec.price
                                }
                                #responseData['data'].append(productInfo)    
                                # responseData['data']['price'] = {}
                                v = []
                                price_range=[]
                                quantity_range=[]
                                quantity_sum=[]
                                for obj in productSpecs:
                                    # if product.id==productSpecs.product.id:
                                    # responseData['data'].update({'price':obj.price})
                                    v.append(getattr(obj,'price'))
                                    price_range.append(getattr(obj,'price'))
                                    quantity_range.append(getattr(obj,'quantity'))
                                    quantity_sum.append(getattr(obj,'quantity'))
                                min_price=min(price_range)
                                max_price=max(price_range)
                            
                                productInfo.update({'price':v})   
                                productInfo.update({'min_price':min_price})   
                                productInfo.update({'max_price':max_price})  
                                productInfo.update({'min_quantity':min(quantity_range)}) 
                                productInfo.update({'max_quantity':max(quantity_range)})
                                productInfo.update({'sum_quantity': sum(quantity_sum)}) 
                                responseData['data'].append(productInfo)

                                models.Product_Browsed.objects.create(
                                    id=uuid.uuid4(),
                                    product_id=product.id
                                )

                    elif product.product_spec_on=='n':   
                        for productPic in productPics:
                            # for productSpec in productSpecs:    
                            if product.id==productPic.product_id : 
                                # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                productShopId=models.Shop.objects.get(id=product.shop_id)
                                productInfo = {
                                    'id': product.id,
                                    'product_category_id': product.product_category_id, 
                                    'product_title': product.product_title,    
                                    'product_price': product.product_price,  
                                    'product_status':product.product_status,
                                    'pic_path':productPic.product_pic,
                                    'product_spec_on':product.product_spec_on,
                                    'shop_id':productShopId.id,
                                    'shop_title':productShopId.shop_title,
                                    'liked':'N'
                                    # 'price' : productSpec.price
                                }
                                #responseData['data'].append(productInfo)    
                                # responseData['data']['price'] = {}
                                productInfo.update({'min_price':product.product_price}) 
                                productInfo.update({'max_price':product.product_price}) 
                                productInfo.update({'min_quantity':product.quantity}) 
                                productInfo.update({'max_quantity':product.quantity})
                                productInfo.update({'sum_quantity':product.quantity})
                                responseData['data'].append(productInfo) 
                                models.Product_Browsed.objects.create(
                                    id=uuid.uuid4(),
                                    product_id=product.id
                                )            

                responseData['ret_val'] = '已取得商品清單!'
            else:
                print("userID登入")
                categoryId=models.Product.objects.get(id=product_id)
                products = models.Product.objects.filter(product_category_id=categoryId.product_category_id,is_delete='N',product_status='active')[:3]
                getProductID=[]
                getShopID=[]
                for product in products:
                    getProductID.append(product.id)
                for shop in products:
                    getShopID.append(shop.id)

                productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')
                for product in products:   
                    if product.product_spec_on=='y':
                        for productPic in productPics:
  
                            if product.id==productPic.product_id : 
                                
                                productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                                productShopId=models.Shop.objects.get(id=product.shop_id)
                                productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=id)

                                productInfo = {
                                    'id': product.id,
                                    'product_category_id': product.product_category_id, 
                                    'product_title': product.product_title,                                    
                                    'product_description': product.product_description, 
                                    'product_price': product.product_price,                                     
                                    'product_status':product.product_status,
                                    'pic_path':productPic.product_pic,
                                    'product_spec_on':product.product_spec_on,
                                    'shop_id':productShopId.id,
                                    'shop_title':productShopId.shop_title,
                                    'liked':'N'
                                }

                                v = []
                                price_range=[]
                                quantity_range=[]
                                quantity_sum=[]
                                for obj in productSpecs:
                                    v.append(getattr(obj,'price'))
                                    price_range.append(getattr(obj,'price'))
                                    quantity_range.append(getattr(obj,'quantity'))
                                    quantity_sum.append(getattr(obj,'quantity'))
                                min_price=min(price_range)
                                max_price=max(price_range)
                            
                                productInfo.update({'price':v})   
                                productInfo.update({'min_price':min_price})   
                                productInfo.update({'max_price':max_price})  
                                productInfo.update({'min_quantity':min(quantity_range)}) 
                                productInfo.update({'max_quantity':max(quantity_range)})
                                productInfo.update({'sum_quantity': sum(quantity_sum)}) 

                                for productLike in productLikes:
                                    if productLike.product_id==product.id :
                                        productInfo.update({'liked': 'Y'})
                                    else:
                                        productInfo.update({'liked': 'N'})

                                responseData['data'].append(productInfo)

                                models.Product_Browsed.objects.create(
                                    id=uuid.uuid4(),
                                    product_id=product.id, 
                                    user_id=id
                                )

                    elif product.product_spec_on=='n':   
                        for productPic in productPics:  
                            if product.id==productPic.product_id : 
                                
                                productShopId=models.Shop.objects.get(id=product.shop_id)
                                productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=id)
                                
                                productInfo = {
                                    'id': product.id,
                                    'product_category_id': product.product_category_id, 
                                    'product_title': product.product_title,                                    
                                    'product_description': product.product_description, 
                                    'product_price': product.product_price,                                     
                                    'product_status':product.product_status,
                                    'pic_path':productPic.product_pic,
                                    'product_spec_on':product.product_spec_on,
                                    'shop_id':productShopId.id,
                                    'shop_title':productShopId.shop_title,
                                    'liked':'N'
                                }

                                productInfo.update({'min_price':product.product_price}) 
                                productInfo.update({'max_price':product.product_price}) 
                                productInfo.update({'min_quantity':product.quantity}) 
                                productInfo.update({'max_quantity':product.quantity})
                                productInfo.update({'sum_quantity':product.quantity})
                                
                                for productLike in productLikes:
                                    if productLike.product_id==product.id :
                                        productInfo.update({'liked': 'Y'})
                                    else:
                                        productInfo.update({'liked': 'N'})

                                responseData['data'].append(productInfo)

                                models.Product_Browsed.objects.create(
                                    id=uuid.uuid4(),
                                    product_id=product.id, 
                                    user_id=id
                                )      
               
                responseData['ret_val'] = '已取得商品清單!'
    return JsonResponse(responseData)

def like_product(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method=='POST':
        # user id, product id, like[Y|N]
        user_id= request.POST.get('user_id', '')
        product_id= request.POST.get('product_id', '')
        like = request.POST.get('like', '')

        if response_data['status']==0:
            try:
                models.User.objects.get(id=user_id)
            except:
                response_data['status'], response_data['ret_val'] = -2, '使用者不存在'
                
        if response_data['status']==0:
            try:
                models.Product.objects.get(id=product_id)
            except:
                response_data['status'], response_data['ret_val'] = -3, '商品不存在'
        
        if response_data['status']==0:
            if like!='Y' and like!='N':
                response_data['status'], response_data['ret_val'] = -4, 'like只能為Y|N'

        if response_data['status']==0:
            products_liked_check=models.Product_Liked.objects.filter(user_id=user_id,product_id=product_id)
            print(products_liked_check)
            if (len(products_liked_check))>0 and like=='N':
                products_liked_check.delete()
                response_data['ret_val'] = '取消收藏成功'
                response_data['status'] = 0
            elif (len(products_liked_check))==0 and like=='Y':
                models.Product_Liked.objects.create(
                    id=uuid.uuid4(),
                    user_id=user_id,
                    product_id=product_id
                )
                products_liked=models.Product_Liked.objects.filter(user_id=user_id,product_id=product_id)
                if(len(products_liked))>0:
                    response_data['ret_val'] = '商品收藏成功!'
                    response_data['status'] = 0
                elif(len(products_liked))==0:
                    response_data['ret_val'] = '商品收藏失敗!'
                    response_data['status'] = -1
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
            # for product_spec_list02 in product_spec_list:
            # 寫入資料庫
            # for i in range(len(product_spec_list["product_spec_list"])):
                # models.Product_Spec.objects.create(
                #     product_id=product_spec_list[i][0],
                #     spec_name=product_spec_list[i][1],
                #     price=product_spec_list[i][2],
                #     quantity=product_spec_list[i][3],
                #     size=product_spec_list[i][4]
                # )
                # models.Product_Spec.objects.create(
                #     product_id=product_spec_list["product_spec_list"][i]["product_id"],
                #     spec_desc_1=product_spec_list["product_spec_list"][i]["spec_desc_1"],
                #     spec_desc_2=product_spec_list["product_spec_list"][i]["spec_desc_2"],
                #     spec_dec_1_items=product_spec_list["product_spec_list"][i]["spec_dec_1_items"],
                #     spec_dec_2_items=product_spec_list["product_spec_list"][i]["spec_dec_2_items"],
                #     price=product_spec_list["product_spec_list"][i]["price"],
                #     quantity=product_spec_list["product_spec_list"][i]["quantity"],
                # )
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

            
            # response_data['test'].append(product_spec_list)
            

    return JsonResponse(response_data)
# 取得單一商品評價詳細資料(買家)
def get_product_rating_details_for_buyer(request, id):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            try:
                product = models.Product.objects.get(id=id)
            except:
                response_data['status'] = -1
                response_data['ret_val'] = '找不到此商品!'

        if response_data['status'] == 0:
            product_ratings = models.Product_Rate.objects.filter(product_id=product.id).values('user_id', 'rating', 'comment')
            for product_rating in product_ratings:
                users = models.User.objects.filter(id=product_rating['user_id']).values('first_name')
                response_data['data'].append({
                    'user_name': users[0]['first_name'] if len(users) > 0 else '', 
                    'rating': product_rating['rating'], 
                    'comment': product_rating['comment']
                })
            response_data['ret_val'] = '取得單一商品評價詳細資料(買家)成功!'
    return JsonResponse(response_data)