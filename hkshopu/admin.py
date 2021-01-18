from django.contrib import admin
from hkshopu import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Shop)
admin.site.register(models.Shop_Category)