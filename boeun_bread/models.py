
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Profile(models.Model):
    user        = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    cookie_id   = models.CharField(max_length=30, null=True, blank=True)
    U_phone     = models.CharField(max_length=11,null=True,blank=True)
    U_is_active = models.BooleanField(default=False) #True : 인증된 회원
    U_grade     = models.IntegerField(default=2) # 0:관리자 1:회원 2:비회원
    U_name      = models.CharField(max_length=20,null=True,blank=True)
    U_groupName = models.CharField(max_length=50, null=True, blank=True)
    U_email     = models.EmailField(max_length=50)
    U_delete    = models.BooleanField(default=False) #True = 탈퇴
    U_Reason    = models.IntegerField(default=0)

class Product(models.Model):
    PRODUCT_KIND =(
        ('1','제빵'),
        ('2','제과'),
        ('3','선물세트'),
    )
    P_img        = models.ImageField(upload_to="bread_img/",null=True,blank=True)
    P_name       = models.CharField(max_length=50)
    P_price      = models.IntegerField(default=0)
    P_nutrition  = models.TextField(null=True, blank=True)
    P_info       = models.TextField(null=True, blank=True)
    P_sales      = models.IntegerField(default=0) # 판매량
    P_newProduct = models.BooleanField(default=False) #True : 신제품
    P_kind       = models.CharField(max_length=1,choices=PRODUCT_KIND) #상품종류
    def __str__(self):
        return self.P_name


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
    User                  = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    User_address          = models.CharField(max_length=200)
    User_detail_address   = models.CharField(max_length=100) #상세 주소
    Order_Number          = models.CharField(max_length=200)
    Total_price           = models.IntegerField(default=0)
    Order_date            = models.DateField(auto_now_add=True)
    Order_type            = models.IntegerField(default=0) # 0 : 결제확인
    Order_hope_date       = models.DateTimeField(null=True,blank=True) #배송 희망일
    Order_request_content = models.CharField(null=True,blank=True,max_length=200) #주문시 요청사항

class Order_Product(models.Model):
    Order         = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product_id    = models.IntegerField()
    product_img   = models.ImageField()
    product_name  = models.CharField(max_length=50)
    product_price = models.IntegerField(default=0)
    product_count = models.IntegerField(default=0)

class Board(models.Model):
    user    = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title   = models.CharField(max_length=200) #공지사항 제목
    content = models.TextField() #공지사항 내용
    hit     = models.IntegerField(default=0) #조회수
    date    = models.DateField(auto_now_add=True) # 작성날짜

class BoardFile(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    file  = models.FileField(upload_to="board/") #첨부파일

class QNA(models.Model):
    QUESTION_KIND =(
        ('1','배달기준'),

    )
    user          = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question      = models.CharField(max_length=200) #질문
    answer        = models.TextField() #내용
    question_kind = models.CharField(max_length=1,choices=QUESTION_KIND) #질문유형
