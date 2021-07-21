from django.http.response import JsonResponse
from django.shortcuts import render
from hkshopu import models
from datetime import datetime
from django.db.models import Sum
from django.db import transaction
import uuid
import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import paypalrestsdk

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AdBCLHocOrbf94O5WAIkLVi3OAjuwWseJfwNtX6uHSm96tV5gqB_e1g4uBvfvS6TlQeAs9mjT90b-Ok3",
  "client_secret": "EFg3J2mb7i__gh7xOjd836JiS_WwXOb6No0mJiSc-bt_SyjIE0resRHWkHDYVuWdsNnWGJN7R3M7_7qX" })

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
    print('--------------------------------------------------')
    #print(request.body)
    f = open("paypalWebHooks.txt", "a")
    data = json.loads(request.body)
    print(data['event_type']+'\n')
    f.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+'\n')
    f.write('ID: '+data['id']+'\n')
    f.write('event_type: '+ data['event_type']+'\n')
    f.write('summary: '+data['summary']+'\n')
    f.write(json.dumps(data))
    f.write('\n--------------------------------------------------\n\n')
    f.close()
    print('--------------------------------------------------')

    return JsonResponse(responseData)
def paypalWebHooks_COC(request):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': {}
    }
    print('--------------------------------------------------')
    print('CHECKOUT.ORDER.COMPLETED\n')
    #print(request.body)
    f = open("paypalWebHooks_COC.txt", "a")
    f.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+'\n')
    f.write(json.dumps(json.loads(request.body)))
    f.write('\n--------------------------------------------------\n\n')
    f.close()
    print('--------------------------------------------------')

    return JsonResponse(responseData)
def paypalWebHooks_COA(request):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': {}
    }
    print('--------------------------------------------------')
    print('CHECKOUT.ORDER.APPROVED\n')
    f = open("paypalWebHooks_COA.txt", "a")
    f.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+'\n')
    f.write(json.dumps(json.loads(request.body)))
    f.write('\n--------------------------------------------------\n\n')
    f.close()
    print('--------------------------------------------------')

    return JsonResponse(responseData)
def paypalWebHooks_PSC(request):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': {}
    }
    print('--------------------------------------------------')
    print('PAYMENT.SALE.COMPLETED\n')
    f = open("paypalWebHooks_PSC.txt", "a")
    f.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+'\n')
    f.write(json.dumps(json.loads(request.body)))
    f.write('\n--------------------------------------------------\n\n')
    f.close()
    print('--------------------------------------------------')

    return JsonResponse(responseData)
def paypalWebHooks_POC(request):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': {}
    }
    print('--------------------------------------------------')
    print('PAYMENT.ORDER.CANCELLED\n')
    f = open("paypalWebHooks_POC.txt", "a")
    f.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+'\n')
    f.write(json.dumps(json.loads(request.body)))
    f.write('\n--------------------------------------------------\n\n')
    f.close()
    print('--------------------------------------------------')

    return JsonResponse(responseData)

# CHECKOUT.ORDER.COMPLETED
# CHECKOUT.ORDER.APPROVED
# PAYMENT.SALE.COMPLETED
# PAYMENT.ORDER.CANCELLED

def paypal_createPayment(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '',
        'data': {"approval_url": ""}
    }
    
    hkshopu_order_number = request.POST.get('hkshopu_order_number')
    email = request.POST.get('payee_email')

    try:
        shop_order = models.Shop_Order.objects.get(order_number=hkshopu_order_number)
        if shop_order.status != 'Pending Payment':
            responseData['status'], responseData['ret_val'] = -2, '訂單已付款'  
    except:
        responseData['status'], responseData['ret_val'] = -1, '無此訂單編號'

    if responseData['status'] == 0:
        shop_order_details = models.Shop_Order_Details.objects.filter(shop_order_id=shop_order.id)
        total_amount = 0
        for detail in shop_order_details:
            total_amount += detail.unit_price*detail.quantity + detail.logistic_fee
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                # "return_url": "https://hkshopu.df.r.appspot.com/paypal/executePayment/",
                # "cancel_url": "https://hkshopu.df.r.appspot.com/paypal/cancelPayment/"},                
                "return_url": "http://localhost:8000/payment/paypal/executePayment/",
                "cancel_url": "http://localhost:8000/payment/paypal/cancelPayment/"},
            "transactions": [{
                "payee": {
                    "email": email
                },
                "amount": {
                    "total": str(total_amount),
                    "currency": "HKD"},
                "description": "HKShopU Paypal Payment."}]})
        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    # Convert to str to avoid Google App Engine Unicode issue
                    # https://github.com/paypal/rest-api-sdk-python/pull/58
                    approval_url = str(link.href)
                    #print("Redirect for approval: %s" % (approval_url))
                    responseData['data']['approval_url'] = approval_url
            paypal_payment_id = payment.id
            
            hkshopu_paypal_transaction = models.Paypal_Transactions.objects.filter(order_number=hkshopu_order_number)
            if len(hkshopu_paypal_transaction) == 1:
                hkshopu_paypal_transaction.update(paypal_transaction_id=paypal_payment_id)
            elif len(hkshopu_paypal_transaction) == 0:
                models.Paypal_Transactions.objects.create(
                    id=uuid.uuid4(),
                    order_number=hkshopu_order_number,
                    paypal_transaction_id=paypal_payment_id,
                )
        else:
            responseData['status'], responseData['ret_val'] = -2, payment.error

    return JsonResponse(responseData)

def paypal_executePayment(request):
    paymentId = request.GET.get('paymentId')
    token = request.GET.get('token')
    PayerID = request.GET.get('PayerID')
    payment = paypalrestsdk.Payment.find(paymentId)
    if payment.execute({"payer_id": PayerID}):
        payment = paypalrestsdk.Payment.find(paymentId)
        hkshopu_paypal_transaction = models.Paypal_Transactions.objects.filter(paypal_transaction_id=paymentId)
        paypal_sale_state = payment['transactions'][0]['related_resources'][0]['sale']['state']
        if len(hkshopu_paypal_transaction) == 1 and paypal_sale_state == 'completed':
            transaction_amount = payment['transactions'][0]['amount']['total']
            transaction_currency_code = payment['transactions'][0]['amount']['currency']
            fee_amount = payment['transactions'][0]['related_resources'][0]['sale']['transaction_fee']['value']
            fee_currency_code = payment['transactions'][0]['related_resources'][0]['sale']['transaction_fee']['currency']
            with transaction.atomic():
                hkshopu_paypal_transaction.update(
                    paypal_payer_id=PayerID,
                    transaction_amount=transaction_amount,
                    transaction_currency_code=transaction_currency_code,
                    fee_amount=fee_amount,
                    fee_currency_code=fee_currency_code
                )
                models.Shop_Order.objects.filter(order_number=hkshopu_paypal_transaction[0].order_number).update(
                    status='Pending Delivery'
                )
        return HttpResponse("Paypal payment execute successfully")
    else:
        #print(payment.error) # Error Hash
        return JsonResponse(payment.error)

def paypal_cancelPayment(request):
    return HttpResponse("PayPal payment has been cancelled")

def paypal_getPaymentDetails(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '',
        'data': {}
    }
    # Fetch Payment
    id = request.POST.get('id')
    payment = paypalrestsdk.Payment.find(id)
    responseData['data'] = payment.to_dict()

    # Get List of Payments
    # payment_history = paypalrestsdk.Payment.all({"count": 10})
    # print(payment_history.payments)
    
    return JsonResponse(responseData)