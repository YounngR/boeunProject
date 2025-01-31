# Generated by Django 2.2.7 on 2020-03-11 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boeun_bread', '0006_merge_20200311_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='non_user_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='non_user_phone',
            field=models.EmailField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(blank=True, default='결제대기', max_length=200, null=True),
        ),
    ]
