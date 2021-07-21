from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import paypalrestsdk


paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AdBCLHocOrbf94O5WAIkLVi3OAjuwWseJfwNtX6uHSm96tV5gqB_e1g4uBvfvS6TlQeAs9mjT90b-Ok3",
  "client_secret": "EFg3J2mb7i__gh7xOjd836JiS_WwXOb6No0mJiSc-bt_SyjIE0resRHWkHDYVuWdsNnWGJN7R3M7_7qX" })


# Create your views here.
def createPayment(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '',
        'data': {"approval_url": ""}
    }

    email = request.POST.get('email')

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "https://hkshopu.df.r.appspot.com/paypal/executePayment/",
            "cancel_url": "https://hkshopu.df.r.appspot.com/paypal/cancel/"},
        "transactions": [{
            "payee": {
                "email": email
            },
            "amount": {
                "total": "5.00",
                "currency": "HKD"},
            "description": "This is the payment transaction description."}]})
    if payment.create():
        print("Payment created successfully")
        for link in payment.links:
            if link.rel == "approval_url":
                # Convert to str to avoid Google App Engine Unicode issue
                # https://github.com/paypal/rest-api-sdk-python/pull/58
                approval_url = str(link.href)
                print("Redirect for approval: %s" % (approval_url))
                responseData['data']['approval_url'] = approval_url
        print(payment)
    else:
        print(payment.error)
        responseData['status'], responseData['ret_val'] = -2, payment.error

    return JsonResponse(responseData)

def executePayment(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '',
        'data': {}
    }
    paymentId = request.GET.get('paymentId')
    token = request.GET.get('token')
    PayerID = request.GET.get('PayerID')
    payment = paypalrestsdk.Payment.find(paymentId)

    if payment.execute({"payer_id": PayerID}):
        print("Payment execute successfully")
        print(payment)
    else:
        print(payment.error) # Error Hash
    return JsonResponse(responseData)

def getPaymentDetails(request):
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