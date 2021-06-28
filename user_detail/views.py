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

# Create your views here.

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
                        responseData['status'] = -5
                        responseData['ret_val'] = '用戶名稱格式錯誤!'
                        return JsonResponse(responseData)
                    else:
                        user.account_name=user_name               
                elif gender !='':
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
        'data': []
    } 
    if request.method=='GET':
        if responseData['status']==0:
            user=models.User.objects.get(id=user_id)
            userInfo={
                    "user_id":user.id,
                    "name":user.account_name,
                    "gender":user.gender,
                    "birthday":user.birthday,
                    "phone":user.phone,
                    "email":user.email,
                    # "shop_rate":shop.id,
                }
            responseData['data'].append(userInfo) 

            responseData['ret_val'] = '買家資訊取得成功'
    return JsonResponse(responseData) 