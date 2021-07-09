from django.db.models import Q, Avg, Min, Max, Count, Sum
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.contrib.auth.hashers import make_password ,check_password
from passlib.handlers.django import django_pbkdf2_sha256
from django.core import mail
from django.utils.html import strip_tags
from hkshopu import models
import uuid
import datetime
import re
import random
from utils.upload_tools import upload_file , delete_file
# Create your views here.

#新增會員圖片
def add_pic(request):
    # 回傳資料
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method=='POST':

        user_id= request.POST.get('user_id', '')
        user_pic = request.FILES.get('user_pic')
        if response_data['status']==0:
            user=models.User.objects.get(id=user_id)
            if user.pic=='' or user.pic is None:
                # 上傳圖片
                destination_path = 'images/user/'
                userPic = upload_file(FILE=user_pic,destination_path=destination_path,suffix='icon')
                user.pic=userPic
                user.save()
                response_data['ret_val'] = '使用者照片新增成功!'
                response_data['data'].append(user.pic)
            else:
                delete_file(user.pic)
                user.pic=''
                user.save() 
                # 上傳圖片
                destination_path = 'images/user/'
                userPic = upload_file(FILE=user_pic,destination_path=destination_path,suffix='icon')
                user.pic=userPic
                user.save()
                response_data['ret_val'] = '使用者照片新增成功!'
                response_data['data'].append(user.pic)
    return JsonResponse(response_data)

# 更改會員
def update_detail(request):
    responseData = {
            'status': 0,
            'ret_val': '',
            'data': {}
        }
  
    if request.method=='POST':
        user_id= request.POST.get('user_id', '')
        user_name= request.POST.get('user_name', '')
        gender=request.POST.get('gender', '')
        birthday=request.POST.get('birthday', '')
        phone=request.POST.get('phone', '')
        facebook_on_off=request.POST.get('facebook_on_off', '')
        instagram_on_off=request.POST.get('instagram_on_off', '')

        old_password=request.POST.get('old_password', '')
        new_password=request.POST.get('new_password', '')

        users=models.User.objects.filter(id=user_id)
        # if responseData['status'] == 0:
        #     if not(re.match('^(?!.*[^\x21-\x7e])(?=.{8,16})(?=.*[\W])(?=.*[a-zA-Z])(?=.*\d).*$', new_password)):
        #         responseData['status'] = -1
        #         responseData['ret_val'] = '新密碼格式錯誤!'
        print(make_password(old_password))
        print("============")
        print(check_password(old_password,users[0].password))
        if responseData['status']==0:
            for user in users:
                if user_name !='':
                    if not(re.match('^[A-Za-z]{3,45}$', accountName)):
                        responseData['status'] = -6
                        responseData['ret_val'] = '用戶名稱格式錯誤!'
                        return JsonResponse(responseData)
                    else:
                        user.account_name=user_name               
                elif gender !='':
                    if not(re.match('^[M|F|O]{1}$', gender)):
                        responseData['status'] = -5
                        responseData['ret_val'] = '性別格式錯誤!'
                        return JsonResponse(responseData)
                    else :
                        user.gender=gender      
                elif birthday !='':
                    if not(re.match('^[0-9]{2}\/[0-9]{2}\/[0-9]{4}$', birthday)):
                        responseData['status'] = -3
                        responseData['ret_val'] = '出生日期格式錯誤!'
                        return JsonResponse(responseData)
                    else:
                        user.birthday =birthday
                elif phone !='':
                    if not(re.match('^[0-9]{8,10}$', phone)):
                        responseData['status'] = -4
                        responseData['ret_val'] = '手機號碼格式錯誤!'
                        return JsonResponse(responseData)
                    else:
                        user.phone =phone
                elif old_password !='':
                    if check_password(old_password,users[0].password):
                        responseData['status'] = 0
                        responseData['ret_val'] = '輸入值與舊密碼一致'
                        return JsonResponse(responseData)
                    else : 
                        responseData['status'] = -1
                        responseData['ret_val'] = '輸入值與舊密碼不一致'
                        return JsonResponse(responseData)
                elif new_password !='':
                    if not(re.match('^(?!.*[^\x21-\x7e])(?=.{8,16})(?=.*[\W])(?=.*[a-zA-Z])(?=.*\d).*$', new_password)):
                        responseData['status'] = -2
                        responseData['ret_val'] = '新密碼格式錯誤!'
                        return JsonResponse(responseData)
                    else:
                        user.password =make_password(new_password)
                
                user.save()
                responseData['ret_val'] = '使用者資訊更新成功!'

    return JsonResponse(responseData)

def user_rate(request,user_id): 
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    } 
    if request.method=='GET':
        if response_data['status']==0:
            rates=models.User_Rate.objects.filter(user_id=user_id)
            for rate in rates:
                sellerName=models.User.objects.get(id=rate.user_id)
                rateInfo={
                    "id":rate.id,
                    "name":sellerName.account_name,
                    "rating":rate.rating,
                    "comment": rate.comment,
                    "rate_time":rate.created_at
                }
                response_data['data'].append(rateInfo)

            response_data['ret_val'] = '買家評價取得成功'
    return JsonResponse(response_data)

def liked_count(request,user_id): 
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    } 
    if request.method=='GET':
        likes=models.Product_Liked.objects.filter(user_id=user_id).count()
        responseData['data'] =likes
        responseData['ret_val'] = '買家收藏數量取得成功'

    return JsonResponse(responseData)    
def user_liked(request): 
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    } 
    if request.method=='POST':
        user_id= request.POST.get('user_id', '')
        keyword=request.POST.get('keyword', '')
        if responseData['status']==0:
            likes=models.Product_Liked.objects.filter(user_id=user_id)
            getProductID=[]
            for like in likes:
                getProductID.append(like.product_id)
                # sellerName=models.User.objects.get(id=rate.user_id)

            products=models.Product.objects.filter(id__in=getProductID).filter(product_title__icontains=keyword).filter(is_delete='N')
            productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')  
            for product in products:
                if product.product_spec_on=='y':
                    for productPic in productPics:
                        # for productSpec in productSpecs:    
                        if product.id==productPic.product_id : 
                            productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                            productShopId=models.Shop.objects.get(id=product.shop_id)

                            likeInfo = {
                                'product_id': product.id,
                                'product_title': product.product_title,
                                'product_description': product.product_description, 
                                'product_price': product.product_price, 
                                'pic_path':productPic.product_pic,
                                'shop_id':productShopId.id,
                                'shop_title':productShopId.shop_title,
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
                            likeInfo.update({'min_price':min_price})   
                            likeInfo.update({'max_price':max_price})  
                            responseData['data'].append(likeInfo)

                elif product.product_spec_on=='n':   
                    for productPic in productPics:
                        # for productSpec in productSpecs:    
                        if product.id==productPic.product_id : 
                            # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                            productShopId=models.Shop.objects.get(id=product.shop_id)
                            likeInfo = {
                                'product_id': product.id,
                                'product_title': product.product_title,
                                'product_description': product.product_description, 
                                'product_price': product.product_price, 
                                'pic_path':productPic.product_pic,
                                'shop_id':productShopId.id,
                                'shop_title':productShopId.shop_title,
                            }
                            #responseData['data'].append(productInfo)    
                            # responseData['data']['price'] = {}
                            likeInfo.update({'min_price':product.product_price}) 
                            likeInfo.update({'max_price':product.product_price}) 
                            responseData['data'].append(likeInfo) 

            responseData['ret_val'] = '買家收藏取得成功'
    return JsonResponse(responseData)

def followed_count(request,user_id): 
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    } 
    if request.method=='GET':
        follow=models.Shop_Follower.objects.filter(follower_id=user_id).count()
        responseData['data'] =follow
        responseData['ret_val'] = '買家關注店鋪數量取得成功'

    return JsonResponse(responseData)   

def user_followed(request): 
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    } 
    if request.method=='POST':
        user_id= request.POST.get('user_id', '')
        keyword=request.POST.get('keyword', '')
        if responseData['status']==0:
            follows=models.Shop_Follower.objects.filter(follower_id=user_id)
            
            getShopID=[]
            for follow in follows:
                getShopID.append(follow.shop_id)
                # sellerName=models.User.objects.get(id=rate.user_id)

            shops=models.Shop.objects.filter(id__in=getShopID).filter(shop_title__icontains=keyword).filter(is_delete='N')
            for shop in shops:
                followCount=models.Shop_Follower.objects.filter(shop_id=shop.id).count()
                shopInfo={
                    "shop_id":shop.id,
                    "shop_title":shop.shop_title,
                    "shop_icon":shop.shop_icon,
                    "shop_pic":shop.shop_pic,
                    "follow_count":followCount,
                    # "shop_rate":shop.id,
                }
                responseData['data'].append(shopInfo) 

            responseData['ret_val'] = '買家關注店鋪取得成功'
    return JsonResponse(responseData) 

def browsed_count(request,user_id): 
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    } 
    if request.method=='GET':
        browse=models.Product_Browsed.objects.filter(user_id=user_id).values('product_id').annotate(Count('product_id')).count()
        responseData['data'] =browse
        responseData['ret_val'] = '買家足跡數量取得成功'

    return JsonResponse(responseData)   

def user_browsed(request): 
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    } 
    if request.method=='POST':
        user_id= request.POST.get('user_id', '')
        keyword=request.POST.get('keyword', '')
        if responseData['status']==0:
            browses=models.Product_Browsed.objects.filter(user_id=user_id)
            getProductID=[]
            for browse in browses:
                getProductID.append(browse.product_id)
                # sellerName=models.User.objects.get(id=rate.user_id)

            products=models.Product.objects.filter(id__in=getProductID).filter(product_title__icontains=keyword).filter(is_delete='N')
            productPics=models.Selected_Product_Pic.objects.filter(product_id__in=getProductID).filter(cover='y')  
            for product in products:
                if product.product_spec_on=='y':
                    for productPic in productPics:
                        # for productSpec in productSpecs:    
                        if product.id==productPic.product_id : 
                            productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                            productShopId=models.Shop.objects.get(id=product.shop_id)
                            productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)

                            browsedInfo = {
                                'product_id': product.id,
                                'product_title': product.product_title,
                                'product_description': product.product_description, 
                                'product_price': product.product_price, 
                                'pic_path':productPic.product_pic,
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
                            browsedInfo.update({'min_price':min_price})   
                            browsedInfo.update({'max_price':max_price})  

                            for productLike in productLikes:
                                if productLike.product_id==product.id :
                                    browsedInfo.update({'liked': 'Y'})
                                else:
                                    browsedInfo.update({'liked': 'N'})
                            responseData['data'].append(browsedInfo)

                elif product.product_spec_on=='n':   
                    for productPic in productPics:
                        # for productSpec in productSpecs:    
                        if product.id==productPic.product_id : 
                            # productSpecs=models.Product_Spec.objects.filter(product_id=product.id)
                            productShopId=models.Shop.objects.get(id=product.shop_id)
                            productLikes=models.Product_Liked.objects.filter(product_id=product.id).filter(user_id=user_id)
                            browsedInfo = {
                                'product_id': product.id,
                                'product_title': product.product_title,
                                'product_description': product.product_description, 
                                'product_price': product.product_price, 
                                'pic_path':productPic.product_pic,
                                'shop_id':productShopId.id,
                                'shop_title':productShopId.shop_title,
                                'liked':'N'
                            }
                            #responseData['data'].append(productInfo)    
                            # responseData['data']['price'] = {}
                            browsedInfo.update({'min_price':product.product_price}) 
                            browsedInfo.update({'max_price':product.product_price}) 

                            for productLike in productLikes:
                                if productLike.product_id==product.id :
                                    browsedInfo.update({'liked': 'Y'})
                                else:
                                    browsedInfo.update({'liked': 'N'})
                            responseData['data'].append(browsedInfo) 

            responseData['ret_val'] = '買家足跡取得成功'
    return JsonResponse(responseData)

def show(request,user_id): 
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': {}
    } 
    if request.method=='GET':
        if responseData['status']==0:
            user=models.User.objects.get(id=user_id)
            if user.pic==None:
                pic=""  
            else :
                pic=user.pic
            if user.account_name==None:
                account_name=""
            else:
                account_name=user.account_name
            if user.gender==None:
                gender=""
            else:
                gender=user.gender
            if user.birthday==None:
                birthday=""
            else:
                birthday=user.birthday
            if user.phone==None:
                phone=""
            else:
                phone=user.phone
            if user.email==None:
                email=""
            else:
                email=user.email
            userInfo={
                    "user_id":user.id,
                    "name":account_name,
                    "gender":gender,
                    "birthday":birthday,
                    "phone":phone,
                    "email":email,
                    "pic":pic
                }
            responseData.update({'data':userInfo}) 

            responseData['ret_val'] = '買家資訊取得成功'
    return JsonResponse(responseData) 

def profile(request,user_id): 
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': {}
    } 
    if request.method=='GET':
        if responseData['status']==0:
            user=models.User.objects.get(id=user_id)
            rate=models.User_Rate.objects.filter(user_id=user_id).aggregate(Avg('rating'))
            print(rate)
            if rate["rating__avg"]== None:
                rating=0
            else :
                rating=rate["rating__avg"]
            if user.pic==None:
                pic=""  
            else :
                pic=user.pic
            if user.account_name==None:
                account_name=""
            else :
                account_name=user.account_name
            userInfo={
                    "user_id":user.id,
                    "name":account_name,
                    "pic":pic,
                    "rating":rating
                    # "shop_rate":shop.id,
            }
            responseData.update({'data':userInfo}) 

            responseData['ret_val'] = '買家資訊取得成功'
    return JsonResponse(responseData) 

# 更新預設買家地址 is_default
def userAddress_isDefault(request): 
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        user_id= request.POST.get('user_id', '')
        user_address_id = request.POST.get('user_address_id', '')

        user_address_default_olds=models.User_Address.objects.filter(user_id=user_id)
        for user_address_default_old in user_address_default_olds:
            user_address_default_old.is_default='N'
            user_address_default_old.save()

        user_address_default=models.User_Address.objects.get(id=user_address_id)
        user_address_default.is_default='Y'
        user_address_default.save()

        responseData['status'] =0
        responseData['ret_val'] = '預設買家地址設定成功!'

    return JsonResponse(responseData)

def shopping_list(request): 
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    } 
    if request.method=='POST':
        user_id=request.POST.get('user_id', '')
        status=request.POST.get('status', '')

    
        if responseData['status']==0:
            orders=models.Shop_Order.objects.filter(user_id=user_id,status=status)

            for order in orders:
                productID=[]
                sub_total=0
                shop=models.Shop.objects.get(id=order.shop_id)
                getProductIDs=models.Shop_Order_Details.objects.filter(order_id=order.id)
                
                for getProductID in getProductIDs:
                    productID.append(getProductID.product_id)

                product=models.Product.objects.get(id=productID[0])
                product_pic=models.Selected_Product_Pic.objects.get(product_id=product.id,cover='y')
                product_count=models.Shop_Order_Details.objects.filter(order_id=order.id).count()
                orderInfo={
                    "order_id":order.id,
                    "order_number":order.order_number,
                    "shop_id":shop.id,
                    "shop_title":shop.shop_title,
                    "shop_icon":shop.shop_icon,
                    "product_pic":product_pic.product_pic,
                    "count":product_count
                    # status中文顯示(待收貨、已完成...等)? if status =='xxx': return status="中文"
                }
                details=models.Shop_Order_Details.objects.filter(order_id=order.id)
                for detail in details:
                    sub_total+=detail.quantity*detail.unit_price+detail.logistic_fee
                orderInfo["sub_total"]=sub_total
                responseData['data'].append(orderInfo) 

            responseData['ret_val'] = '買家資訊取得成功'
    return JsonResponse(responseData) 

def order_detail(request,order_id): 
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    } 
    if request.method=='GET':
        if responseData['status']==0:
            order=models.Shop_Order.objects.get(id=order_id)
            shop=models.Shop.objects.get(id=order.shop_id)
            subtotal=0
            orderInfo={
                "status":order.status,
                "shipment_info":order.product_shipment_desc,
                "name_in_address":order.name_in_address, 
                "phone":order.phone,
                "full_address":order.full_address,
                "shop_id":shop.id,
                "shop_title":shop.shop_title, 
                "shop_icon" : shop.shop_icon,
                "productList":[],
                "subtotal":0, #小計，由後端計算，有多個商品加總
                # "unit_price":order.unit_price,
                "shipment_price":0,
                "bill":0, #訂單金額
                "payment_desc":order.payment_desc,
                "order_number":order.order_number,
                "pay_time":order.updated_at #付款時間 (tbc)
            }
            orderDetails=models.Shop_Order_Details.objects.filter(order_id=order.id)
            for orderDetail in orderDetails:
                productPic=models.Selected_Product_Pic.objects.get(product_id=orderDetail.product_id,cover='y')
                productList={
                    "product_id":orderDetail.product_id,
                    "product_title":orderDetail.product_description,
                    "product_spec_id":orderDetail.product_spec_id,
                    "spec_desc_1":orderDetail.spec_desc_1,
                    "spec_desc_2":orderDetail.spec_desc_2,
                    "spec_dec_1_items":orderDetail.spec_dec_1_items,
                    "spec_dec_2_items":orderDetail.spec_dec_2_items,
                    "quantity":orderDetail.quantity, #or purchasing_qty (tbc)
                    "product_pic":productPic.product_pic,
                    "price":orderDetail.unit_price
                }
                subtotal+=orderDetail.quantity*orderDetail.unit_price
                orderInfo["productList"].append(productList)
            orderInfo.update({"subtotal":subtotal})

            responseData['data'].append(orderInfo)
            responseData['ret_val'] = '訂單詳情取得成功'
    return JsonResponse(responseData) 