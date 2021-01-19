from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.contrib.auth.hashers import make_password
from passlib.handlers.django import django_pbkdf2_sha256
from django.core import mail
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from hkshopu import models
import re
import random
import datetime

# Create your views here.


# user

# 會員註冊頁面
def register(request):
    template = get_template('register.html')
    html = template.render()
    return HttpResponse(html)
# 會員註冊
def registerProcess(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
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
        # 判斷欄位資料是否符合要求格式
        if responseData['status'] == 0:
            if not(re.match('^[A-Za-z]{3,45}$', accountName)):
                responseData['status'] = -1
                responseData['ret_val'] = '用戶名稱格式錯誤!'

        if responseData['status'] == 0:
            if not(re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', email)):
                responseData['status'] = -2
                responseData['ret_val'] = '電子郵件格式錯誤!'

        if responseData['status'] == 0:
            if not(re.match('^.{6,20}$', password)):
                responseData['status'] = -3
                responseData['ret_val'] = '密碼格式錯誤!'

        if responseData['status'] == 0:
            if confirmPassword != password:
                responseData['status'] = -4
                responseData['ret_val'] = '兩次密碼輸入不一致!'

        if responseData['status'] == 0:
            if not(re.match('^[A-Za-z\u4e00-\u9fa5]{1,45}$', firstName)):
                responseData['status'] = -5
                responseData['ret_val'] = '名字格式錯誤!'

        if responseData['status'] == 0:
            if not(re.match('^[A-Za-z\u4e00-\u9fa5]{1,45}$', lastName)):
                responseData['status'] = -6
                responseData['ret_val'] = '姓氏格式錯誤!'

        if responseData['status'] == 0:
            if not(re.match('^09[0-9]{8}$', phone)):
                responseData['status'] = -7
                responseData['ret_val'] = '手機號碼格式錯誤!'
        if responseData['status'] == 0:
            if not(re.match('^[M|F]{1}$', gender)):
                responseData['status'] = -8
                responseData['ret_val'] = '性別格式錯誤!'

        if responseData['status'] == 0:
            if not(re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', birthday)):
                responseData['status'] = -9
                responseData['ret_val'] = '出生日期格式錯誤!'

        if responseData['status'] == 0:
            if not(re.match('^[A-Za-z\u4e00-\u9fa5]{10,95}$', address)):
                responseData['status'] = -10
                responseData['ret_val'] = '居住地址格式錯誤!'
        # 判斷使用者是否使用相同電子郵件或手機號碼重複註冊
        if responseData['status'] == 0:
            try:
                user = models.User.objects.get(Q(email=email) | Q(phone=phone))
                responseData['status'] = -11
                responseData['ret_val'] = '該電子郵件或手機號碼已被使用!'
            except:
                pass
                
        if responseData['status'] == 0:
            models.User.objects.create(
                account_name=accountName, 
                email=email, 
                password=make_password(password), 
                first_name=firstName, 
                last_name=lastName, 
                phone=phone, 
                gender=gender, 
                birthday=birthday, 
                address=address
            )
            responseData['ret_val'] = '註冊成功!'
    return JsonResponse(responseData)
# 會員登入
def loginProcess(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
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
            if not(django_pbkdf2_sha256.verify(password, user.password)):
                responseData['status'] = -3
                responseData['ret_val'] = '密碼錯誤!'

        if responseData['status'] == 0:
            request.session['user'] = {
                'id': user.id, 
                'account_name': user.account_name, 
                'email': user.email, 
                'first_name': user.first_name, 
                'last_name': user.last_name
            }
            responseData['ret_val'] = '登入成功!'
    return JsonResponse(responseData)
# 社群登入
def socialLoginProcess(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
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
                    responseData['ret_val'] = '已使用 Google 帳戶登入!'
                    responseData['status'] = 1
                except:
                    models.User.objects.create(
                        google_account=googleAccount, 
                        email=email
                    )
                    responseData['ret_val'] = '已使用 Google 帳戶註冊!'
                    responseData['status'] = -1

        if responseData['status'] == 0:
            if facebookAccount and email:
                try:
                    user = models.User.objects.get(email=email)
                    user.facebook_account = facebookAccount
                    user.save()
                    responseData['ret_val'] = '已使用 Facebook 帳戶登入!'
                    responseData['status'] = 2
                except:
                    models.User.objects.create(
                        facebook_account=facebookAccount, 
                        email=email
                    )
                    responseData['ret_val'] = '已使用 Facebook 帳戶註冊!'
                    responseData['status'] = -2

        if responseData['status'] == 0:
            if appleAccount and email:
                try:
                    user = models.User.objects.get(email=email)
                    user.apple_account = appleAccount
                    user.save()
                    responseData['ret_val'] = '已使用 Apple 帳戶登入!'
                    responseData['status'] = 3
                except:
                    models.User.objects.create(
                        apple_account=appleAccount, 
                        email=email
                    )
                    responseData['ret_val'] = '已使用 Apple 帳戶註冊!'
                    responseData['status'] = -3
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
            fromEmail = 'HKShopU'
            toEmail = [email, ]
            mail.send_mail(subject=subject, message=message, from_email=fromEmail, recipient_list=toEmail, html_message=htmlMessage)
            responseData['ret_val'] = '已發送重設密碼連結至您的電子郵件!'
    return JsonResponse(responseData)


# shop

# 新增商店頁面
def create(request):
    template = get_template('shop/create.html')
    html = template.render()
    return HttpResponse(html)

# 新增商店
def save(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }

    if request.method == 'POST':
        # 欄位資料
        shopIcon = request.FILES.get('shop_icon', '')
        shopTitle = request.POST.get('shop_title', '')
        shopCategoryId = request.POST.get('shop_category_id', 0)
        shopPic = request.FILES.get('shop_pic', '')
        shopDesc = request.POST.get('shop_desc', '')
        paypal = request.POST.get('paypal', '')
        visa = request.POST.get('visa', '')
        master = request.POST.get('master', '')
        apple = request.POST.get('apple', '')
        android = request.POST.get('android', '')
        isShipFree = request.POST.get('is_ship_free', '')
        shipFreeQuota = request.POST.get('ship_free_quota', 0)
        fixShipFee = request.POST.get('fix_ship_fee', 0)
        fixShipFeeFr = request.POST.get('fix_ship_fee_fr', 0)
        fixShipFeeTo = request.POST.get('fix_ship_fee_to', 0)
        shipByProduct = request.POST.get('ship_by_product', '')
        # 檢查使用者是否登入
        if responseData['status'] == 0:
            if not('user' in request.session):
                responseData['status'] = -1
                responseData['ret_val'] = '請先登入會員!'
        # 判斷必填欄位是否填寫及欄位格式是否正確
        if responseData['status'] == 0:
            if not(shopIcon):
                responseData['status'] = -2
                responseData['ret_val'] = '未上傳商店小圖!'

        if responseData['status'] == 0:
            if not(shopTitle):
                responseData['status'] = -3
                responseData['ret_val'] = '未填寫商店標題!'

        if responseData['status'] == 0:
            if not(shopCategoryId):
                responseData['status'] = -4
                responseData['ret_val'] = '未選擇商店類別!'

        if responseData['status'] == 0:
            if not(shopPic):
                responseData['status'] = -5
                responseData['ret_val'] = '未上傳商店主圖!'

        if responseData['status'] == 0:
            if not(shopDesc):
                responseData['status'] = -6
                responseData['ret_val'] = '未填寫商店描述!'

        if responseData['status'] == 0:
            if not(re.match('^\w+\.(gif|png|jpg|jpeg)$', str(shopIcon.name))):
                responseData['status'] = -7
                responseData['ret_val'] = '商店小圖格式錯誤!'

        if responseData['status'] == 0:
            if not(re.match('^\d+$', shopCategoryId)):
                responseData['status'] = -8
                responseData['ret_val'] = '商店分類格式錯誤!'

        if responseData['status'] == 0:
            if not(re.match('^\w+\.(gif|png|jpg|jpeg)$', str(shopPic.name))):
                responseData['status'] = -9
                responseData['ret_val'] = '商店主圖格式錯誤!'
        # 選填欄位若有填寫，則判斷其格式是否正確
        if responseData['status'] == 0:
            if paypal:
                if not(re.match('^\w+$', paypal)):
                    responseData['status'] = -10
                    responseData['ret_val'] = 'PayPal 格式錯誤!'

        if responseData['status'] == 0:
            if visa:
                if not(re.match('^\w+$', visa)):
                    responseData['status'] = -11
                    responseData['ret_val'] = 'Visa 卡格式錯誤!'

        if responseData['status'] == 0:
            if master:
                if not(re.match('^\w+$', master)):
                    responseData['status'] = -12
                    responseData['ret_val'] = 'Master 卡格式錯誤!'

        if responseData['status'] == 0:
            if apple:
                if not(re.match('^\w+$', apple)):
                    responseData['status'] = -13
                    responseData['ret_val'] = 'Apple 格式錯誤!'

        if responseData['status'] == 0:
            if android:
                if not(re.match('^\w+$', android)):
                    responseData['status'] = -14
                    responseData['ret_val'] = 'Android 格式錯誤!'

        if responseData['status'] == 0:
            if isShipFree:
                if not(re.match('^\w+$', isShipFree)):
                    responseData['status'] = -15
                    responseData['ret_val'] = '是否免運費格式錯誤!'

        if responseData['status'] == 0:
            if shipFreeQuota:
                if not(re.match('^\d+$', shipFreeQuota)):
                    responseData['status'] = -16
                    responseData['ret_val'] = '免運費訂單價格格式錯誤!'

        if responseData['status'] == 0:
            if fixShipFee:
                if not(re.match('^\d+$', fixShipFee)):
                    responseData['status'] = -17
                    responseData['ret_val'] = '運費訂價格式錯誤!'

        if responseData['status'] == 0:
            if fixShipFeeFr:
                if not(re.match('^\d+$', fixShipFeeFr)):
                    responseData['status'] = -18
                    responseData['ret_val'] = '訂單價格由格式錯誤!'

        if responseData['status'] == 0:
            if fixShipFeeTo:
                if not(re.match('^\d+$', fixShipFeeTo)):
                    responseData['status'] = -19
                    responseData['ret_val'] = '訂單價格至格式錯誤!'

        if responseData['status'] == 0:
            if shipByProduct:
                if not(re.match('^\w+$', shipByProduct)):
                    responseData['status'] = -20
                    responseData['ret_val'] = '運費由商品設定格式錯誤!'
        # 檢查同一人是否重複新增同名的商店
        if responseData['status'] == 0:
            try:
                shop = models.Shop.objects.get(shop_title=shopTitle)
                responseData['status'] = -21
                responseData['ret_val'] = '此商店名稱已存在，請選擇其他名稱!'
            except:
                pass
        # 新增商店並移動圖檔到指定路徑
        if responseData['status'] == 0:
            now = datetime.datetime.now()
            # shop_icon
            shopIconName = str(shopIcon.name).split('.')[0]
            shopIconExtension = str(shopIcon.name).split('.')[1]
            shopIconFullName = shopIconName + '_' + now.strftime('%Y%m%d%H%M%S') + '_' + str(round(now.timestamp())) + '.' + shopIconExtension
            # shop_pic
            shopPicName = str(shopPic.name).split('.')[0]
            shopPicExtension = str(shopPic.name).split('.')[1]
            shopPicFullName = shopPicName + '_' + now.strftime('%Y%m%d%H%M%S') + '_' + str(round(now.timestamp())) + '.' + shopPicExtension
            # 移動圖檔到指定路徑
            fs = FileSystemStorage(location='templates/static/images/')
            fs.save(name=shopIconFullName, content=shopIcon)
            fs.save(name=shopPicFullName, content=shopPic)
            # 新增商店
            models.Shop.objects.create(
                user_id=request.session['user']['id'], 
                shop_category_id=shopCategoryId, 
                shop_title=shopTitle, 
                shop_icon=shopIconFullName, 
                shop_pic=shopPicFullName, 
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
                fix_ship_fee_to=fixShipFeeTo
            )
            responseData['ret_val'] = '商店新增成功!'
    return JsonResponse(responseData)
# 更新商店
def update(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        shopIcon = request.FILES.get('shop_icon', '')
        shopTitle = request.POST.get('shop_title', '')
        shopCategoryId = request.POST.get('shop_category_id', 0)
        shopPic = request.FILES.get('shop_pic', '')
        shopDesc = request.POST.get('shop_desc', '')
        paypal = request.POST.get('paypal', '')
        visa = request.POST.get('visa', '')
        master = request.POST.get('master', '')
        apple = request.POST.get('apple', '')
        android = request.POST.get('android', '')
        isShipFree = request.POST.get('is_ship_free', '')
        shipFreeQuota = request.POST.get('ship_free_quota', 0)
        fixShipFee = request.POST.get('fix_ship_fee', 0)
        fixShipFeeFr = request.POST.get('fix_ship_fee_fr', 0)
        fixShipFeeTo = request.POST.get('fix_ship_fee_to', 0)
        shipByProduct = request.POST.get('ship_by_product', '')
        # 現在時間
        now = datetime.datetime.now()
        # FileSystemStorage
        fs = FileSystemStorage(location='templates/static/images/')
        # 檢查商店編號是否正確
        if responseData['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=id)
            except:
                responseData['status'] = -1
                responseData['ret_val'] = '找不到此商店編號的商店!'
        # 檢查使用者是否登入
        if responseData['status'] == 0:
            if not('user' in request.session):
                responseData['status'] = -2
                responseData['ret_val'] = '請先登入會員!'
        # 判斷必填欄位是否填寫及欄位格式是否正確
        if responseData['status'] == 0:
            if not(shopTitle):
                responseData['status'] = -3
                responseData['ret_val'] = '未填寫商店標題!'

        if responseData['status'] == 0:
            if not(shopCategoryId):
                responseData['status'] = -4
                responseData['ret_val'] = '未選擇商店類別!'

        if responseData['status'] == 0:
            if not(shopDesc):
                responseData['status'] = -5
                responseData['ret_val'] = '未填寫商店描述!'

        if responseData['status'] == 0:
            if not(re.match('^\d+$', shopCategoryId)):
                responseData['status'] = -6
                responseData['ret_val'] = '商店分類格式錯誤!'
        # 選填欄位若有填寫，則判斷其格式是否正確
        if responseData['status'] == 0:
            if shopIcon:
                if not(re.match('^\w+\.(gif|png|jpg|jpeg)$', str(shopIcon.name))):
                    responseData['status'] = -7
                    responseData['ret_val'] = '商店小圖格式錯誤!'
                else:
                    shopIconName = str(shopIcon.name).split('.')[0]
                    shopIconExtension = str(shopIcon.name).split('.')[1]
                    shopIconFullName = shopIconName + '_' + now.strftime('%Y%m%d%H%M%S') + '_' + str(round(now.timestamp())) + '.' + shopIconExtension
                    fs.save(name=shopIconFullName, content=shopIcon)
                    shop.shop_icon = shopIconFullName
                    shop.save()

        if responseData['status'] == 0:
            if shopPic:
                if not(re.match('^\w+\.(gif|png|jpg|jpeg)$', str(shopPic.name))):
                    responseData['status'] = -8
                    responseData['ret_val'] = '商店主圖格式錯誤!'
                else:
                    shopPicName = str(shopPic.name).split('.')[0]
                    shopPicExtension = str(shopPic.name).split('.')[1]
                    shopPicFullName = shopPicName + '_' + now.strftime('%Y%m%d%H%M%S') + '_' + str(round(now.timestamp())) + '.' + shopPicExtension
                    fs.save(name=shopPicFullName, content=shopPic)
                    shop.shop_pic = shopPicFullName
                    shop.save()

        if responseData['status'] == 0:
            if paypal:
                if not(re.match('^\w+$', paypal)):
                    responseData['status'] = -9
                    responseData['ret_val'] = 'PayPal 格式錯誤!'

        if responseData['status'] == 0:
            if visa:
                if not(re.match('^\w+$', visa)):
                    responseData['status'] = -10
                    responseData['ret_val'] = 'Visa 卡格式錯誤!'

        if responseData['status'] == 0:
            if master:
                if not(re.match('^\w+$', master)):
                    responseData['status'] = -11
                    responseData['ret_val'] = 'Master 卡格式錯誤!'

        if responseData['status'] == 0:
            if apple:
                if not(re.match('^\w+$', apple)):
                    responseData['status'] = -12
                    responseData['ret_val'] = 'Apple 格式錯誤!'

        if responseData['status'] == 0:
            if android:
                if not(re.match('^\w+$', android)):
                    responseData['status'] = -13
                    responseData['ret_val'] = 'Android 格式錯誤!'

        if responseData['status'] == 0:
            if isShipFree:
                if not(re.match('^\w+$', isShipFree)):
                    responseData['status'] = -14
                    responseData['ret_val'] = '是否免運費格式錯誤!'

        if responseData['status'] == 0:
            if shipFreeQuota:
                if not(re.match('^\d+$', shipFreeQuota)):
                    responseData['status'] = -15
                    responseData['ret_val'] = '免運費訂單價格格式錯誤!'

        if responseData['status'] == 0:
            if fixShipFee:
                if not(re.match('^\d+$', fixShipFee)):
                    responseData['status'] = -16
                    responseData['ret_val'] = '運費訂價格式錯誤!'

        if responseData['status'] == 0:
            if fixShipFeeFr:
                if not(re.match('^\d+$', fixShipFeeFr)):
                    responseData['status'] = -17
                    responseData['ret_val'] = '訂單價格由格式錯誤!'

        if responseData['status'] == 0:
            if fixShipFeeTo:
                if not(re.match('^\d+$', fixShipFeeTo)):
                    responseData['status'] = -18
                    responseData['ret_val'] = '訂單價格至格式錯誤!'

        if responseData['status'] == 0:
            if shipByProduct:
                if not(re.match('^\w+$', shipByProduct)):
                    responseData['status'] = -19
                    responseData['ret_val'] = '運費由商品設定格式錯誤!'
        # 先檢查使用者是否更改商店名稱，若有更改，則檢查是否更改名稱為其他同名的商店
        if responseData['status'] == 0:
            try:
                oldShop = models.Shop.objects.get(id=id, shop_title=shopTitle)
            except:
                sameNameShops = models.Shop.objects.filter(shop_title=shopTitle)
                if len(sameNameShops) > 0:
                    responseData['status'] = -20
                    responseData['ret_val'] = '此商店名稱已存在，請選擇其他名稱!'
        # 更新商店
        if responseData['status'] == 0:
            shop.shop_title = shopTitle
            shop.shop_category_id = shopCategoryId
            shop.shop_description = shopDesc
            shop.paypal = paypal
            shop.visa = visa
            shop.master = master
            shop.apple = apple
            shop.android = android
            shop.is_ship_free = isShipFree
            shop.ship_by_product = shipByProduct
            shop.ship_free_quota = shipFreeQuota
            shop.fix_ship_fee = fixShipFee
            shop.fix_ship_fee_from = fixShipFeeFr
            shop.fix_ship_fee_to = fixShipFeeTo
            shop.save()
            responseData['ret_val'] = '商店更新成功!'
    return JsonResponse(responseData)
# 單一商店
def show(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'shop': {}
    }

    if request.method == 'GET':
        # 檢查商店編號是否正確
        if responseData['status'] == 0:
            try:
                shop = models.Shop.objects.get(id=id)
                responseData['shop']['id'] = shop.id
                responseData['shop']['user_id'] = shop.user_id
                responseData['shop']['shop_category_id'] = shop.shop_category_id
                responseData['shop']['shop_title'] = shop.shop_title
                responseData['shop']['shop_icon'] = shop.shop_icon
                responseData['shop']['shop_pic'] = shop.shop_pic
                responseData['shop']['shop_description'] = shop.shop_description
                responseData['shop']['paypal'] = shop.paypal
                responseData['shop']['visa'] = shop.visa
                responseData['shop']['master'] = shop.master
                responseData['shop']['apple'] = shop.apple
                responseData['shop']['android'] = shop.android
                responseData['shop']['is_ship_free'] = shop.is_ship_free
                responseData['shop']['ship_by_product'] = shop.ship_by_product
                responseData['shop']['ship_free_quota'] = shop.ship_free_quota
                responseData['shop']['fix_ship_fee'] = shop.fix_ship_fee
                responseData['shop']['fix_ship_fee_from'] = shop.fix_ship_fee_from
                responseData['shop']['fix_ship_fee_to'] = shop.fix_ship_fee_to
                responseData['shop']['created_at'] = shop.created_at
                responseData['shop']['updated_at'] = shop.updated_at
                responseData['ret_val'] = '已找到商店資料!'
            except:
                responseData['status'] = -1
                responseData['ret_val'] = '找不到此商店編號的商店!'
    return JsonResponse(responseData)
