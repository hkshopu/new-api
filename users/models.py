from django.db import models

# Create your models here.
class HKShopU_User(models.Model):
    account_name = models.CharField(max_length=50)
    google_account = models.CharField(max_length=50)
    facebook_account = models.CharField(max_length=50)
    apple_account = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    birthday = models.DateField()
    mobile = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)