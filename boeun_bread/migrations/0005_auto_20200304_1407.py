# Generated by Django 2.2.7 on 2020-03-04 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boeun_bread', '0004_delivery_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='delivery_status',
            field=models.CharField(choices=[('1', '상품준비중'), ('2', '배송중'), ('3', '배송완료')], default='1', max_length=1),
        ),
    ]