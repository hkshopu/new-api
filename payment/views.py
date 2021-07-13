from django.http.response import JsonResponse
from django.shortcuts import render
from hkshopu import models
from datetime import datetime
from django.db import transaction
import uuid

# Create your views here.

def method(request):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': []
    }
    if request.method == 'GET':
        method_attr = [
            'id',
            'payment_desc'
        ]
        payment_method = models.Payment_Method.objects.all().order_by('-is_default')
        for method in payment_method:
            temp_data = {}
            for attr in method_attr:
                if hasattr(method, attr):
                    temp_data[attr] = getattr(method, attr)
            responseData['data'].append(temp_data)
    return JsonResponse(responseData)

def confirmFPSOrderTransaction(request):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': []
    }

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        user_payment_account_id = request.POST.get('user_payment_account_id')
        target_delivery_date = request.POST.get('target_delivery_date')
        target_delivery_time = request.POST.get('target_delivery_time')

        try:
            models.Shop_Order.objects.get(id=order_id)
        except:
            responseData['status'], responseData['ret_val'] = -1, '無此order_id'
        if responseData['status']==0:
            try:
                models.User_Payment_Account.objects.get(id=user_payment_account_id)
            except:
                responseData['status'], responseData['ret_val'] = -2, '無此user_payment_account_id'
        if responseData['status']==0:
            try:
                datetime.strptime(target_delivery_date, '%Y-%m-%d')
            except:
                responseData['status'], responseData['ret_val'] = -3, 'target_delivery_date應為 %Y-%m-%d'
        if responseData['status']==0:
            try:
                datetime.strptime(target_delivery_time, '%H-%M-%S')
            except:
                responseData['status'], responseData['ret_val'] = -4, 'target_delivery_time應為 %H-%M-%S'

        
        if responseData['status']==0:
            with transaction.atomic():
                models.FPS_Order_Transaction.objects.create(
                    id=uuid.uuid4(),
                    order_id=order_id,
                    user_payment_account_id=user_payment_account_id,
                    target_delivery_date=target_delivery_date,
                    target_delivery_time=target_delivery_time
                )
                models.Shop_Order.objects.filter(id=order_id).update(status='Pending Delivery')
            responseData['ret_val'] = '確認成功'
    return JsonResponse(responseData)

def paymentProcess(request):    
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': {}
    }

    if request.method == 'POST':

        hkshopu_order_number = request.POST.get('hkshopu_order_number')
        paypal_payer_id = request.POST.get('paypal_payer_id')
        paypal_transaction_id = request.POST.get('paypal_transaction_id')

        if hkshopu_order_number and paypal_payer_id and paypal_transaction_id:
            try:
                models.Shop_Order.objects.get(order_number=hkshopu_order_number)
            except:
                responseData['status'], responseData['ret_val'] = -1, 'order_number不存在'
            
            paypal_transaction = models.Paypal_Transactions.objects.create(
                id=uuid.uuid4(),
                order_number=hkshopu_order_number,
                paypal_transaction_id=paypal_transaction_id,
                paypal_payer_id=paypal_payer_id
            )
            responseData['ret_val'], responseData['data']['id'] = '成功', paypal_transaction.id

    return JsonResponse(responseData)

def paypalWebHooks(request):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': {}
    }

    if request.method == 'GET':
        pass

    return JsonResponse(responseData)

def createOrder(request):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': {}
    }

    

    return JsonResponse(responseData)

