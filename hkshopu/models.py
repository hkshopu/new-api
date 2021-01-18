# _*_ encoding: utf-8 _*_
from django.db import models

# Create your models here.
class User(models.Model):
    account_name = models.CharField(max_length=50, null=True)
    google_account = models.CharField(max_length=50, null=True)
    facebook_account = models.CharField(max_length=50, null=True)
    apple_account = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=1, null=True)
    birthday = models.DateField(null=True)
    address = models.CharField(max_length=100, null=True)
    forget_password_token = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shop(models.Model):
    user_id = models.PositiveIntegerField()
    shop_category_id = models.PositiveIntegerField()
    shop_title = models.CharField(max_length=50)
    shop_icon = models.CharField(max_length=255)
    shop_pic = models.CharField(max_length=255)
    shop_description = models.TextField()
    paypal = models.CharField(max_length=50, null=True)
    visa = models.CharField(max_length=50, null=True)
    master = models.CharField(max_length=50, null=True)
    apple = models.CharField(max_length=50, null=True)
    android = models.CharField(max_length=50, null=True)
    is_ship_free = models.CharField(max_length=1, null=True, default='N')
    ship_by_product = models.CharField(max_length=1, null=True, default='N')
    ship_free_quota = models.PositiveIntegerField(null=True)
    fix_ship_fee = models.PositiveIntegerField(null=True)
    fix_ship_fee_from = models.PositiveIntegerField(null=True)
    fix_ship_fee_to = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shop_Category(models.Model):
    c_shop_category = models.CharField(max_length=50)
    e_shop_category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
