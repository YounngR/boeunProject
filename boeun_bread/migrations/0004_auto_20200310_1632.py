# Generated by Django 2.2.7 on 2020-03-10 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boeun_bread', '0003_merge_20200310_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='post_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='qna',
            name='question_kind',
            field=models.CharField(choices=[('1', '상품정보'), ('2', '배송문의'), ('3', '결제문의'), ('4', '기타')], max_length=1),
        ),
    ]