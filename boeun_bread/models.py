
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
    User_address          = models.CharField(max_length=200) #주소
    User_detail_address   = models.CharField(max_length=100) #상세 주소
    Order_Number          = models.CharField(max_length=200)#주문번호
    Total_price           = models.IntegerField(default=0) # 주문 총금액
    Order_date            = models.DateField(auto_now_add=True) #주문 날짜
    Order_type            = models.IntegerField(default=0) # 0 : 결제확인
    Order_hope_date       = models.DateTimeField(null=True,blank=True) #배송 희망일
    Order_request_content = models.CharField(null=True,blank=True,max_length=200) #주문시 요청사항
    Order_status          = models.BooleanField(default=False) #True = 결제완료
    

class Delivery(models.Model):
    DELIVERY_STATUS = (
        ('1','상품준비중'),
        ('2','배송중'),
        ('3','배송완료')
    )
    order            = models.OneToOneField(Order,on_delete=models.CASCADE,null=True,blank=True)
    delivery_number  = models.CharField(max_length=30) #송장번호
    delivery_company = models.CharField(max_length=20) #택배회사
    #배송상태
    delivery_status  = models.CharField(max_length=1,choices=DELIVERY_STATUS,default='1')
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
    user             = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question_title   = models.CharField(max_length=200) #질문제목
    question_content = models.TextField()#질문내용
    question_kind    = models.CharField(max_length=1,choices=QUESTION_KIND) #질문유형
    '''
        true: 답변완료
        false: 답변 없음
    '''
    question_status  = models.BooleanField(default=False)
    question_date    = models.DateField(auto_now_add=True) #질문 날짜
    '''
        true : 비공개
        false: 공개
    '''
    is_private       = models.BooleanField(default=False)
class Answer(models.Model):
    qna           = models.OneToOneField(QNA,on_delete=models.CASCADE)
    answer        = models.TextField() #답변내용
    question_date = models.DateField(auto_now_add=True) #답변 날짜

class Reason(models.Model):
    REASON = (
        ('1','배송불만(지연,반품)'),
        ('2','홈페이지 사용 불편'),
        ('3','제품(빵) 가격 불만'),
        ('4','제품(빵) 품질 불만'),
        ('5','기타')
    )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reason = models.CharField(max_length=1, choices=REASON)
