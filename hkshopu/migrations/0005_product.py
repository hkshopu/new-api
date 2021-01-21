# Generated by Django 3.1.5 on 2021-01-21 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hkshopu', '0004_auto_20210118_1539'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_id', models.PositiveIntegerField()),
                ('product_category_id', models.PositiveIntegerField()),
                ('product_sub_category_id', models.PositiveIntegerField()),
                ('product_title', models.CharField(max_length=50)),
                ('quantity', models.PositiveIntegerField()),
                ('product_description', models.TextField()),
                ('product_country_code', models.CharField(max_length=5)),
                ('product_price', models.PositiveIntegerField()),
                ('shipping_fee', models.PositiveIntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
