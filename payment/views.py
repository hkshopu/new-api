from django.http.response import JsonResponse
from django.shortcuts import render
from hkshopu import models

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