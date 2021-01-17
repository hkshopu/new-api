from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
import mysql.connector
# Create your views here.

# 首頁
def index(request):
    template = get_template('index.html')
    html = template.render()
    return HttpResponse(html)