# Generated by Django 2.2.7 on 2020-03-02 03:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('hit', models.IntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_address', models.CharField(max_length=200)),
                ('User_detail_address', models.CharField(max_length=100)),
                ('Order_Number', models.CharField(max_length=200)),
                ('Total_price', models.IntegerField(default=0)),
                ('Order_date', models.DateField(auto_now_add=True)),
                ('Order_type', models.IntegerField(default=0)),
                ('Order_hope_date', models.DateTimeField(blank=True, null=True)),
                ('Order_request_content', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('P_img', models.ImageField(blank=True, null=True, upload_to='bread_img/')),
                ('P_name', models.CharField(max_length=50)),
                ('P_price', models.IntegerField(default=0)),
                ('P_nutrition', models.TextField(blank=True, null=True)),
                ('P_info', models.TextField(blank=True, null=True)),
                ('P_sales', models.IntegerField(default=0)),
                ('P_newProduct', models.BooleanField(default=False)),
                ('P_kind', models.CharField(choices=[('1', '제빵'), ('2', '제과'), ('3', '선물세트')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cookie_id', models.CharField(blank=True, max_length=30, null=True)),
                ('U_phone', models.CharField(blank=True, max_length=11, null=True)),
                ('U_is_active', models.BooleanField(default=False)),
                ('U_grade', models.IntegerField(default=2)),
                ('U_name', models.CharField(blank=True, max_length=20, null=True)),
                ('U_groupName', models.CharField(blank=True, max_length=50, null=True)),
                ('U_email', models.EmailField(max_length=50)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QNA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('answer', models.TextField()),
                ('question_kind', models.CharField(choices=[('1', '배달기준')], max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boeun_bread.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Order_Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('product_img', models.ImageField(upload_to='')),
                ('product_name', models.CharField(max_length=50)),
                ('product_price', models.IntegerField(default=0)),
                ('product_count', models.IntegerField(default=0)),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='boeun_bread.Order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='boeun_bread.Profile'),
        ),
        migrations.CreateModel(
            name='Cart_Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('product_img', models.ImageField(upload_to='')),
                ('product_name', models.CharField(max_length=50)),
                ('product_price', models.IntegerField(default=0)),
                ('product_count', models.IntegerField(default=0)),
                ('Cart', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='CartProduct', to='boeun_bread.Cart')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='boeun_bread.Profile'),
        ),
        migrations.CreateModel(
            name='BoardFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boeun_bread.Board')),
            ],
        ),
        migrations.AddField(
            model_name='board',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boeun_bread.Profile'),
        ),
    ]