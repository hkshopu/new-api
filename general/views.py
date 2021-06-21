from django.http.response import JsonResponse
from django.shortcuts import render
from hkshopu import models
from django.db.models import Q

# Create your views here.
def bankCode(request):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': {'bank_list':[]}
    }
    
    if request.method == 'GET':
        keyword = request.GET.get('keyword', '')
        bank_list = models.Bank_Code.objects.filter(Q(bank_code__icontains=keyword) | Q(bank_name__icontains=keyword)).values('id', 'bank_code', 'bank_name', 'seq').order_by('-seq')
        for row in bank_list:
            temp_obj = {}
            for attr in row:
                temp_obj[attr] = row[attr]
            responseData['data']['bank_list'].append(temp_obj)
    return JsonResponse(responseData)