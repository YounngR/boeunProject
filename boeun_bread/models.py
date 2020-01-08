from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    U_phone = models.CharField(max_length=11)
    U_is_active = models.BooleanField(default=False) #True : 인증된 회원
    U_grade = models.IntegerField(default=0) # 0:관리자 1:회원 2:비회원
    U_groupName = models.CharField(max_length=50, null=True, blank=True)

class Product(models.Model):
    P_name = models.CharField(max_length=50)
    P_price = models.IntegerField(default=0)
    P_nutrition = models.TextField(null=True, blank=True)
    P_info = models.TextField(null=True, blank=True)
    P_sales = models.IntegerField(default=0)
    P_newProduct = models.BooleanField(default=False) #True : 신제품

class Cart(models.Model):
    User = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)

class Cart_Product(models.Model):
    Cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    product_name = models.CharField(max_length=50)
    product_count = models.IntegerField(default=0)

class Order(models.Model):
    User = User = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    User_address = models.CharField(max_length=50)
    Total_price = models.IntegerField(default=0)
    Order_date = models.DateTimeField()

class Order_Product(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product_name = models.CharField(max_length=50)
    product_count = models.IntegerField(default=0)
