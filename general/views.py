from django.http.response import JsonResponse
from django.shortcuts import render
from hkshopu import models
from django.db.models import Q
from utils.gmail import gmail_authenticate
from utils.gmail import search_messages
from utils.gmail import read_message
import datetime
from django.db import transaction


# Create your views here.
def bankCode(request):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': []
    }
    
    if request.method == 'GET':
        keyword = request.GET.get('keyword', '')
        bank_list = models.Bank_Code.objects.filter(Q(bank_code__icontains=keyword) | Q(bank_name__icontains=keyword)).values('id', 'bank_code', 'bank_name', 'seq').order_by('seq')
        for row in bank_list:
            temp_obj = {}
            for attr in row:
                temp_obj[attr] = row[attr]
            responseData['data'].append(temp_obj)
    return JsonResponse(responseData)

def keywordSearchCount(request, keyword):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': {}    
    }

    if request.method == 'GET':
        search_count = len(models.Search_History.objects.filter(keyword=keyword))
        responseData['data']['search_count'], responseData['ret_val'] = search_count, '取得成功'
    return JsonResponse(responseData)

def searchGmail(request):
    responseData = {
        'status': 0,
        'ret_val': '',
        'data': []
    }
    if request.method == 'GET':
        #gmail = request.POST.get('gmail')
        #search = request.POST.get('search')
        # Inward+Payments+Notification&isrefinement=true&datestart=2021-07-12&dateend=2021-07-19&daterangetype=custom_range
        # Dates have to formatted in YYYY/MM/DD format for gmail
        #query = "before: {0} after: {1}".format(today.strftime('%Y/%m/%d'),yesterday.strftime('%Y/%m/%d'))
        delta=datetime.timedelta(days=1)
        before=datetime.date.today()+delta
        after=datetime.date.today()-delta
        search = 'subject:Inward+Payments+Notification before: {0} after: {1}'.format(before.strftime('%Y/%m/%d'),after.strftime('%Y/%m/%d'))
        #search = 'subject:Inward+Payments+Notification before: {0} after: {1}'.format('2021/07/17','2021/07/15')
        # get the Gmail API service
        service = gmail_authenticate()
        # get emails that match the query you specify
        results = search_messages(service, search)
        # for each email matched, read it (output plain/text to console & save HTML and attachments)
        for msg in results:
            responseData['data'].append(read_message(service, msg))
        try:
            with transaction.atomic():
                for mail in responseData['data']:
                    mail_date = datetime.datetime.strptime(mail['Date'], '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S')
                    account_nickname = mail['body']['parsed_html_data']['Account Nickname']
                    as_of = mail['body']['parsed_html_data']['As of']
                    credit_amount = mail['body']['parsed_html_data']['Credit Amount']
                    paying_bank = mail['body']['parsed_html_data']['Paying Bank']
                    reference_number = mail['body']['parsed_html_data']['Reference Number']
                    if not models.Fps_Email_Transaction.objects.filter(reference_number=reference_number).exists():
                        models.Fps_Email_Transaction.objects.create(
                            reference_number=reference_number,
                            account_nickname=account_nickname,
                            as_of=as_of,
                            credit_amount=credit_amount,
                            paying_bank=paying_bank,
                            mail_date=mail_date
                        )
        except:
            responseData['status'], responseData['ret_val'] = -1, 'This was not supposed to happen, please contact our engineer.'

    return JsonResponse(responseData)