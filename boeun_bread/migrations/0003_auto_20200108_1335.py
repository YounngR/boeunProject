# Generated by Django 2.2.7 on 2020-01-08 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boeun_bread', '0002_product_p_newproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='U_grade',
            field=models.IntegerField(default=2),
        ),
    ]
