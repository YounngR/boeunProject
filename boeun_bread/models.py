from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user        = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    cookie_id   = models.CharField(max_length=30, null=True, blank=True)
    U_phone     = models.CharField(max_length=11,null=True,blank=True)
    U_is_active = models.BooleanField(default=False) #True : 인증된 회원
    U_grade     = models.IntegerField(default=2) # 0:관리자 1:회원 2:비회원
    U_name      = models.CharField(max_length=20,null=True,blank=True)
    U_groupName = models.CharField(max_length=50, null=True, blank=True)
    U_email     = models.EmailField(max_length=50)

class Product(models.Model):
    P_img       = models.ImageField(upload_to="bread_img/",null=True,blank=True)
    P_name      = models.CharField(max_length=50)
    P_price     = models.IntegerField(default=0)
    P_nutrition = models.TextField(null=True, blank=True)
    P_info = models.TextField(null=True, blank=True)
    P_sales = models.IntegerField(default=0)
    P_newProduct = models.BooleanField(default=False) #True : 신제품

class Cart(models.Model):
    User = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    def get_total(self):
        total = 0
        query_set = self.CartProduct.all()
        for obj in query_set:
            total += (obj.product_price * obj.product_count)
        return total


class Cart_Product(models.Model):
    Cart          = models.ForeignKey(Cart, related_name='CartProduct',on_delete=models.DO_NOTHING)
    product_id    = models.IntegerField()
    product_img   = models.ImageField()
    product_name  = models.CharField(max_length=50)
    product_price = models.IntegerField(default=0)
    product_count = models.IntegerField(default=0)



class Order(models.Model):
    User  = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    User_address = models.CharField(max_length=200)
    Order_Number = models.CharField(max_length=200)
    Total_price = models.IntegerField(default=0)
    Order_date = models.DateTimeField(auto_now_add=True)
    Order_type = models.IntegerField(default=0) # 0 : 결제확인

class Order_Product(models.Model):
    Order         = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product_id    = models.IntegerField()
    product_img   = models.ImageField()
    product_name  = models.CharField(max_length=50)
    product_price = models.IntegerField(default=0)
    product_count = models.IntegerField(default=0)
