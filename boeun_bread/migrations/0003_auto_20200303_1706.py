# Generated by Django 2.2.7 on 2020-03-03 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boeun_bread', '0002_auto_20200302_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='U_Reason',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='U_delete',
            field=models.BooleanField(default=False),
        ),
    ]
