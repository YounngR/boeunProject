# Generated by Django 2.2 on 2020-01-08 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boeun_bread', '0003_auto_20200108_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='P_img',
            field=models.ImageField(blank=True, null=True, upload_to='bread_img/'),
        ),
    ]
