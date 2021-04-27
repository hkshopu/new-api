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
    birthday = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True)
    street_name = models.CharField(max_length=50, null=True)
    street_no = models.CharField(max_length=50, null=True)
    floor = models.CharField(max_length=50, null=True)
    room = models.CharField(max_length=50)
    forget_password_token = models.CharField(max_length=20, null=True)
    activated = models.CharField(max_length=1, default='N')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shop(models.Model):
    user_id = models.PositiveIntegerField()
    shop_title = models.CharField(max_length=50)
    shop_icon = models.CharField(max_length=255)
    shop_pic = models.CharField(max_length=255, null=True)
    shop_description = models.TextField(null=True)
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
    discount_by_percent = models.PositiveIntegerField(null=True)
    discount_by_amount = models.PositiveIntegerField(null=True)
    transaction_method = models.CharField(max_length=50, null=True)
    transport_setting = models.CharField(max_length=50, null=True)
    bank_code = models.CharField(max_length=50, null=True)
    bank_name = models.CharField(max_length=50, null=True)
    bank_account = models.CharField(max_length=50, null=True)
    bank_account_name = models.CharField(max_length=50, null=True)
    address_name = models.CharField(max_length=50, null=True)
    address_country_code = models.CharField(max_length=50, null=True)
    address_phone = models.CharField(max_length=50, null=True)
    address_is_phone_show= models.CharField(max_length=1, null=True, default='Y')
    address_area = models.CharField(max_length=50, null=True)
    address_district = models.CharField(max_length=50, null=True)
    address_road = models.CharField(max_length=50, null=True)
    address_number = models.CharField(max_length=50, null=True)
    address_other = models.CharField(max_length=50, null=True)
    address_floor = models.CharField(max_length=50, null=True)
    address_room = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shop_Category(models.Model):
    c_shop_category = models.CharField(max_length=50)
    e_shop_category = models.CharField(max_length=50)
    unselected_shop_category_icon = models.CharField(max_length=255)
    selected_shop_category_icon = models.CharField(max_length=255)
    shop_category_background_color = models.CharField(max_length=6)
    shop_category_seq = models.PositiveIntegerField()
    is_delete = models.CharField(max_length=1, default='N')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shop_Sub_Category(models.Model):
    shop_category_id = models.PositiveIntegerField()
    c_shop_sub_category = models.CharField(max_length=50)
    e_shop_sub_category = models.CharField(max_length=50)
    unselected_shop_sub_category_icon = models.CharField(max_length=255)
    selected_shop_sub_category_icon = models.CharField(max_length=255)
    shop_sub_category_seq = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Selected_Shop_Category(models.Model):
    shop_id = models.PositiveIntegerField()
    shop_category_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shop_Shipment_Setting(models.Model):
    shop_id = models.PositiveIntegerField()
    shipment_desc = models.CharField(max_length=255)
    onoff = models.CharField(max_length=50)

class Shipment_default_method(models.Model):
    shipment_default_desc = models.CharField(max_length=255)
    onoff = models.CharField(max_length=50)

class Product(models.Model):
    shop_id = models.PositiveIntegerField()
    product_category_id = models.PositiveIntegerField()
    product_sub_category_id = models.PositiveIntegerField()
    product_title = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    product_description = models.TextField()
    # product_country_code = models.CharField(max_length=5)
    product_price = models.PositiveIntegerField()
    shipping_fee = models.PositiveIntegerField(null=True)
    weight = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    new_secondhand= models.CharField(max_length=50)
    longterm_stock_up= models.CharField(max_length=1)
    user_id=models.PositiveIntegerField()
    length = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    like = models.PositiveIntegerField()
    seen = models.PositiveIntegerField()
    sold_quantity = models.PositiveIntegerField()

class Product_Category(models.Model):
    c_product_category = models.CharField(max_length=50)
    e_product_category = models.CharField(max_length=50)
    unselected_product_category_icon = models.CharField(max_length=255)
    selected_product_category_icon = models.CharField(max_length=255)
    product_category_background_color = models.CharField(max_length=6)
    product_category_seq = models.IntegerField()
    is_delete = models.CharField(max_length=1, default='N')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Sub_Category(models.Model):
    product_category_id = models.PositiveIntegerField()
    c_product_sub_category = models.CharField(max_length=50)
    e_product_sub_category = models.CharField(max_length=50)
    unselected_product_sub_category_icon = models.CharField(max_length=255)
    selected_product_sub_category_icon = models.CharField(max_length=255)
    product_sub_category_background_color = models.CharField(max_length=6)
    product_sub_category_seq = models.IntegerField()
    is_delete = models.CharField(max_length=1, default='N')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Color(models.Model):
    c_product_color = models.CharField(max_length=50)
    e_product_color = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Selected_Product_Color(models.Model):
    product_id = models.PositiveIntegerField()
    color_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Size(models.Model):
    c_product_size = models.CharField(max_length=50)
    e_product_size = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Selected_Product_Size(models.Model):
    product_id = models.PositiveIntegerField()
    size_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Origin(models.Model):
    c_product_origin = models.CharField(max_length=50)
    e_product_origin = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Selected_Product_Pic(models.Model):
    product_id = models.PositiveIntegerField()
    product_pic = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover= models.CharField(max_length=2)

class Email_Validation(models.Model):
    user_id = models.PositiveIntegerField()
    email = models.CharField(max_length=50)
    validation_code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Audit_Log(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    action = models.CharField(max_length=100)
    parameter_in = models.TextField()
    parameter_out = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shop_Score(models.Model):
    user_id = models.PositiveIntegerField()
    shop_id = models.PositiveIntegerField()
    # from shop table
    score = models.FloatField() #or models.FloatField(**options)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Spec(models.Model):
    product_id = models.PositiveIntegerField()
    spec_desc_1 = models.CharField(max_length=255)
    spec_desc_2 = models.CharField(max_length=255)
    spec_dec_1_items= models.CharField(max_length=255)
    spec_dec_2_items= models.CharField(max_length=255)
    price=models.PositiveIntegerField()
    quantity= models.PositiveIntegerField()

class Product_Shipment_Method(models.Model):
    product_id = models.PositiveIntegerField()
    shipment_desc = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    onoff = models.CharField(max_length=50)
    shop_id=models.PositiveIntegerField()