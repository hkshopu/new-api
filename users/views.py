from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.contrib.auth.hashers import make_password
from passlib.handlers.django import django_pbkdf2_sha256
from django.core import mail
from django.utils.html import strip_tags
import mysql.connector
import re
import random

# Create your views here.

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
        # 判斷使用者是否使用相同電子郵件重複註冊
        if responseData['status'] == 0:
            conn = mysql.connector.connect(
                host='localhost', 
                user='root', 
                password='32753715', 
                database='store'
            )
            cursor = conn.cursor(buffered=True)
            cursor.execute('select * from `hkshopu_user` where `email` = %s or `phone` = %s limit 1', (email, phone))
            if cursor.rowcount > 0:
                responseData['status'] = -11
                responseData['ret_val'] = '該電子郵件或手機號碼已被使用!'

        if responseData['status'] == 0:
            cursor.execute('insert into `hkshopu_user` (`account_name`, `email`, `password`, `first_name`, `last_name`, `phone`, `gender`, `birthday`, `address`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (accountName, email, make_password(password), firstName, lastName, phone, gender, birthday, address))
            conn.commit()
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

        conn = mysql.connector.connect(
            host='localhost', 
            user='root', 
            password='32753715', 
            database='store'
        )
        cursor = conn.cursor(buffered=True)
        # 驗證使用者輸入的電子郵件與密碼是否正確
        if responseData['status'] == 0:
            if not(email) or not(password):
                responseData['status'] = -1
                responseData['ret_val'] = '電子郵件或密碼未填寫!'

        if responseData['status'] == 0:
            query = 'select * from `hkshopu_user` where `email` = %s limit 1'
            values = (email, )
            cursor.execute(query, values)
            if cursor.rowcount == 0:
                responseData['status'] = -2
                responseData['ret_val'] = '電子郵件錯誤!'

        if responseData['status'] == 0:
            userData = cursor.fetchone()
            if not(django_pbkdf2_sha256.verify(password, userData[6])):
                responseData['status'] = -3
                responseData['ret_val'] = '密碼錯誤!'

        if responseData['status'] == 0:
            request.session['user'] = {
                'id': userData[0], 
                'account_name': userData[1], 
                'email': userData[5], 
                'first_name': userData[7], 
                'last_name': userData[8]
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
        # 取得欄位資料
        email = request.POST.get('email', '')
        googleAccount = request.POST.get('google_account', '')
        facebookAccount = request.POST.get('facebook_account', '')
        appleAccount = request.POST.get('apple_account')
        conn = mysql.connector.connect(
            host='localhost', 
            user='root', 
            password='32753715', 
            database='store'
        )
        cursor = conn.cursor(buffered=True)

        if responseData['status'] == 0:
            if googleAccount and email:
                sqlQuery = 'select * from `hkshopu_user` where `email` = %s limit 1'
                values = (email, )
                cursor.execute(sqlQuery, values)
                if cursor.rowcount > 0:
                    sqlQuery = 'update `hkshopu_user` set `google_account` = %s where `email` = %s'
                    values = (googleAccount, email)
                    cursor.execute(sqlQuery, values)
                    conn.commit()
                    responseData['ret_val'] = '已使用 Google 帳戶登入!'
                    responseData['status'] = 1
                else:
                    sqlQuery = 'insert into `hkshopu_user` (`google_account`, `email`) values (%s, %s)'
                    values = (googleAccount, email)
                    cursor.execute(sqlQuery, values)
                    conn.commit()
                    responseData['ret_val'] = '已使用 Google 帳戶註冊!'
                    responseData['status'] = -1

        if responseData['status'] == 0:
            if facebookAccount and email:
                sqlQuery = 'select * from `hkshopu_user` where `email` = %s limit 1'
                values = (email, )
                cursor.execute(sqlQuery, values)
                if cursor.rowcount > 0:
                    sqlQuery = 'update `hkshopu_user` set `facebook` = %s where `email` = %s'
                    values = (facebookAccount, email)
                    cursor.execute(sqlQuery, values)
                    conn.commit()
                    responseData['ret_val'] = '已使用 Facebook 帳戶登入!'
                    responseData['status'] = 2
                else:
                    sqlQuery = 'insert into `hkshopu_user` (`facebook_account`, `email`) values (%s, %s)'
                    values = (facebookAccount, email)
                    cursor.execute(sqlQuery, values)
                    conn.commit()
                    responseData['ret_val'] = '已使用 Facebook 帳戶註冊!'
                    responseData['status'] = -2

        if responseData['status'] == 0:
            if appleAccount and email:
                sqlQuery = 'select * from `hkshopu_user` where `email` = %s limit 1'
                values = (email, )
                cursor.execute(sqlQuery, values)
                if cursor.rowcount > 0:
                    sqlQuery = 'update `hkshopu_user` set `apple` = %s where `email` = %s'
                    values = (appleAccount, email)
                    cursor.execute(sqlQuery, values)
                    conn.commit()
                    responseData['ret_val'] = '已使用 Apple 帳戶登入!'
                    responseData['status'] = 3
                else:
                    sqlQuery = 'insert into `hkshopu_user` (`apple_account`, `email`) values (%s, %s)'
                    values = (appleAccount, email)
                    cursor.execute(sqlQuery, values)
                    conn.commit()
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

        conn = mysql.connector.connect(
            host='localhost', 
            user='root', 
            password='32753715', 
            database='store'
        )
        cursor = conn.cursor(buffered=True)

        if responseData['status'] == 0:
            if not(email):
                responseData['status'] = -1
                responseData['ret_val'] = '電子郵件未填寫!'

        if responseData['status'] == 0:
            query = 'select * from `hkshopu_user` where `email` = %s limit 1'
            values = (email, )
            cursor.execute(query, values)
            if cursor.rowcount == 0:
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
                salt = ''.join(randStrList)
                # 確認資料表中沒有重複的 Token
                query = 'select * from `hkshopu_user` where `forget_password_token` = %s limit 1'
                values = (salt, )
                cursor.execute(query, values)
                i = cursor.rowcount
            # 更新使用者資料表的 Token
            query = 'update `hkshopu_user` set `forget_password_token` = %s where `email` = %s'
            values = (salt, email)
            cursor.execute(query, values)
            conn.commit()
            # 發送忘記密碼通知信
            query = 'select * from `hkshopu_user` where `email` = %s limit 1'
            values = (email, )
            cursor.execute(query, values)
            userData = cursor.fetchone()
            subject = 'HKShopU - 忘記密碼'
            htmlMessage = render_to_string('forget_password_mail.html', {'id': userData[0], 'account_name': userData[1], 'token': salt})
            message = strip_tags(htmlMessage)
            fromEmail = 'HKShopU'
            toEmail = [email, ]
            mail.send_mail(subject=subject, message=message, from_email=fromEmail, recipient_list=toEmail, html_message=htmlMessage)
            responseData['ret_val'] = '已發送重設密碼連結至您的電子郵件!'
    return JsonResponse(responseData)