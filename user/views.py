from django.db.models import Q, Avg, Min, Max, Count, Sum
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.contrib.auth.hashers import make_password,check_password
from passlib.handlers.django import django_pbkdf2_sha256
from django.core import mail
from django.utils.html import strip_tags
from django.db import transaction
from hkshopu import models
from utils.upload_tools import upload_file
import uuid
import datetime
import re
import random
import json

# Create your views here.

# 會員註冊頁面
def register(request):
    template = get_template('register.html')
    html = template.render()
    return HttpResponse(html)
# 測試邀請電子郵件頁面
def page_of_invitation_email(request):
    template = get_template('invitation_testing_mail.html')
    html = template.render()
    return HttpResponse(html)
# 檢查電子郵件是否已存在
def checkEmailExistsProcess(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        email = request.POST.get('email', '')

        if response_data['status'] == 0:
            users = models.User.objects.filter(email=email)
            if len(users) > 0:
                response_data['status'] = -1
                response_data['ret_val'] = '該電子郵件已存在!'

        if response_data['status'] == 0:
            response_data['ret_val'] = '該電子郵件沒有重複使用!'
    return JsonResponse(response_data)
# 確認電子郵件是否透過社群登入
def checkEmailIsAllowedLoginProcess(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        email = request.POST.get('email', '')

        if response_data['status'] == 0:
            try:
                user = models.User.objects.get(email=email)
            except:
                response_data['status'] = -1
                response_data['ret_val'] = '該電子郵件未被使用!'

        if response_data['status'] == 0:
            if not(user.password):
                response_data['status'] = -2
                response_data['ret_val'] = '該電子郵件只可透過社群登入!'

        if response_data['status'] == 0:
            response_data['ret_val'] = '該電子郵件可正常登入!'
    return JsonResponse(response_data)
# 會員註冊
def registerProcess(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'user_id': ''
    }
    if request.method == 'POST':
        # 取得欄位資料
        accountName = request.POST.get('account_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirmPassword = request.POST.get('confirm_password', '')
        firstName = request.POST.get('first_name', '')
        lastName = request.POST.get('last_name', '')
        phone = request.POST.get('phone', '')
        gender = request.POST.get('gender', '')
        birthday = request.POST.get('birthday', '')
        address = request.POST.get('address', '')
        region = request.POST.get('region', '')
        district = request.POST.get('district', '')
        street_name = request.POST.get('street_name', '')
        street_no = request.POST.get('street_no', '')
        floor = request.POST.get('floor', '')
        room = request.POST.get('room', '')
        # 判斷欄位資料是否符合要求格式
        if responseData['status'] == 0:
            if accountName:
                if not(re.match('^[A-Za-z]{3,45}$', accountName)):
                    responseData['status'] = -1
                    responseData['ret_val'] = '用戶名稱格式錯誤!'

        if responseData['status'] == 0:
            if not(re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', email)):
                responseData['status'] = -2
                responseData['ret_val'] = '電子郵件格式錯誤!'

        if responseData['status'] == 0:
            if not(re.match('^(?!.*[^\x21-\x7e])(?=.{8,16})(?=.*[\W])(?=.*[a-zA-Z])(?=.*\d).*$', password)):
                responseData['status'] = -3
                responseData['ret_val'] = '密碼格式錯誤!'

        if responseData['status'] == 0:
            if confirmPassword != password:
                responseData['status'] = -4
                responseData['ret_val'] = '兩次密碼輸入不一致!'

        if responseData['status'] == 0:
            if firstName:
                if not(re.match('^[A-Za-z\u4e00-\u9fa5]{1,45}$', firstName)):
                    responseData['status'] = -5
                    responseData['ret_val'] = '名字格式錯誤!'
            else:
                firstName = str(email).split('@')[0]

        if responseData['status'] == 0:
            if lastName:
                if not(re.match('^[A-Za-z\u4e00-\u9fa5]{1,45}$', lastName)):
                    responseData['status'] = -6
                    responseData['ret_val'] = '姓氏格式錯誤!'

        if responseData['status'] == 0:
            if phone:
                if not(re.match('^[0-9]{8,10}$', phone)):
                    responseData['status'] = -7
                    responseData['ret_val'] = '手機號碼格式錯誤!'
        if responseData['status'] == 0:
            if gender:
                if not(re.match('^[M|F|O]{1}$', gender)):
                    responseData['status'] = -8
                    responseData['ret_val'] = '性別格式錯誤!'

        if responseData['status'] == 0:
            if birthday:
                if not(re.match('^[0-9]{2}\/[0-9]{2}\/[0-9]{4}$', birthday)):
                    responseData['status'] = -9
                    responseData['ret_val'] = '出生日期格式錯誤!'

        if responseData['status'] == 0:
            if address:
                if not(re.match('^[A-Za-z0-9\u4e00-\u9fa5]{1,95}$', address)):
                    responseData['status'] = -10
                    responseData['ret_val'] = '居住地址格式錯誤!'

        if responseData['status'] == 0:
            if region:
                if not(re.match('^[A-Za-z\u4e00-\u9fa5]{1,45}$', region)):
                    responseData['status'] = -11
                    responseData['ret_val'] = '地域格式錯誤!'

        if responseData['status'] == 0:
            if district:
                if not(re.match('^[A-Za-z\u4e00-\u9fa5]{1,45}$', district)):
                    responseData['status'] = -12
                    responseData['ret_val'] = '地區格式錯誤!'

        if responseData['status'] == 0:
            if street_name:
                if not(re.match('^[A-Za-z\u4e00-\u9fa5]{1,45}$', street_name)):
                    responseData['status'] = -13
                    responseData['ret_val'] = '街道名稱格式錯誤!'

        if responseData['status'] == 0:
            if street_no:
                if not(re.match('^[0-9\u4e00-\u9fa5]{1,45}$', street_no)):
                    responseData['status'] = -14
                    responseData['ret_val'] = '街道門牌格式錯誤!'

        if responseData['status'] == 0:
            if floor:
                if not(re.match('^[0-9\u4e00-\u9fa5]{1,45}$', floor)):
                    responseData['status'] = -15
                    responseData['ret_val'] = '樓層格式錯誤!'

        if responseData['status'] == 0:
            if room:
                if not(re.match('^[0-9\u4e00-\u9fa5]{1,45}$', room)):
                    responseData['status'] = -16
                    responseData['ret_val'] = '室格式錯誤!'
        # 判斷使用者是否使用相同電子郵件重複註冊
        if responseData['status'] == 0:
            try:
                user = models.User.objects.get(email=email)
                responseData['status'] = -17
                responseData['ret_val'] = '該電子郵件已被使用!'
            except:
                pass
                
        if responseData['status'] == 0:
            models.User.objects.create(
                id=uuid.uuid4(),
                account_name=accountName, 
                email=email, 
                password=make_password(password), 
                first_name=firstName, 
                last_name=lastName, 
                phone=phone, 
                gender=gender, 
                birthday=birthday, 
                address=address, 
                region=region, 
                district=district, 
                street_name=street_name, 
                street_no=street_no, 
                floor=floor, 
                room=room
            )
            try:
                user = models.User.objects.get(email=email)
                responseData['user_id'] = user.id
                # 預設將使用者登入
                request.session['user'] = {
                    'id': user.id, 
                    'account_name': user.account_name, 
                    'email': user.email, 
                    'first_name': user.first_name, 
                    'last_name': user.last_name
                }
            except:
                pass
            responseData['ret_val'] = '註冊成功!'
    return JsonResponse(responseData)
# 產生並發送驗證碼到使用者電子郵件
def generateAndSendValidationCodeProcess(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        email = request.POST.get('email', '')
        # 檢查使用者是否登入
        if response_data['status'] == 0:
            try:
                user = models.User.objects.get(email=email)
            except:
                response_data['status'] = -1
                response_data['ret_val'] = '該電子郵件未被使用!'

        if response_data['status'] == 0:
            # 產生帳號註冊驗證碼
            rand_str = ''
            needle = '0123456789'
            for j in range(4):
                rand_str += random.choice(needle)
            # 判斷資料表中是否已有使用者電子郵件和驗證碼，若沒有則新增，若有則更新
            try:
                user_validation = models.Email_Validation.objects.get(email=email)
                user_validation.validation_code = rand_str
                user_validation.save()
            except:
                models.Email_Validation.objects.create(
                    id=uuid.uuid4(),
                    user_id=user.id, 
                    email=user.email, 
                    validation_code=rand_str
                )
            # 發送電子郵件，告知帳號註冊驗證碼
            subject = 'HKShopU - 會員電子郵件驗證'
            html_message = render_to_string('validation_mail.html', {'validation_code': rand_str})
            message = strip_tags(html_message)
            from_email = 'info@hkshopu.com'
            recipient_list = [user.email, ]
            mail.send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, html_message=html_message)
            response_data['ret_val'] = '已寄出驗證碼!'
    return JsonResponse(response_data)
# 驗證電子郵件
def validateEmailProcess(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 取得欄位資料
        email = request.POST.get('email', '')
        validation_code = request.POST.get('validation_code', '')
        # 確認電子郵件是否存在
        if response_data['status'] == 0:
            try:
                user = models.User.objects.get(email=email)
            except:
                response_data['status'] = -1
                response_data['ret_val'] = '該電子郵件不存在!'
        # 確認電子郵件及驗證碼是否正確
        if response_data['status'] == 0:
            try:
                user_validation = models.Email_Validation.objects.get(email=email, validation_code=validation_code)
            except:
                response_data['status'] = -2
                response_data['ret_val'] = '電子郵件或驗證碼錯誤!'

        if response_data['status'] == 0:
            now = datetime.datetime.now()
            updated_at = user_validation.updated_at
            if (now - updated_at).min > datetime.timedelta(minutes=10):
                response_data['status'] = -3
                response_data['ret_val'] = '驗證碼已過期，請重新產生!'

        if response_data['status'] == 0:
            user.activated = 'Y'
            user.save()
            response_data['ret_val'] = '驗證成功!'
    return JsonResponse(response_data)
# 會員登入
def loginProcess(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'user_id': ''
    }
    if request.method == 'POST':
        # 取得欄位資料
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        # 驗證使用者輸入的電子郵件與密碼是否正確
        if responseData['status'] == 0:
            if not(email) or not(password):
                responseData['status'] = -1
                responseData['ret_val'] = '電子郵件或密碼未填寫!'

        if responseData['status'] == 0:
            try:
                user = models.User.objects.get(email=email)
            except:
                responseData['status'] = -2
                responseData['ret_val'] = '電子郵件錯誤!'

        if responseData['status'] == 0:
            if not(user.password):
                responseData['status'] = -3
                responseData['ret_val'] = '此電子郵件僅透過社群帳號註冊使用，請選擇社群登入!'

        if responseData['status'] == 0:
            if not(django_pbkdf2_sha256.verify(password, user.password)):
                responseData['status'] = -4
                responseData['ret_val'] = '密碼錯誤!'

        if responseData['status'] == 0:
            request.session['user'] = {
                'id': user.id, 
                'account_name': user.account_name, 
                'email': user.email, 
                'first_name': user.first_name, 
                'last_name': user.last_name
            }
            responseData['user_id'] = user.id
            responseData['ret_val'] = '登入成功!'
    return JsonResponse(responseData)
# 社群登入
def socialLoginProcess(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'user_id': ''
    }
    if request.method == 'POST':
        # 欄位資料
        email = request.POST.get('email', '')
        googleAccount = request.POST.get('google_account', '')
        facebookAccount = request.POST.get('facebook_account', '')
        appleAccount = request.POST.get('apple_account', '')

        if responseData['status'] == 0:
            if googleAccount and email:
                try:
                    user = models.User.objects.get(email=email)
                    user.google_account = googleAccount
                    user.save()
                    responseData['user_id'] = user.id
                    responseData['ret_val'] = '已使用 Google 帳戶登入!'
                    responseData['status'] = 1
                except:
                    models.User.objects.create(
                        id=uuid.uuid4(),
                        google_account=googleAccount, 
                        email=email
                    )
                    responseData['user_id'] = models.User.objects.order_by('-updated_at')[0].id
                    responseData['ret_val'] = '已使用 Google 帳戶註冊!'
                    responseData['status'] = -1

        if responseData['status'] == 0:
            if facebookAccount and email:
                try:
                    user = models.User.objects.get(email=email)
                    user.facebook_account = facebookAccount
                    user.save()
                    responseData['user_id'] = user.id
                    responseData['ret_val'] = '已使用 Facebook 帳戶登入!'
                    responseData['status'] = 2
                except:
                    models.User.objects.create(
                        id=uuid.uuid4(),
                        facebook_account=facebookAccount, 
                        email=email
                    )
                    responseData['user_id'] = models.User.objects.order_by('-updated_at')[0].id
                    responseData['ret_val'] = '已使用 Facebook 帳戶註冊!'
                    responseData['status'] = -2

        if responseData['status'] == 0:
            if appleAccount:
                try:
                    user = models.User.objects.get(apple_account=appleAccount)
                    responseData['user_id'] = user.id
                    responseData['ret_val'] = '已使用 Apple 帳戶登入!'
                    responseData['status'] = 3
                except:
                    if email != '':
                        try:
                            user = models.User.objects.get(email=email)
                            user.apple_account = appleAccount
                            user.save()
                            responseData['user_id'] = user.id
                            responseData['ret_val'] = '已使用 Apple 帳戶登入!'
                            responseData['status'] = 3
                        except:
                            models.User.objects.create(
                                id=uuid.uuid4(),
                                apple_account=appleAccount, 
                                email=email
                            )
                            responseData['user_id'] = models.User.objects.order_by('-updated_at')[0].id
                            responseData['ret_val'] = '已使用 Apple 帳戶註冊!'
                            responseData['status'] = -3
                    else:
                        responseData['ret_val'] = 'Social Login Error'
                        responseData['status'] = -4
    return JsonResponse(responseData)
# 忘記密碼
def forgetPasswordProcess(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        email = request.POST.get('email', '')

        if responseData['status'] == 0:
            if not(email):
                responseData['status'] = -1
                responseData['ret_val'] = '電子郵件未填寫!'

        if responseData['status'] == 0:
            try:
                user = models.User.objects.get(email=email)
            except:
                responseData['status'] = -2
                responseData['ret_val'] = '電子郵件錯誤或未被使用!'

        if responseData['status'] == 0:
            # 產生隨機字串
            seed = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+'
            i = 1
            while i > 0:
                randStrList = []
                for i in range(8):
                    randStrList.append(random.choice(seed))
                token = ''.join(randStrList)
                # 確認資料表中沒有重複的 Token
                users = models.User.objects.filter(forget_password_token=token)
                i = len(users)
            # 更新使用者的 Token
            user.forget_password_token = token
            user.save()
            # 發送忘記密碼通知信
            subject = 'HKShopU - 忘記密碼'
            htmlMessage = render_to_string('forget_password_mail.html', {'id': user.id, 'account_name': user.account_name, 'token': user.forget_password_token})
            message = strip_tags(htmlMessage)
            fromEmail = 'info@hkshopu.com'
            toEmail = [email, ]
            mail.send_mail(subject=subject, message=message, from_email=fromEmail, recipient_list=toEmail, html_message=htmlMessage)
            responseData['ret_val'] = '已發送重設密碼連結至您的電子郵件!'
    return JsonResponse(responseData)
# 會員密碼更新
def resetPasswordProcess(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        # 檢查電子郵件是否存在
        if response_data['status'] == 0:
            try:
                user = models.User.objects.get(email=email)
            except:
                response_data['status'] = -1
                response_data['ret_val'] = '該電子郵件不存在或未被使用!'
        # 檢查密碼格式是否正確
        if response_data['status'] == 0:
            if not(re.match('^(?!.*[^\x21-\x7e])(?=.{8,16})(?=.*[\W])(?=.*[a-zA-Z])(?=.*\d).*$', password)):
                response_data['status'] = -2
                response_data['ret_val'] = '密碼格式錯誤!'
        # 檢查兩次密碼輸入是否一致
        if response_data['status'] == 0:
            if confirm_password != password:
                response_data['status'] = -3
                response_data['ret_val'] = '兩次密碼輸入不一致!'
        # 更新會員密碼
        if response_data['status'] == 0:
            user.password = make_password(password)
            user.save()
            response_data['ret_val'] = '密碼修改成功!'
    return JsonResponse(response_data)
# 使用者商店列表
def getUserShopListProcess(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }

    if request.method == 'GET':
        if responseData['status'] == 0:
            shops = models.Shop.objects.filter(user_id=id,is_delete='N')
            if len(shops) == 0:
                responseData['status'] = 1
                responseData['ret_val'] = '您尚未建立任何商店!'
        
        if responseData['status'] == 0:
            for shop in shops:
                products = models.Product.objects.filter(shop_id=shop.id,is_delete='N')
                shopInfo = {
                    'id': shop.id, 
                    'shop_title': shop.shop_title, 
                    'shop_icon': shop.shop_icon, 
                    'shop_pic': shop.shop_pic,
                    'product_count': len(products),
                    'rating': 0,
                    'follower': 0,
                    'income': 0
                }
                responseData['data'].append(shopInfo)
            responseData['ret_val'] = '已取得您的商店清單!'
    return JsonResponse(responseData)
# 取得會員資料
def getUserListProcess(request):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'user_list': []
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            users = models.User.objects.all()
            if len(users) == 0:
                response_data['status'] = 1
                response_data['ret_val'] = '目前尚未存在任何會員!'
            
        if response_data['status'] == 0:
            for user in users:
                user_info = {
                    'id': user.id, 
                    'account_name': user.account_name, 
                    'google_account': user.google_account, 
                    'facebook_account': user.facebook_account, 
                    'apple_account': user.apple_account, 
                    'email': user.email, 
                    'password': user.password, 
                    'first_name': user.first_name, 
                    'last_name': user.last_name, 
                    'phone': user.phone, 
                    'gender': user.gender, 
                    'birthday': user.birthday, 
                    'address': user.address, 
                    'region': user.region, 
                    'district': user.district, 
                    'street_name': user.street_name, 
                    'street_no': user.street_no, 
                    'floor': user.floor, 
                    'room': user.room, 
                    'forget_password_token': user.forget_password_token, 
                    'activated': user.activated, 
                    'created_at': user.created_at, 
                    'updated_at': user.updated_at
                }
                response_data['user_list'].append(user_info)
            response_data['ret_val'] = '取得會員資料成功!'
    return JsonResponse(response_data)
# 取得單一用戶資料
def show(request, id):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'user_data': {}
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            try:
                user = models.User.objects.get(id=id)
            except:
                response_data['status'] = 1
                response_data['ret_val'] = '找不到此使用者編號的資料!'

        if response_data['status'] == 0:
            response_data['user_data']['id'] = user.id
            response_data['user_data']['account_name'] = user.account_name
            response_data['user_data']['google_account'] = user.google_account
            response_data['user_data']['facebook_account'] = user.facebook_account
            response_data['user_data']['apple_account'] = user.apple_account
            response_data['user_data']['email'] = user.email
            response_data['user_data']['first_name'] = user.first_name
            response_data['user_data']['last_name'] = user.last_name
            response_data['user_data']['phone'] = user.phone
            response_data['user_data']['gender'] = user.gender
            response_data['user_data']['birthday'] = user.birthday
            response_data['user_data']['address'] = user.address
            response_data['user_data']['region'] = user.region
            response_data['user_data']['district'] = user.district
            response_data['user_data']['street_name'] = user.street_name
            response_data['user_data']['street_no'] = user.street_no
            response_data['user_data']['floor'] = user.floor
            response_data['user_data']['room'] = user.room
            response_data['user_data']['activated'] = user.activated
            response_data['user_data']['created_at'] = user.created_at
            response_data['user_data']['updated_at'] = user.updated_at
            response_data['ret_val'] = '已取得使用者資料!'
    return JsonResponse(response_data)
# 取得使用者商店總數
def getUserShopCount(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }

    if request.method == 'GET':        
        if responseData['status'] == 0:
            shops = models.Shop.objects.filter(user_id=id,is_delete='N')
            shopInfo = {
                'shop_count': len(shops)
            }
            responseData['data'].append(shopInfo)
            responseData['ret_val'] = '已取得您的商店總數!'
    return JsonResponse(responseData)
# 發送電子郵件邀請使用者參與測試頁面
def send_invitation_testing_mail_page(request):
    template = get_template('invitation_testing_mail/index.html')
    html = template.render()
    return HttpResponse(html)
# 發送電子郵件邀請使用者參與測試
def send_invitation_testing_mail(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        email = request.POST.get('email', '')

        if response_data['status'] == 0:
            if not(email):
                response_data['status'] = -1
                response_data['ret_val'] = '未填寫電子郵件!'

        if response_data['status'] == 0:
            email = str(email).split(',')
            subject = 'HKShopU - 參與測試邀請'
            html_message = render_to_string('invitation_testing_mail.html')
            message = strip_tags(html_message)
            from_email = 'info@hkshopu.com'
            for x in email:
                mail.send_mail(subject=subject, message=message, from_email=from_email, recipient_list=[x, ] , html_message=html_message)
            response_data['ret_val'] = '發送參與測試邀請電子郵件成功!'
    return JsonResponse(response_data)

# 收藏商店
def followShop(request, user_id='', shop_id=''):
    response_data = {
        'status': 0, 
        'ret_val': '',
        'data': []
    }
    if request.method=='POST':

        follow = request.POST.get('follow')

        try:
            models.User.objects.get(id=user_id)
        except:
            response_data['status'], response_data['ret_val'] = -1, '尚未登入'
        
        if response_data['status'] == 0:
            try:
                models.Shop.objects.get(id=shop_id)
            except:
                response_data['status'], response_data['ret_val'] = -2, '無此商店編號'
        
        if response_data['status'] == 0:
            if follow != 'Y' and follow != 'N':
                response_data['status'], response_data['ret_val'] = -4, 'follow只能為Y|N'


        if response_data['status'] == 0:
            follows = models.Shop_Follower.objects.filter(shop_id=shop_id, follower_id=user_id)
            try:                
                if follow == 'Y' and len(follows)==0:
                    models.Shop_Follower.objects.create(
                        id=uuid.uuid4(),                
                        shop_id=shop_id,
                        follower_id=user_id
                    )
                    response_data['ret_val'] = '收藏成功'
                elif follow=='N' and len(follows)>0:
                    follows.delete()
                    response_data['ret_val'] = '取消收藏成功'
            except:
                response_data['status'], response_data['ret_val'] = -3, '收藏商店錯誤'


    
    return JsonResponse(response_data)

# 推薦商品詳情
def topProductDetail(request, user_id='', product_id=''):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': []
    }
    if request.method == 'GET':
        if responseData['status'] == 0:
            try:
                if user_id is not '':
                    models.User.objects.get(id=user_id)
            except:
                responseData['status'], responseData['ret_val'] = -1, '使用者不存在'

        if responseData['status'] == 0:
            try:
                product = models.Product.objects.get(id=product_id, is_delete='N')
            except:
                responseData['status'], responseData['ret_val'] = -2, '商品不存在'
        
        if responseData['status'] == 0:
            product_attr = [
                'product_title', # name
                'shop_id',
                'new_secondhand',
                'product_description', # description
                ]
            tempData = {}
            for attr in product_attr:
                if hasattr(product, attr):
                    tempData[attr] = getattr(product, attr)
            tempData['pic'] = list(models.Selected_Product_Pic.objects.filter(product_id=product_id).order_by('seq').values_list('product_pic', flat=True))[0:5]
            tempData['liked_count'] = len(models.Product_Liked.objects.filter(product_id=product_id))
            tempData['category'] = models.Product_Category.objects.get(id=product.product_category_id).c_product_category + '>' + models.Product_Sub_Category.objects.get(id=product.product_sub_category_id).c_product_sub_category
            rating = models.Product_Rate.objects.filter(product_id=product_id).aggregate(Avg('rating'))['rating__avg']
            tempData['average_rating'] = 0 if rating is None else rating
            min_max_spec = models.Product_Spec.objects.filter(product_id=product_id).aggregate(min_price=Min('price'), max_price=Max('price'), min_quantity=Min('quantity'), max_quantity=Max('quantity'))
            for k in min_max_spec:
                tempData[k] = min_max_spec[k] if min_max_spec[k] is not None else product.product_price if 'price' in k else product.quantity
            min_max_shipment = models.Product_Shipment_Method.objects.filter(product_id=product_id, onoff='on').aggregate(min_shipment=Min('price'), max_shipment=Max('price'))
            for k in min_max_shipment:
                tempData[k] = min_max_shipment[k]
            selling_count = models.Shop_Order_Details.objects.filter(product_id=product_id).aggregate(selling_count=Sum('purchasing_qty'))['selling_count']
            tempData['selling_count'] = 0 if selling_count is None else selling_count
            liked_count = models.Product_Liked.objects.filter(product_id=product_id).aggregate(liked_count=Count('user_id'))['liked_count']
            tempData['liked_count'] = 0 if liked_count is None else liked_count
            tempData['liked'] = 'Y' if len(models.Product_Liked.objects.filter(user_id=user_id,product_id=product_id))>0 else 'N'
            tempData['product_spec_on'] = product.product_spec_on
            tempData['longterm_stock_up'] = product.longterm_stock_up
            responseData['data'].append(tempData)

            models.Product_Clicked.objects.create(
                id=uuid.uuid4(),
                user_id=user_id,
                product_id=product_id
            )
        
    return JsonResponse(responseData)

# 新增Audit Log
def auditLog(request, user_id=''):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': {}
    }

    if user_id != '':
        try:
            models.User.objects.get(id=user_id)
        except:
            responseData['status'], responseData['ret_val'] = -1, '使用者不存在'

    if request.method == 'POST': # insert
        action = request.POST.get('action', '')
        parameter_in = request.POST.get('parameter_in', '')
        parameter_out = request.POST.get('parameter_out', '')
        models.Audit_Log.objects.create(
            id = uuid.uuid4(),
            user_id = user_id,
            action = action,
            parameter_in = parameter_in,
            parameter_out = parameter_out
        )
        responseData['ret_val'] = '新增成功'

    return JsonResponse(responseData)

def paymentAccount(request, user_id='', id=''):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': {}
    }
    if request.method == 'GET':
        try:
            models.User.objects.get(id=user_id)
        except:
            responseData['status'], responseData['ret_val'] = -1, '無此使用者'
        if responseData['status'] == 0:
            payment_account_attr = [
                'id',
                'payment_type',
                'bank_code',
                'bank_name',
                'bank_account_name',
                'contact_type',
                'phone_country_code',
                'phone_number',
                'contact_email',
                'is_default'
            ]
            payment_accounts = models.User_Payment_Account.objects.filter(user_id=user_id).order_by('-is_default')
            responseData['data'] = []
            for account in payment_accounts:
                temp_data = {}
                for attr in payment_account_attr:
                    if hasattr(account, attr):
                        temp_data[attr] = getattr(account, attr)
                responseData['data'].append(temp_data)

    elif request.method == 'POST': # add
        payment_type = request.POST.get('payment_type','')
        bank_code = request.POST.get('bank_code','')
        bank_name = request.POST.get('bank_name','')
        bank_account_name = request.POST.get('bank_account_name', '')
        contact_type = request.POST.get('contact_type','')
        phone_country_code = request.POST.get('phone_country_code','')
        phone_number = request.POST.get('phone_number','')
        contact_email = request.POST.get('contact_email','')
        is_default = request.POST.get('is_default')

        try:
            models.User.objects.get(id=user_id)
        except:
            responseData['status'], responseData['ret_val'] = -1, '無此使用者'
        if responseData['status'] == 0:
            if contact_type == 'email' and contact_email == '':
                responseData['status'], responseData['ret_val'] = -2, 'contact_email為必填'
            elif contact_type == 'phone':
                if phone_number == '':
                    responseData['status'], responseData['ret_val'] = -3, 'phone_number為必填'
                elif len(phone_number) != 8:
                    responseData['status'], responseData['ret_val'] = -4, 'phone_number長度只能為8'

        if responseData['status'] == 0:
            if not is_default:
                if len(models.User_Payment_Account.objects.filter(user_id=user_id, is_default='Y'))==0:
                    is_default='Y'
                else:
                    is_default='N'
            
            payment_account=models.User_Payment_Account.objects.create(
                id = uuid.uuid4(),
                payment_type = payment_type,
                user_id = user_id,
                bank_code = bank_code,
                bank_name = bank_name,
                bank_account_name = bank_account_name,
                contact_type = contact_type,
                phone_country_code = phone_country_code,
                phone_number = phone_number,
                contact_email = contact_email,
                is_default = is_default
            )
            responseData['data']['id'] = payment_account.id
            responseData['ret_val'] = '新增使用者付款方式成功'
            
    elif request.method == 'PATCH': # default account
        try:
            models.User_Payment_Account.objects.get(id=id)
        except:
            responseData['status'], responseData['ret_val'] = -1, '無此付款方式ID'
        if responseData['status'] == 0:
            payment_account = models.User_Payment_Account.objects.get(id=id)
            models.User_Payment_Account.objects.filter(user_id=payment_account.user_id, is_default='Y').update(is_default='N')
            payment_account.is_default = 'Y'
            payment_account.save()
            responseData['ret_val'] = '設定預設付款方式成功'
    elif request.method == 'DELETE': # delete
        try:
            models.User_Payment_Account.objects.get(id=id)
        except:
            responseData['status'], responseData['ret_val'] = -1, '無此付款方式ID'
        if responseData['status'] == 0:
            models.User_Payment_Account.objects.get(id=id).delete()
            responseData['ret_val'] = '刪除預設付款方式成功'
        
            
    return JsonResponse(responseData)

# 使用者編號驗證
def user_id_validation(request):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': {}
    }
    if request.method == 'POST':
        # 欄位資料
        user_id = request.POST.get('user_id', '')

        if response_data['status'] == 0:
            try:
                user = models.User.objects.get(id=user_id)
            except:
                response_data['data']['is_exists'] = 'N'
                response_data['status'] = -1
                response_data['ret_val'] = '該使用者不存在!'

        if response_data['status'] == 0:
            response_data['data']['is_exists'] = 'Y'
            response_data['ret_val'] = '該使用者存在!'
    return JsonResponse(response_data)

def adSettingRanking(request, ad_category='', ad_type=''):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': {}
    }
    try:
        if request.method == 'GET':
            keyword = request.GET.get('keyword')
            bid = request.GET.get('bid')
            header_ids = models.Ad_Setting_Header.objects.filter(ad_category=ad_category,ad_type=ad_type)
            ranking = models.Ad_Setting_Detail.objects.filter(ad_setting_header_id__in=header_ids,bid__gt=bid)
            if ad_category=='keyword':
                ranking = ranking.filter(keyword=keyword)
            responseData['ret_val'], responseData['data']['ranking'] = '成功', len(ranking)
    except:
        pass

    return JsonResponse(responseData)

def adSetting(request, user_id='', ad_category='', ad_type='',):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': {}
    }
    
    if request.method == 'POST': # CREATE Ad Setting
        budget_type = request.POST.get('budget_type')
        budget_amount = request.POST.get('budget_amount')
        ad_period_type = request.POST.get('ad_period_type')
        start_datetime = request.POST.get('start_datetime')
        end_datetime = request.POST.get('end_datetime')
        details = request.POST.get('details') # json type
        #/*
        # general validation
        if responseData['status'] == 0:
            try:
                models.User.objects.get(id=user_id)
            except:
                responseData['status'], responseData['ret_val'] = -1, '使用者不存在'
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Ad_Setting_Header.validate_column('ad_type', -2, ad_type)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Ad_Setting_Header.validate_column('budget_type', -3, budget_type)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Ad_Setting_Header.validate_column('budget_amount', -4, budget_amount)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Ad_Setting_Header.validate_column('ad_period_type', -5, ad_period_type)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Ad_Setting_Header.validate_column('start_datetime', -6, start_datetime)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Ad_Setting_Header.validate_column('end_datetime', -7, end_datetime)
        if responseData['status'] == 0:
            if ad_period_type=='custom' and start_datetime >= end_datetime:
                responseData['status'], responseData['ret_val'] = -8, 'start_datetime需小於end_datetime'
        if responseData['status'] == 0:
            try:
                details = json.loads(details)
            except:
                responseData['status'], responseData['ret_val'] = -9, 'JSON解析錯誤'
        if responseData['status'] == 0:
            for detail in details:
                if 'shop_id' not in detail or detail['shop_id'] == '':
                    detail['shop_id'] = None
                if 'product_id' not in detail or detail['product_id'] == '': 
                    detail['product_id'] = None                        
                    if not detail['shop_id']:
                        responseData['status'], responseData['ret_val'] = -12, 'product_id, shop_id 至少需要其中一個'
                        break
                if not detail['product_id'] and not models.Shop.objects.filter(id=detail['shop_id']).exists():
                    responseData['status'], responseData['ret_val'] = -10, 'shop_id不存在 -> '+str(detail['shop_id'])
                if not detail['shop_id'] and not models.Product.objects.filter(id=detail['product_id']).exists():
                    responseData['status'], responseData['ret_val'] = -11, 'product_id不存在 -> '+str(detail['product_id'])

                if 'keyword' not in detail or detail['keyword'] == '':                    
                    if ad_category == 'keyword':                    
                        responseData['status'], responseData['ret_val'] = -13, 'keyword不能為空'
                        break
                    else:
                        detail['keyword'] = None

                try:
                    if float(detail['bid']) < 0:
                        raise ValueError
                except: # catch KeyError & ValueError & TypeError
                    responseData['status'], responseData['ret_val'] = -14, 'bid只能為非負數'
                    break
        #*/
        #/*
        # default action
        if budget_type == 'unlimit': budget_amount = None
        if ad_period_type == 'unlimit': start_datetime = end_datetime = None
        status = 'running'
        #*/

        if ad_category == 'keyword':
            #/*
            # custom validation
            # 
            #*/
            if responseData['status'] == 0:
                try:
                    with transaction.atomic():
                        keyword_ad_setting_header = models.Ad_Setting_Header.objects.create(
                            id=uuid.uuid4(),
                            user_id=user_id,
                            ad_category=ad_category,
                            ad_type=ad_type,
                            budget_type=budget_type,
                            budget_amount=budget_amount,
                            ad_period_type=ad_period_type,
                            start_datetime=start_datetime,
                            end_datetime=end_datetime,
                            status=status
                        )
                        for detail in details:
                            models.Ad_Setting_Detail.objects.create(
                                id=uuid.uuid4(),
                                ad_setting_header_id=keyword_ad_setting_header.id,
                                shop_id=detail['shop_id'],
                                product_id=detail['product_id'],
                                keyword=detail['keyword'],
                                bid=detail['bid']
                            )
                    responseData['ret_val'] = '新增成功'
                    responseData['data']['id'] = keyword_ad_setting_header.id
                except:
                    responseData['status'], responseData['ret_val'] = -99, '新增失敗'
        elif ad_category == 'recommend':
            #/*
            # custom validation
            # 
            #*/
            if responseData['status'] == 0:
                try:
                    with transaction.atomic():
                        recommend_header = models.Ad_Setting_Header.objects.create(
                            id=uuid.uuid4(),
                            user_id=user_id,
                            ad_category=ad_category,
                            ad_type=ad_type,
                            budget_type=budget_type,
                            budget_amount=budget_amount,
                            ad_period_type=ad_period_type,
                            start_datetime=start_datetime,
                            end_datetime=end_datetime,
                            status=status
                        )
                        models.Ad_Setting_Detail.objects.create(
                            id=uuid.uuid4(),
                            ad_setting_header_id=recommend_header.id,
                            shop_id=details[0]['shop_id'],
                            product_id=details[0]['product_id'],
                            keyword=details[0]['keyword'],
                            bid=details[0]['bid']
                        )
                    responseData['ret_val'] = '新增成功'
                    responseData['data']['id'] = recommend_header.id
                    pass
                except:
                    responseData['status'], responseData['ret_val'] = -99, '新增失敗'
        elif ad_category == 'store':
            #/*
            # custom validation
            ad_img = request.FILES.get('ad_img')
            if not ad_img:
                responseData['status'], responseData['ret_val'] = -15, 'ad_img不可為空'
            elif not(re.match('^.+\.(gif|png|jpg|jpeg)$', str(ad_img.name))):
                responseData['status'], responseData['ret_val'] = -16, 'ad_img 應為 gif|png|jpg|jpeg'                
            #*/
            if responseData['status'] == 0:
                img_url = upload_file(ad_img,'images/ad/',suffix="ad_img")
                try:
                    with transaction.atomic():
                        store_header = models.Ad_Setting_Header.objects.create(
                            id=uuid.uuid4(),
                            user_id=user_id,
                            ad_category=ad_category,
                            ad_type=ad_type,
                            budget_type=budget_type,
                            budget_amount=budget_amount,
                            ad_period_type=ad_period_type,
                            start_datetime=start_datetime,
                            end_datetime=end_datetime,
                            status=status
                        )
                        models.Ad_Setting_Detail.objects.create(
                            id=uuid.uuid4(),
                            ad_setting_header_id=store_header.id,
                            ad_img=img_url,
                            shop_id=details[0]['shop_id'],
                            product_id=details[0]['product_id'],
                            keyword=details[0]['keyword'],
                            bid=details[0]['bid']
                        )
                    responseData['ret_val'] = '新增成功'
                    responseData['data']['id'] = store_header.id
                    pass
                except:
                    responseData['status'], responseData['ret_val'] = -99, '新增失敗'
                
    elif request.method == 'GET':
        if ad_category == 'keyword':
            pass
        elif ad_category == 'recommend':
            pass
        elif ad_category == 'store':
            pass
    return JsonResponse(responseData)

def updateAdSetting(request, ad_category='', ad_type='', ad_setting_header_id=''):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': {}
    }

    if request.method == 'POST': # UPDATE Ad Setting
        budget_type = request.POST.get('budget_type')
        budget_amount = request.POST.get('budget_amount')
        ad_period_type = request.POST.get('ad_period_type')
        start_datetime = request.POST.get('start_datetime')
        end_datetime = request.POST.get('end_datetime')
        details = request.POST.get('details') # json type
        #/*
        # general validation
        if responseData['status'] == 0:
            try:
                models.Ad_Setting_Header.objects.get(id=ad_setting_header_id)
            except:
                responseData['status'], responseData['ret_val'] = -1, '廣告不存在'
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Ad_Setting_Header.validate_column('ad_type', -2, ad_type)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Ad_Setting_Header.validate_column('budget_type', -3, budget_type)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Ad_Setting_Header.validate_column('budget_amount', -4, budget_amount)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Ad_Setting_Header.validate_column('ad_period_type', -5, ad_period_type)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Ad_Setting_Header.validate_column('start_datetime', -6, start_datetime)
        if responseData['status'] == 0:
            responseData['status'], responseData['ret_val'] = models.Ad_Setting_Header.validate_column('end_datetime', -7, end_datetime)
        if responseData['status'] == 0:
            if ad_period_type=='custom' and start_datetime >= end_datetime:
                responseData['status'], responseData['ret_val'] = -8, 'start_datetime需小於end_datetime'
        if responseData['status'] == 0:
            try:
                details = json.loads(details)
            except:
                responseData['status'], responseData['ret_val'] = -9, 'JSON解析錯誤'        
        if responseData['status'] == 0:
            for detail in details:
                if 'shop_id' not in detail or detail['shop_id'] == '':
                    detail['shop_id'] = None
                if 'product_id' not in detail or detail['product_id'] == '': 
                    detail['product_id'] = None
                    if not detail['shop_id']:
                        responseData['status'], responseData['ret_val'] = -12, 'product_id, shop_id 至少需要其中一個'
                        break
                if not detail['product_id'] and not models.Shop.objects.filter(id=detail['shop_id']).exists():
                    responseData['status'], responseData['ret_val'] = -10, 'shop_id不存在 -> '+str(detail['shop_id'])
                if not detail['shop_id'] and not models.Product.objects.filter(id=detail['product_id']).exists():
                    responseData['status'], responseData['ret_val'] = -11, 'product_id不存在 -> '+str(detail['product_id'])

                if 'keyword' not in detail or detail['keyword'] == '':                    
                    if ad_category == 'keyword':                    
                        responseData['status'], responseData['ret_val'] = -13, 'keyword不能為空'
                        break
                    else:
                        detail['keyword'] = None
                try:
                    if float(detail['bid']) < 0:
                        raise ValueError
                except: # catch KeyError & ValueError & TypeError
                    responseData['status'], responseData['ret_val'] = -14, 'bid只能為非負數'
                    break
        #*/        
        #/*
        # default action
        if budget_type == 'unlimit': budget_amount = None
        if ad_period_type == 'unlimit': start_datetime = end_datetime = None
        status = 'running'
        #*/

        if ad_category == 'keyword':
            #/*
            # custom validation
            # 
            #*/
            if responseData['status'] == 0:        
                with transaction.atomic():
                    models.Ad_Setting_Header.objects.filter(id=ad_setting_header_id).update(
                        budget_type=budget_type, 
                        budget_amount=budget_amount, 
                        ad_period_type=ad_period_type, 
                        start_datetime=start_datetime, 
                        end_datetime=end_datetime
                    )
                    keyword_ad_setting_detail_delete = models.Ad_Setting_Detail.objects.filter(ad_setting_header_id=ad_setting_header_id)
                    for detail in details:
                        keyword_ad_setting_detail = models.Ad_Setting_Detail.objects.filter(ad_setting_header_id=ad_setting_header_id, keyword=detail['keyword'])
                        row_count = len(keyword_ad_setting_detail)
                        if row_count == 0:
                            models.Ad_Setting_Detail.objects.create(
                                id=uuid.uuid4(),
                                ad_setting_header_id=ad_setting_header_id,
                                shop_id=detail['shop_id'],
                                product_id=detail['product_id'],
                                keyword=detail['keyword'],
                                bid=detail['bid']
                            )
                        elif row_count == 1:
                            models.Ad_Setting_Detail.objects.filter(id=ad_setting_header_id, keyword=detail['keyword']).update(
                                shop_id=detail['shop_id'],
                                product_id=detail['product_id'],
                                keyword=detail['keyword'],
                                bid=detail['bid']
                            )
                        keyword_ad_setting_detail_delete = keyword_ad_setting_detail_delete.filter(~Q(keyword=detail['keyword']))
                    if len(keyword_ad_setting_detail_delete) > 0:
                        keyword_ad_setting_detail_delete.delete()
                responseData['ret_val'] = '更新成功'    
                try:
                    pass    
                except:
                    responseData['status'], responseData['ret_val'] = -99, '更新失敗'
        elif ad_category == 'recommend':
            #/*
            # custom validation
            # 
            #*/
            if responseData['status'] == 0:
                try:
                    with transaction.atomic():
                        models.Ad_Setting_Header.objects.filter(id=ad_setting_header_id).update(
                            budget_type=budget_type, 
                            budget_amount=budget_amount, 
                            ad_period_type=ad_period_type, 
                            start_datetime=start_datetime, 
                            end_datetime=end_datetime
                        )
                        models.Ad_Setting_Detail.objects.filter(ad_setting_header_id=ad_setting_header_id).update(
                            shop_id=details[0]['shop_id'],
                            product_id=details[0]['product_id'],
                            keyword=details[0]['keyword'],
                            bid=details[0]['bid']
                        )
                    responseData['ret_val'] = '更新成功'
                except:
                    responseData['status'], responseData['ret_val'] = -99, '更新失敗'
        elif ad_category == 'store':
            #/*
            # custom validation
            ad_img = request.FILES.get('ad_img')
            if not ad_img:
                responseData['status'], responseData['ret_val'] = -15, 'img不可為空'
            elif not(re.match('^.+\.(gif|png|jpg|jpeg)$', str(ad_img.name))):
                responseData['status'], responseData['ret_val'] = -16, 'img 應為 gif|png|jpg|jpeg'                
            #*/
            if responseData['status'] == 0:
                img_url = upload_file(ad_img,'images/ad/',suffix="ad_img")
                try:
                    with transaction.atomic():
                        models.Ad_Setting_Header.objects.filter(id=ad_setting_header_id).update(
                            budget_type=budget_type, 
                            budget_amount=budget_amount, 
                            ad_period_type=ad_period_type, 
                            start_datetime=start_datetime, 
                            end_datetime=end_datetime
                        )
                        models.Ad_Setting_Detail.objects.filter(ad_setting_header_id=ad_setting_header_id).update(
                            ad_img=img_url,
                            shop_id=details[0]['shop_id'],
                            product_id=details[0]['product_id'],
                            keyword=details[0]['keyword'],
                            bid=details[0]['bid']
                        )
                    responseData['ret_val'] = '更新成功'
                except:
                    responseData['status'], responseData['ret_val'] = -99, '更新失敗'


    return JsonResponse(responseData)

def sale_list(request): 
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    } 
    if request.method=='POST':
        shop_id=request.POST.get('shop_id', '') #賣家
        status=request.POST.get('status', '')
        #logic : 賣家user_id search shop.id、product.id，比對order
    
        if responseData['status']==0:
            orders=models.Shop_Order.objects.filter(shop_id=shop_id,status=status)

            for order in orders:
                productID=[]
                sub_total=0
                getProductIDs=models.Shop_Order_Details.objects.filter(shop_order_id=order.id)
                
                for getProductID in getProductIDs:
                    productID.append(getProductID.product_id)

                product=models.Product.objects.get(id=productID[0])
                product_pic=models.Selected_Product_Pic.objects.get(product_id=product.id,cover='y')
                product_count=models.Shop_Order_Details.objects.filter(shop_order_id=order.id).count()
                user=models.User.objects.get(id=order.user_id)
                if user.pic==None:
                    user_pic=""
                else :
                    user_pic=user.pic
                orderInfo={
                    "order_id":order.id,
                    "order_number":order.order_number,
                    "product_pic":product_pic.product_pic,
                    "count":product_count,
                    "sub_total":0,
                    "buyer_id":user.id,
                    "buyer_name":user.account_name,
                    "buyer_pic":user_pic,
                    "shipment_info":order.product_shipment_desc
                }
                details=models.Shop_Order_Details.objects.filter(shop_order_id=order.id)
                for detail in details:
                    sub_total+=detail.quantity*detail.unit_price+detail.logistic_fee
                orderInfo["sub_total"]=sub_total
                
                responseData['data'].append(orderInfo) 

            responseData['ret_val'] = '訂單資訊取得成功'
    return JsonResponse(responseData)

from datetime import datetime
from datetime import date
def sale_order_detail(request,order_id): 
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'data': {}
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

            messages=models.Order_Message.objects.get(order_status=order.status)
            #傳中文 or 英文
            if order.status=='Pending Payment': 
                shop_message='待付款'+messages.shop_message_template.replace('<status>','')

            if order.status=='Pending Delivery': 
                d1 = order.estimated_deliver_at.strftime("%d/%m/%Y")
                print("d1 =", d1)
                shop_message='待發貨'+messages.shop_message_template.replace('<status>','').replace('<estimate_delivery_date>','').replace('前到貨','')+d1+'前到貨'

            if order.status=='Pending Good Receive': 
                d1 = order.actual_deliver_at.strftime("%d/%m/%Y")
                print("d1 =", d1)
                shop_message='待收貨'+messages.shop_message_template.replace('<status>','').replace('<actual_delivery_date>','').replace('前到貨','')+d1+'前到貨'

            if order.status=='Completed': 
                shop_message=messages.shop_message_template
                # order.status
            if order.status=='Cancelled': 
                shop_message=''
                # order.status
            if order.status=='Refunded': 
                shop_message=''
                # order.status
            orderInfo["shop_message"]=shop_message

            orderDetails=models.Shop_Order_Details.objects.filter(shop_order_id=order.id)
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
                    "price":orderDetail.unit_price,
                    "quantity":orderDetail.quantity, #or purchasing_qty (tbc)
                    "product_pic":productPic.product_pic
                }
                subtotal+=orderDetail.quantity*orderDetail.unit_price
                orderInfo["productList"].append(productList)
            orderInfo.update({"subtotal":subtotal})

            responseData['data']=orderInfo
            responseData['ret_val'] = '訂單詳情取得成功'
    return JsonResponse(responseData)    
