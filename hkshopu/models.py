# _*_ encoding: utf-8 _*_
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import models
import re

from django.db.models.fields import FloatField

# validator
def validate_empty_value_to_default(value):
    if value == '':
        return None
# Create your models here.
class User(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
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
    pic=models.CharField(max_length=255)
    
class Shop(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.CharField(max_length=36)
    shop_title = models.CharField(max_length=50)
    shop_icon = models.CharField(max_length=255)
    shop_pic = models.CharField(max_length=255)
    shop_description = models.TextField()
    paypal = models.CharField(max_length=50)
    visa = models.CharField(max_length=50)
    master = models.CharField(max_length=50)
    apple = models.CharField(max_length=50)
    android = models.CharField(max_length=50)
    is_ship_free = models.CharField(max_length=1, null=True, default = 'Y')
    ship_by_product = models.CharField(max_length=1, null=True, default = 'Y')
    ship_free_quota = models.PositiveIntegerField(null=True)
    fix_ship_fee = models.PositiveIntegerField(null=True)
    fix_ship_fee_from = models.PositiveIntegerField(null=True)
    fix_ship_fee_to = models.PositiveIntegerField(null=True)
    discount_by_percent = models.PositiveIntegerField(null=True)
    discount_by_amount = models.PositiveIntegerField(null=True)
    transaction_method = models.CharField(max_length=50)
    transport_setting = models.CharField(max_length=50)
    bank_code = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=50)
    bank_account = models.CharField(max_length=50)
    bank_account_name = models.CharField(max_length=50)
    address_name = models.CharField(max_length=50)
    address_country_code = models.CharField(max_length=50)
    address_phone = models.CharField(max_length=50)
    address_is_phone_show= models.CharField(max_length=1, null=True, default='Y')
    address_area = models.CharField(max_length=50)
    address_district = models.CharField(max_length=50)
    address_road = models.CharField(max_length=50)
    address_number = models.CharField(max_length=50)
    address_other = models.CharField(max_length=50)
    address_floor = models.CharField(max_length=50)
    address_room = models.CharField(max_length=50)
    shop_name_updated_at = models.DateTimeField(auto_now=True, null=True)
    background_pic = models.CharField(max_length=255, null=True)
    shop_email = models.CharField(max_length=50, null=True)
    email_on = models.CharField(max_length=1, null=True)
    long_description = models.TextField(null=True)
    facebook_on = models.CharField(max_length=1, null=True)
    instagram_on = models.CharField(max_length=1, null=True)
    marketing_notification = models.CharField(max_length=1, null=True, default='Y')
    follower_notification = models.CharField(max_length=1, null=True, default='Y')
    rating_notification = models.CharField(max_length=1, null=True, default='Y')
    system_upgrade_notification = models.CharField(max_length=1, null=True, default='Y')
    hkshopu_event_notification = models.CharField(max_length=1, null=True, default='Y')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.CharField(max_length=1, default='N')      
    def validate_column(column_name, err_code, param):
        ret_code = 0
        ret_description = ''
        if column_name=='user_id':
            if not(param):
                ret_code, ret_description = err_code, '請先登入會員!'
        elif column_name=='shop_title':
            if not(param):
                ret_code, ret_description = err_code, '未填寫商店標題!'
            elif len(param)>50:
                ret_code, ret_description = err_code, '商店標題過長'
        elif column_name=='shop_icon':
            if not(param):
                ret_code, ret_description = err_code, '未上傳商店小圖!'
            elif not(re.match('^.+\.(gif|png|jpg|jpeg)$', str(param.name))):
                ret_code, ret_description = err_code, '商店小圖格式錯誤!'
        elif column_name=='shop_pic':
            if param:
                if not(re.match('^.+\.(gif|png|jpg|jpeg)$', str(param.name))):
                    ret_code, ret_description = err_code, '商店主圖格式錯誤!'
        elif column_name=='shop_description':
            pass
        elif column_name=='paypal':
            if param:
                if not(re.match('^\w+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, 'PayPal 格式錯誤!'
        elif column_name=='visa':
            if param:
                if not(re.match('^\w+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, 'Visa 格式錯誤!'
        elif column_name=='master':
            if param:
                if not(re.match('^\w+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, 'Master 格式錯誤!'
        elif column_name=='apple':
            if param:
                if not(re.match('^\w+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, 'Apple 格式錯誤!'
        elif column_name=='android':
            if param:
                if not(re.match('^\w+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, 'Android 格式錯誤!'
        elif column_name=='is_ship_free':
            if param:
                if not(re.match('^\w+$', param)) or len(param)>1:
                    ret_code, ret_description = err_code, '是否免運費格式錯誤!'
        elif column_name=='ship_by_product':
            if param:
                if not(re.match('^\w+$', param)) or len(param)>1:
                    ret_code, ret_description = err_code, '運費由商品設定格式錯誤!'
        elif column_name=='ship_free_quota':
            if param:
                if not(re.match('^\d+$', param)):
                    ret_code, ret_description = err_code, '免運費訂單價格格式錯誤!'
        elif column_name=='fix_ship_fee':
            if param:
                if not(re.match('^\d+$', param)):
                    ret_code, ret_description = err_code, '運費訂價格式錯誤!'
        elif column_name=='fix_ship_fee_from':
            if param:
                if not(re.match('^\d+$', param)):
                    ret_code, ret_description = err_code, '訂單價格由格式錯誤!'
        elif column_name=='fix_ship_fee_to':
            if param:
                if not(re.match('^\d+$', param)):
                    ret_code, ret_description = err_code, '訂單價格至格式錯誤!'
        elif column_name=='discount_by_percent':
            if param:
                if not(re.match('^\d+$', param)):
                    ret_code, ret_description = err_code, '價格折扣格式錯誤!'
        elif column_name=='discount_by_amount':
            if param:
                if not(re.match('^\d+$', param)):
                    ret_code, ret_description = err_code, '百分比折扣格式錯誤!'
        
        return ret_code, ret_description

class Shop_Clicked(models.Model):
    id = models.TextField(primary_key=True, max_length=36)
    shop_id = models.CharField(max_length=36)
    user_id = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shop_Category(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    c_shop_category = models.CharField(max_length=50)
    e_shop_category = models.CharField(max_length=50)
    unselected_shop_category_icon = models.CharField(max_length=255)
    selected_shop_category_icon = models.CharField(max_length=255)
    shop_category_background_color = models.CharField(max_length=6)
    shop_category_seq = models.PositiveIntegerField()
    is_delete = models.CharField(max_length=1, default='N')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def validate_column(column_name, err_code, param):
        ret_code = 0
        ret_description = ''
        if column_name=='user_id':
            if not(param):
                ret_code, ret_description = err_code, '請先登入會員!'
        elif column_name=='shop_title':
            if not(param):
                ret_code, ret_description = err_code, '未填寫商店標題!'
        elif column_name=='shop_icon':
            if not(param):
                ret_code, ret_description = err_code, '未上傳商店小圖!'
            elif not(re.match('^.+\.(gif|png|jpg|jpeg)$', str(param.name))):
                ret_code, ret_description = err_code, '商店小圖格式錯誤!'
        elif column_name=='shop_pic':
            if param:
                if not(re.match('^.+\.(gif|png|jpg|jpeg)$', str(param.name))):
                    ret_code, ret_description = err_code, '商店主圖格式錯誤!'
        elif column_name=='shop_description':
            pass
        elif column_name=='paypal':
            if param:
                if not(re.match('^\w+$', param)):
                    ret_code, ret_description = err_code, 'PayPal 格式錯誤!'
        elif column_name=='visa':
            if param:
                if not(re.match('^\w+$', param)):
                    ret_code, ret_description = err_code, 'Visa 格式錯誤!'
        elif column_name=='master':
            if param:
                if not(re.match('^\w+$', param)):
                    ret_code, ret_description = err_code, 'Master 格式錯誤!'
        elif column_name=='apple':
            if param:
                if not(re.match('^\w+$', param)):
                    ret_code, ret_description = err_code, 'Apple 格式錯誤!'
        elif column_name=='android':
            if param:
                if not(re.match('^\w+$', param)):
                    ret_code, ret_description = err_code, 'Android 格式錯誤!'
        elif column_name=='is_ship_free':
            if param:
                if not(re.match('^\w+$', param)):
                    ret_code, ret_description = err_code, '是否免運費格式錯誤!'
        elif column_name=='ship_by_product':
            if param:
                if not(re.match('^\w+$', param)):
                    ret_code, ret_description = err_code, '運費由商品設定格式錯誤!'
        elif column_name=='ship_free_quota':
            if param:
                if not(re.match('^\d+$', param)):
                    ret_code, ret_description = err_code, '免運費訂單價格格式錯誤!'
        elif column_name=='fix_ship_fee':
            if param:
                if not(re.match('^\d+$', param)):
                    ret_code, ret_description = err_code, '運費訂價格式錯誤!'
        elif column_name=='fix_ship_fee_from':
            if param:
                if not(re.match('^\d+$', param)):
                    ret_code, ret_description = err_code, '訂單價格由格式錯誤!'
        elif column_name=='fix_ship_fee_to':
            if param:
                if not(re.match('^\d+$', param)):
                    ret_code, ret_description = err_code, '訂單價格至格式錯誤!'
        elif column_name=='discount_by_percent':
            if param:
                if not(re.match('^\d+$', param)):
                    ret_code, ret_description = err_code, '價格折扣格式錯誤!'
        elif column_name=='discount_by_amount':
            if param:
                if not(re.match('^\d+$', param)):
                    ret_code, ret_description = err_code, '百分比折扣格式錯誤!'
        
        return param,ret_code, ret_description

class Shop_Sub_Category(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    shop_category_id = models.CharField(max_length=36)
    c_shop_sub_category = models.CharField(max_length=50)
    e_shop_sub_category = models.CharField(max_length=50)
    unselected_shop_sub_category_icon = models.CharField(max_length=255)
    selected_shop_sub_category_icon = models.CharField(max_length=255)
    shop_sub_category_seq = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Selected_Shop_Category(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    shop_id = models.CharField(max_length=36)
    shop_category_id = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def validate_column(column_name, err_code, param):
        ret_code = 0
        ret_description = ''
        if column_name == 'shop_id':
            try:
                Shop.objects.get(id=param,is_delete='N')
            except:
                ret_code, ret_description = err_code, '商店編號不存在'
        elif column_name == 'shop_category_id':
            if not(param):
                ret_code, ret_description = err_code, '未填寫商店分類編號!'
            else:
                for value in param:
                    try:
                        Shop_Category.objects.get(id=value)
                    except:
                        ret_code, ret_description = err_code, '商店分類格式錯誤!'
                        break
        elif column_name == 'shop_category_id_json':
            if not(param):
                ret_code, ret_description = err_code, '未填寫商店分類編號!'
            else:
                try:
                    json
                except:
                    import json
                try:
                    json_list = json.loads(param)
                    for item in json_list:
                        try:
                            Shop_Category.objects.get(id=item)
                        except:
                            ret_code, ret_description = err_code, '商店分類編號不存在!'
                            break
                except:
                    ret_code, ret_description = err_code, '商店分類格式錯誤!'



            
        return ret_code, ret_description

class Shop_Shipment_Setting(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    shop_id = models.CharField(max_length=36)
    shipment_desc = models.CharField(max_length=255)
    onoff = models.CharField(max_length=50)
    def validate_column(column_name, err_code, param):
        ret_code = 0
        ret_description = ''
        if column_name == 'shop_id':
            try:
                Shop.objects.get(id=param,is_delete='N')
            except:
                ret_code, ret_description = err_code, '無此商店'
        if column_name == 'shipment_settings':
            try:
                json
            except:
                import json
            try:
                shipment_settings = json.loads(param)
                for setting in shipment_settings:
                    shipmentDesc = setting['shipment_desc']
                    if len(shipmentDesc)>255:
                        ret_code, ret_description = err_code, '運輸設定格式錯誤!'
                        break
                    onOff = setting['onoff']
            except:
                ret_code, ret_description = err_code, '運輸設定格式錯誤!'
        return ret_code, ret_description
                    

class Shop_Address(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    shop_id = models.CharField(max_length=36)
    name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    is_phone_show = models.CharField(max_length=50, null=True, validators = [validate_empty_value_to_default], default = 'N')
    area = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    road = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    other = models.CharField(max_length=50)
    floor = models.CharField(max_length=50)
    room = models.CharField(max_length=50)
    is_address_show=models.CharField(max_length=1, null=True, default = 'Y')
    is_default=models.CharField(max_length=1, null=True, default = 'Y')
    def validate_column(column_name, err_code, param):
        ret_code = 0
        ret_description = ''
        if param == 'shop_id':
            try:
                Shop.objects.get(id=id,is_delete='N')
            except:
                ret_code, ret_description = err_code, '找不到此商店編號的商店!'                
        elif param == 'name':
            if param:
                if not(re.match('^[!@.#$%)(^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '姓名/公司名稱格式錯誤!'
        elif param == 'country_code':
            if param:
                if not(re.match('^[\+\d]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '國碼格式錯誤!'
        elif param == 'phone':
            if param:
                if not(re.match('^\d+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '電話號碼格式錯誤!'
        elif param == 'is_phone_show':
            if param:
                if not(re.match('^\w+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '顯示在店鋪簡介格式錯誤!'
        elif param == 'area':
            if param:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '地域格式錯誤!'
        elif param == 'district':
            if param:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '地區格式錯誤!'
        elif param == 'road':
            if param:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '街道名稱格式錯誤!'
        elif param == 'number':
            if param:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '街道門牌格式錯誤!'
        elif param == 'other':
            if param:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '其他地址格式錯誤!'
        elif param == 'floor':
            if param:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '樓層格式錯誤!'
        elif param == 'room':
            if param:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '房(室)名稱格式錯誤!'
        return  ret_code, ret_description

class Shop_Advertisement(models.Model):
    shop_id = models.CharField(max_length=36)
    pic_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shop_Bank_Account(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    shop_id = models.CharField(max_length=36)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    account = models.CharField(max_length=50)
    account_name = models.CharField(max_length=50)
    is_default = models.CharField(max_length=1, default='Y')
    def validate_column(column_name, err_code, param):
        ret_code = 0
        ret_description = ''
        if param is 'shop_id':
            try:
                Shop.objects.get(id=param,is_delete='N')
            except:
                ret_code, ret_description = err_code, '找不到此商店編號的商店!'
        elif param is 'bank_account_settings':
            try:
                json
            except:
                import json
            try:
                bank_account_settings = json.loads(param)
                for setting in bank_account_settings:
                    if hasattr(setting, 'id') and setting['id'] is not '':
                        pass
                    else:
                        param = setting['code']
                        param = setting['name']
                        param = setting['account']
                        param = setting['account_name']
            except:
                ret_code, ret_description = err_code, '商店銀行設定格式錯誤!'
        elif param == 'code':
            if not(re.match('^\d{1,50}$', param)):
                ret_code, ret_description = err_code, '銀行代碼格式錯誤!'
        elif param == 'name':
            if not(re.match('^[()\w\s]{1,50}$', param)):
                ret_code, ret_description = err_code, '銀行名稱格式錯誤!'
        elif param == 'account':
            if not(re.match('^[!@.#$%)(^&*\+\-\w\s]{1,50}$', param)):
                ret_code, ret_description = err_code, '銀行戶名格式錯誤!'
        elif param == 'account_name':
            if not(re.match('^[\-\d]{1,50}$', param)):
                ret_code, ret_description = err_code, '銀行帳號格式錯誤!'
        return ret_code, ret_description
        

class Shop_Rate(models.Model):
    def validator_between_one_and_five(value):
        if value<1 or value>5:
            raise ValidationError(
                '%s is not between 1 and 5'%value,
                params={'value': value},
            )
    id = models.CharField(primary_key=True, max_length=36)
    shop_id = models.CharField(max_length=36)
    user_id = models.CharField(max_length=36)
    rating = models.FloatField(validators=[validator_between_one_and_five])
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def validate_column(column_name, err_code, param):
        ret_code = 0
        ret_description = ''
        if param is 'shop_id':
            pass
        elif param is 'user_id':
            pass
        elif param is 'rating':
            pass
            if not(re.match('^\d+$', param)):
                ret_code, ret_description = err_code, '格式錯誤!'
        elif param is 'comment':
            pass
            if not(re.match('^[()\w\s]+$', param)):
                ret_code, ret_description = err_code, '格式錯誤!'
        return ret_code, ret_description


class Shipment_default_method(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    shipment_default_desc = models.CharField(max_length=255)
    onoff = models.CharField(max_length=50)

class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    shop_id = models.CharField(max_length=36)
    product_category_id = models.CharField(max_length=36)
    product_sub_category_id = models.CharField(max_length=36)
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
    longterm_stock_up= models.PositiveIntegerField()
    user_id = models.CharField(max_length=36)
    length = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    like = models.PositiveIntegerField()
    seen = models.PositiveIntegerField()
    sold_quantity = models.PositiveIntegerField()
    product_status= models.CharField(max_length=50)
    product_spec_on=models.CharField(max_length=1)
    is_delete=models.CharField(max_length=1, default='N')
    def validate_column(column_name, err_code, param):
        ret_code = 0
        ret_description = ''
        if column_name=='shop_id':
            if not(param):
                ret_code, ret_description = err_code, '未填寫商店編號!'
            elif not(Shop.objects.get(id=param,is_delete='N').exists()):
                ret_code, ret_description = err_code, '商店編號不存在!'
            else:
                pass
                #ret_code, ret_description = err_code, '商店編號格式錯誤!'
        elif column_name=='product_category_id':
            if not(param):
                ret_code, ret_description = err_code, '未填寫產品分類編號!'
            elif not(Product_Category.objects.get(id=param).exists()):
                ret_code, ret_description = err_code, '產品分類編號不存在!'
            else:
                try:
                    Product_Category.objects.get(id=param)
                except:
                    ret_code, ret_description = err_code, '產品分類編號格式錯誤!'
        elif column_name=='product_sub_category_id':
            if not(param):
                ret_code, ret_description = err_code, '未填寫產品子分類編號!'
            elif not(Product_Sub_Category.objects.get(id=param).exists()):
                ret_code, ret_description = err_code, '產品子分類編號不存在!'
            else:
                try:
                    Product_Sub_Category.objects.get(id=param)
                except:
                    ret_code, ret_description = err_code, '產品子分類編號格式錯誤!'
        elif column_name=='product_title':
            if not(param):
                ret_code, ret_description = err_code, '未填寫產品標題!'
            elif not(re.match('^\w+$', param)):
                ret_code, ret_description = err_code, '產品標題格式錯誤!'
        elif column_name=='quantity':
            if param:
                if not(re.match('^\d+$', param)):
                    ret_code, ret_description = err_code, '產品庫存數量格式錯誤!'
        elif column_name=='product_description':
            if not(param):
                ret_code, ret_description = err_code, '未填寫產品描述!'
            elif not(re.match('^\w+$', param)):
                ret_code, ret_description = err_code, '產品描述格式錯誤!'
        elif column_name=='product_price':
            if not(param):
                ret_code, ret_description = err_code, '未填寫產品單價!'
            elif not(re.match('^\d+$', param)):
                ret_code, ret_description = err_code, '產品價格格式錯誤!'
        elif column_name=='shipping_fee':
            if not(param):
                ret_code, ret_description = err_code, '未填寫產品運費!'
            elif not(re.match('^\d+$', param)):
                ret_code, ret_description = err_code, '產品運費格式錯誤!'
        elif column_name=='weight':
            if param:
                if not(re.match('^\d+$', param)):
                    ret_code, ret_description = err_code, '產品重量格式錯誤!'
        elif column_name=='new_secondhand':
            if not(param):
                ret_code, ret_description = err_code, '未填寫全新或二手!'
        elif column_name=='longterm_stock_up':
            pass
        elif column_name=='user_id':
            pass
        elif column_name=='length':
            pass
        elif column_name=='width':
            pass
        elif column_name=='height':
            pass
        elif column_name=='like':
            pass
        elif column_name=='seen':
            pass
        elif column_name=='sold_quantity':
            pass

        return ret_code, ret_description
  

class Product_Category(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
    product_category_id = models.CharField(max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
    c_product_color = models.CharField(max_length=50)
    e_product_color = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Selected_Product_Color(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    product_id = models.CharField(max_length=36)
    color_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Size(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    c_product_size = models.CharField(max_length=50)
    e_product_size = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Selected_Product_Size(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    product_id = models.CharField(max_length=36)
    size_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Origin(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    c_product_origin = models.CharField(max_length=50)
    e_product_origin = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Selected_Product_Pic(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    product_id = models.CharField(max_length=36)
    product_pic = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover = models.CharField(max_length=2)
    seq = models.IntegerField()

class Shop_Analytics(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    shop_id = models.CharField(max_length=36)
    user_id = models.CharField(max_length=255)
    seq = models.PositiveIntegerField()
    pic_path_1 = models.CharField(max_length=255)
    pic_path_2 = models.CharField(max_length=255)
    pic_path_3 = models.CharField(max_length=255)
    shop_name = models.CharField(max_length=50)
    shop_icon = models.CharField(max_length=255)
    rating = models.FloatField()
    followed = models.CharField(max_length=1)
    follower_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Email_Validation(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.CharField(max_length=36)
    email = models.CharField(max_length=50)
    validation_code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Audit_Log(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.CharField(max_length=36)
    action = models.CharField(max_length=100)
    parameter_in = models.TextField()
    parameter_out = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shop_Follower(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    shop_id = models.CharField(max_length=36)
    follower_id = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Rate(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.CharField(max_length=36)
    product_id = models.CharField(max_length=36)
    rating = models.PositiveIntegerField()
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    spec_id = models.CharField(max_length=36)
    
class Shop_Score(models.Model):
    user_id = models.CharField(max_length=36)
    shop_id = models.CharField(max_length=36)
    # from shop table
    score = models.FloatField() #or models.FloatField(**options)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Spec(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    product_id = models.CharField(max_length=36)
    spec_desc_1 = models.CharField(max_length=255)
    spec_desc_2 = models.CharField(max_length=255)
    spec_dec_1_items = models.CharField(max_length=255)
    spec_dec_2_items = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Shipment_Method(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    product_id = models.CharField(max_length=36)
    shipment_desc = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    onoff = models.CharField(max_length=50)
    shop_id = models.CharField(max_length=36)

class Shop_Order(models.Model):
    id = models.TextField(primary_key=True, max_length=36)
    shop_id = models.CharField(max_length=36)
    user_id = models.CharField(max_length=36)
    user_address_id = models.CharField(max_length=36)
    payment_id = models.CharField(max_length=36)
    product_shipment_id = models.CharField(max_length=36)
    shop_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    waybill_number = models.CharField(max_length=25)
    name_in_address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    full_address = models.CharField(max_length=50)
    product_shipment_desc = models.CharField(max_length=255)
    payment_desc = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_number = models.CharField(max_length=25,unique=True)
    payment_at = models.DateTimeField()
    actual_deliver_at   = models.DateTimeField()
    estimated_deliver_at= models.DateTimeField()
    actual_finished_at  = models.DateTimeField()

class Shop_Order_Details(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    shop_order_id = models.TextField(max_length=36)
    product_id = models.CharField(max_length=36)
    product_spec_id = models.CharField(max_length=36,null=True)
    product_shipment_id = models.CharField(max_length=36, null=True)
    product_description = models.TextField(null=True)
    spec_desc_1 = models.CharField(max_length=255, null=True)
    spec_desc_2 = models.CharField(max_length=255, null=True)
    spec_dec_1_items = models.CharField(max_length=255, null=True)
    spec_dec_2_items = models.CharField(max_length=255, null=True)
    unit_price = models.FloatField(null=True)
    quantity = models.PositiveIntegerField(null=True)
    purchasing_qty = models.PositiveIntegerField(null=True)
    logistic_fee = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Liked(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    product_id = models.CharField(max_length=36)
    user_id = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Product_Browsed(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    product_id = models.CharField(max_length=36)
    user_id = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Clicked(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    product_id = models.CharField(max_length=36)
    user_id = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shop_Browsed(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    shop_id = models.CharField(max_length=36)
    user_id = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Analytics(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.CharField(max_length=36)
    seq = models.PositiveIntegerField()
    product_id = models.CharField(max_length=36)
    pic_path= models.CharField( max_length=255)
    product_title= models.CharField( max_length=255)
    shop_title = models.CharField(max_length=255)
    min_price= models.PositiveIntegerField()
    max_price= models.PositiveIntegerField()
    liked= models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

class Search_History(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    search_category = models.CharField(max_length=25)
    keyword = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Shopping_Cart(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id =  models.CharField(max_length=36)
    product_id =  models.CharField(max_length=36)
    product_spec_id =  models.CharField(max_length=36)
    product_shipment_id =  models.CharField(max_length=36)
    quantity =  models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_address_id=  models.CharField(max_length=36)
    payment_id=  models.CharField(max_length=36)
    shop_id=models.CharField(max_length=36)
    is_delete=models.CharField(max_length=1)

class User_Address(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id =  models.CharField(max_length=36)
    name =  models.CharField(max_length=50)
    country_code = models.CharField(max_length=50)
    phone =  models.CharField(max_length=50)
    is_phone_show =  models.CharField(max_length=50)
    area =  models.CharField(max_length=50)
    district =  models.CharField(max_length=50)
    road =  models.CharField(max_length=50)
    number =  models.CharField(max_length=50)
    other =  models.CharField(max_length=50)
    floor =  models.CharField(max_length=50)
    room =  models.CharField(max_length=50)
    is_address_show =  models.CharField(max_length=1)
    is_default =  models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    def validate_column(column_name, err_code, param):
        ret_code = 0
        ret_description = ''
    
        if param == 'name':
            if param:
                if not(re.match('^[!@.#$%)(^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '姓名/公司名稱格式錯誤!'
        elif param == 'country_code':
            if param:
                if not(re.match('^[\+\d]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '國碼格式錯誤!'
        elif param == 'phone':
            if param:
                if not(re.match('^\d+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '電話號碼格式錯誤!'
        elif param == 'is_phone_show':
            if param:
                if not(re.match('^\w+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '顯示在店鋪簡介格式錯誤!'
        elif param == 'area':
            if param:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '地域格式錯誤!'
        elif param == 'district':
            if param:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '地區格式錯誤!'
        elif param == 'road':
            if param:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '街道名稱格式錯誤!'
        elif param == 'number':
            if param:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '街道門牌格式錯誤!'
        elif param == 'other':
            if param:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '其他地址格式錯誤!'
        elif param == 'floor':
            if param:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '樓層格式錯誤!'
        elif param == 'room':
            if param:
                if not(re.match('^[!@.#$%^&*\+\-\w\s]+$', param)) or len(param)>50:
                    ret_code, ret_description = err_code, '房(室)名稱格式錯誤!'
        return  ret_code, ret_description

class Payment_Method(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    payment_desc = models.CharField(max_length=50, null=True)
    is_default = models.CharField(max_length=1, null=True, default='N')
    button_path = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class App_Version(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    app_type = models.CharField(max_length=10, null=True)
    version_number = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Bank_Code(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    bank_code = models.CharField(max_length=3)
    bank_name = models.CharField(max_length=200)
    seq = models.IntegerField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User_Payment_Account(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    payment_type = models.CharField(max_length=10)
    user_id = models.CharField(max_length=36)
    bank_code = models.CharField(max_length=3)
    bank_name = models.CharField(max_length=200)
    bank_account_name = models.CharField(max_length=100)
    contact_type = models.CharField(max_length=25)
    phone_country_code = models.CharField(max_length=5, null=True)
    phone_number = models.CharField(max_length=10, null=True)
    contact_email = models.CharField(max_length=50, null=True)
    is_default = models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User_Rate(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    shop_id =  models.CharField(max_length=36)
    user_id =  models.CharField(max_length=36)
    rating =  models.FloatField()
    comment =  models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FPS_Order_Transaction(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    order_id = models.CharField(max_length=36)
    user_payment_account_id = models.CharField(max_length=36)
    target_delivery_date = models.DateField()
    target_delivery_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order_Error(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    shopping_cart_id = models.CharField(max_length=36)
    product_id = models.CharField(max_length=36)
    product_specification_id = models.CharField(max_length=36, null=True)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Ad_Setting_Header(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.CharField(max_length=36)
    ad_category = models.CharField(max_length=20)
    ad_type = models.CharField(max_length=10)
    budget_type = models.CharField(max_length=10)
    budget_amount = models.PositiveIntegerField(null=True)
    ad_period_type = models.CharField(max_length=10)
    start_datetime = models.DateTimeField(null=True)
    end_datetime = models.DateTimeField(null=True)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def validate_column(column_name, err_code, param):
        ret_code = 0
        ret_description = ''
        if column_name == 'category':
            if not(param):
                ret_code, ret_description = err_code, 'category不能為空'
            elif param not in ['keyword', 'recommend', 'store']:
                ret_code, ret_description = err_code, 'category應為 keyword 或 recommend 或 store'
        elif column_name == 'ad_type':
            if not(param):
                ret_code, ret_description = err_code, 'ad_type不能為空'
            elif param not in ['product', 'shop']:
                ret_code, ret_description = err_code, 'ad_type應為 product 或 shop'
        elif column_name == 'budget_type':
            if not(param):
                ret_code, ret_description = err_code, 'budget_type不能為空'
            elif param not in ['unlimit', 'total', 'day']:
                ret_code, ret_description = err_code, 'budget_type應為 unlimit 或 total 或 day'
        elif column_name == 'budget_amount':
            if param and float(param)<0:
                ret_code, ret_description = err_code, 'budget_amount不能為負'
        elif column_name == 'ad_period_type':
            if not(param):
                ret_code, ret_description = err_code, 'ad_period_type不能為空'
            elif param not in ['unlimit', 'custom']:
                ret_code, ret_description = err_code, 'ad_period_type應為 unlimit 或 custom'
        elif column_name == 'start_datetime':
            if param:
                try:
                    datetime.strptime(param, '%Y-%m-%d %H:%M:%S')
                except:
                    ret_code, ret_description = err_code, 'start_datetime應為YYYY-MM-DD hh:mm:ss'
        elif column_name == 'end_datetime':
            if param:
                try:
                    datetime.strptime(param, '%Y-%m-%d %H:%M:%S')
                except:
                    ret_code, ret_description = err_code, 'end_datetime應為YYYY-MM-DD hh:mm:ss'

        return ret_code, ret_description

class Ad_Setting_Detail(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    ad_setting_header_id = models.CharField(max_length=36)
    ad_img = models.CharField(max_length=255)
    shop_id = models.CharField(max_length=36, null=True)
    product_id = models.CharField(max_length=36, null=True)
    keyword = models.CharField(max_length=200, null=True)
    bid = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Country_Shop_Setting(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    country_code = models.CharField(max_length=2)
    shop_code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shop_Order_Setting(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    shop_id = models.CharField(max_length=36)
    country_code = models.CharField(max_length=2)
    shop_code = models.CharField(max_length=5)
    order_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Rate_Pic(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    rate_id = models.CharField(max_length=36)
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order_Rate(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    order_id = models.CharField(max_length=36)
    logistics  = models.FloatField()
    service = models.FloatField()
    anonymous = models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Paypal_Transactions(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    order_number = models.CharField(max_length=25)
    paypal_transaction_id = models.CharField(max_length=30)
    paypal_payer_id = models.CharField(max_length=15, null=True)
    transaction_amount = models.FloatField()
    transaction_currency_code = models.CharField(max_length=5)
    fee_amount = models.CharField(max_length=10)
    fee_currency_code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order_Message(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    order_status = models.CharField(max_length=255)
    buyer_message_content = models.TextField()
    shop_message_content= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    buyer_message_title = models.CharField(max_length=255)
    shop_message_title = models.CharField(max_length=255)