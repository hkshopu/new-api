# Generated by Django 3.1.5 on 2021-01-21 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hkshopu', '0006_product_category_product_sub_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='discount_by_amount',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='discount_by_percent',
            field=models.PositiveIntegerField(null=True),
        ),
    ]