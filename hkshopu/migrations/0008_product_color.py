# Generated by Django 3.1.5 on 2021-01-21 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hkshopu', '0007_auto_20210121_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.PositiveIntegerField()),
                ('c_product_color', models.CharField(max_length=50)),
                ('e_product_color', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
