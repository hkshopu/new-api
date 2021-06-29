from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.db.models import Q
from hkshopu import models
import re
import uuid

# Create your views here.

# 取得訂單資訊
def convert_shopping_cart_items_to_order(request):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'data': []
    }
    if request.method == 'POST':
        # 欄位資料
        shopping_cart_id = request.POST.getlist('shopping_cart_id', [])

        if response_data['status'] == 0:
            if not(shopping_cart_id):
                response_data['status'] = -1
                response_data['ret_val'] = '未填寫購物車編號!'

        if response_data['status'] == 0:
            unsellable_products = []
            shopping_carts = models.Shopping_Cart.objects.filter(id__in=shopping_cart_id).values('user_id', 'product_id', 'product_spec_id', 'product_shipment_id', 'quantity', 'user_address_id', 'payment_id')
            for shopping_cart in shopping_carts:
                if shopping_cart['product_spec_id'] == '':
                    sellable_products = models.Product.objects.filter(id=shopping_cart['product_id'], quantity__gt=shopping_cart['quantity']).values('id')
                else:
                    sellable_products = models.Product_Spec.objects.filter(id=shopping_cart['product_spec_id'], quantity__gt=shopping_cart['quantity']).values('id')
                if len(sellable_products) == 0:
                    products = models.Product.objects.filter(id=shopping_cart['product_id']).values('product_description')
                    product_specs = models.Product_Spec.objects.filter(id=shopping_cart['product_spec_id']).values('spec_desc_1', 'spec_desc_2', 'spec_dec_1_items', 'spec_dec_2_items')
                    unsellable_products.append({
                        'product_description': products[0]['product_description'] if len(products) > 0 else '', 
                        'spec_desc_1': product_specs[0]['spec_desc_1'] if len(product_specs) > 0 else '', 
                        'spec_desc_2': product_specs[0]['spec_desc_2'] if len(product_specs) > 0 else '', 
                        'spec_dec_1_items': product_specs[0]['spec_dec_1_items'] if len(product_specs) > 0 else '', 
                        'spec_dec_2_items': product_specs[0]['spec_dec_2_items'] if len(product_specs) > 0 else ''
                    })
            if len(unsellable_products) > 0:
                response_data['data'] = unsellable_products
                response_data['status'] = -2
                response_data['ret_val'] = '產品庫存量不足!'

        if response_data['status'] == 0:
            # 購物車資訊
            datas_of_shopping_cart = []
            for shopping_cart in shopping_carts:
                products = models.Product.objects.filter(id=shopping_cart['product_id']).values('shop_id', 'quantity')
                product_specs = models.Product_Spec.objects.filter(id=shopping_cart['product_spec_id']).values('quantity')
                datas_of_shopping_cart.append({
                    'user_id': shopping_cart['user_id'], 
                    'product_id': shopping_cart['product_id'], 
                    'product_spec_id': shopping_cart['product_spec_id'], 
                    'product_shipment_id': shopping_cart['product_shipment_id'], 
                    'quantity': shopping_cart['quantity'], 
                    'user_address_id': shopping_cart['user_address_id'], 
                    'payment_id': shopping_cart['payment_id'], 
                    'shop_id': products[0]['shop_id'] if len(products) > 0 else ''
                })
                # 更新產品庫存
                if shopping_cart['product_spec_id'] == '':
                    models.Product.objects.filter(id=shopping_cart['product_id']).update(quantity=products[0]['quantity'] - shopping_cart['quantity'])
                else:
                    models.Product_Spec.objects.filter(id=shopping_cart['product_spec_id']).update(quantity=product_specs[0]['quantity'] - shopping_cart['quantity'])
            # 寫入 shop_order 資料表
            datas_of_shop_order = []
            for data_of_shopping_cart in datas_of_shopping_cart:
                shop_orders = models.Shop_Order.objects.filter(shop_id=data_of_shopping_cart['shop_id'], product_shipment_id=data_of_shopping_cart['product_shipment_id']).values('id')
                if len(shop_orders) == 0:
                    shops = models.Shop.objects.filter(id=data_of_shopping_cart['shop_id']).values('shop_title')
                    users = models.User.objects.filter(id=data_of_shopping_cart['user_id']).values('first_name', 'last_name', 'phone')
                    product_shipment_methods = models.Product_Shipment_Method.objects.filter(id=data_of_shopping_cart['product_shipment_id']).values('shipment_desc')
                    payment_methods = models.Payment_Method.objects.filter(id=data_of_shopping_cart['payment_id']).values('payment_desc')
                    user_addresses = models.User_Address.objects.filter(id=data_of_shopping_cart['user_address_id']).values('name')
                    id_of_shop_order = uuid.uuid4()
                    datas_of_shop_order.append({
                        'id': id_of_shop_order, 
                        'order_number': '', 
                        'shop_id': data_of_shopping_cart['shop_id'], 
                        'shop_name': shops[0]['shop_title'] if len(shops) > 0 else '', 
                        'user_id': data_of_shopping_cart['user_id'], 
                        'first_name': users[0]['first_name'] if len(users) > 0 else '', 
                        'last_name': users[0]['last_name'] if len(users) > 0 else '', 
                        'product_shipment_id': data_of_shopping_cart['product_shipment_id'], 
                        'product_shipment_desc': product_shipment_methods[0]['shipment_desc'] if len(product_shipment_methods) > 0 else '', 
                        'status': 'Pending Payment', 
                        'payment_id': data_of_shopping_cart['payment_id'], 
                        'payment_desc': payment_methods[0]['payment_desc'] if len(payment_methods) > 0 else '', 
                        'waybill_number': '', 
                        'user_address_id': data_of_shopping_cart['user_address_id'], 
                        'name_in_address': user_addresses[0]['name'] if len(user_addresses) > 0 else '', 
                        'phone': users[0]['phone'] if len(users) > 0 else '', 
                        'full_address': ''
                    })
                    models.Shop_Order.objects.create(
                        id=id_of_shop_order, 
                        order_number='', 
                        shop_id=data_of_shopping_cart['shop_id'], 
                        shop_name=shops[0]['shop_title'] if len(shops) > 0 else '', 
                        user_id=data_of_shopping_cart['user_id'], 
                        first_name=users[0]['first_name'] if len(users) > 0 else '', 
                        last_name=users[0]['last_name'] if len(users) > 0 else '', 
                        product_shipment_id=data_of_shopping_cart['product_shipment_id'], 
                        product_shipment_desc=product_shipment_methods[0]['shipment_desc'] if len(product_shipment_methods) > 0 else '', 
                        status='Pending Payment', 
                        payment_id=data_of_shopping_cart['payment_id'], 
                        payment_desc=payment_methods[0]['payment_desc'] if len(payment_methods) > 0 else '', 
                        waybill_number='', 
                        user_address_id=data_of_shopping_cart['user_address_id'], 
                        name_in_address=user_addresses[0]['name'] if len(user_addresses) > 0 else '', 
                        phone=users[0]['phone'] if len(users) > 0 else '', 
                        full_address=''
                    )
            # 寫入 shop_order_details 資料表
            for data_of_shop_order in datas_of_shop_order:
                for data_of_shopping_cart in datas_of_shopping_cart:
                    if data_of_shopping_cart['shop_id'] == data_of_shop_order['shop_id'] and data_of_shopping_cart['product_shipment_id'] == data_of_shop_order['product_shipment_id']:
                        products = models.Product.objects.filter(id=data_of_shopping_cart['product_id']).values('product_description', 'product_price')
                        product_specs = models.Product_Spec.objects.filter(id=data_of_shopping_cart['product_spec_id']).values('spec_desc_1', 'spec_desc_2', 'spec_dec_1_items', 'spec_dec_2_items')
                        models.Shop_Order_Details.objects.create(
                            id=uuid.uuid4(), 
                            order_id=data_of_shop_order['id'], 
                            product_id=data_of_shopping_cart['product_id'], 
                            product_description=products[0]['product_description'] if len(products) > 0 else '', 
                            product_spec_id=data_of_shopping_cart['product_spec_id'], 
                            spec_desc_1=product_specs[0]['spec_desc_1'] if len(product_specs) > 0 else '', 
                            spec_desc_2=product_specs[0]['spec_desc_2'] if len(product_specs) > 0 else '', 
                            spec_dec_1_items=product_specs[0]['spec_dec_1_items'] if len(product_specs) > 0 else '', 
                            spec_dec_2_items=product_specs[0]['spec_dec_2_items'] if len(product_specs) > 0 else '', 
                            quantity=data_of_shopping_cart['quantity'], 
                            unit_price=products[0]['product_price'] if len(products) > 0 else 0, 
                            product_shipment_id=data_of_shopping_cart['product_shipment_id'], 
                            logistic_fee=0
                        )
            # 刪除原先購物車中的資料
            models.Shopping_Cart.objects.filter(id__in=shopping_cart_id).delete()
            response_data['data'] = datas_of_shop_order
            response_data['ret_val'] = '取得訂單資訊成功!'
    return JsonResponse(response_data)