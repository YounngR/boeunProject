from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User # 회원가입
from django.contrib import auth #로그
import json, random, string
#이메일 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
#from django.db.models import Sum
from django.contrib import messages
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import F
import pandas
from django.db.models import Q



#객체 반환
def get_object(model,**args):
    query_set = model.objects.filter(**args)
    return query_set[0] if query_set else None

#날짜 계산(일주일)


def main(request):
    return render(request,'boeun_bread/main.html')

#-----manage
#관리자 이냐?
def isAdmin(request):
    profile = Profile.objects.get(user=request.user)
    return True if profile.U_grade == 0 else False


#관리자 main
@login_required
def manage(request):
    if not isAdmin(request):
        return render(request,'boeun_bread/main.html',{'manage_msg':'권한 없습니다.'})

    return render(request,'manage/manage_main.html')

#상품등록
@login_required
def create_product(request):
    if not isAdmin(request):
        return render(request,'boeun_bread/main.html',{'manage_msg':'권한 없습니다.'})
    if request.method == "POST":
        is_new = True if request.POST.get('is_new')=="on" else False
        Product.objects.create(
            P_img        = request.FILES.get('bread_img'),
            P_name       = request.POST.get('bread_name'),
            P_price      = request.POST.get('bread_price'),
            P_kind       = request.POST.get('prod_name'),
            P_newProduct = is_new
        )
        return redirect('/manage')
    return render(request,'manage/create_product.html')
#주문 목록
@login_required
def order_list(request):
    if not isAdmin(request):
        return render(request,'boeun_bread/main.html',{'manage_msg':'권한 없습니다.'})
    if request.method == "POST":
        order = get_object(Order,id=request.POST.get('order_pk'))
        delivery = get_object(Delivery,order=order)
        if delivery:
            
            delivery.delivery_status = request.POST.get('status')
            delivery.save()
        else:
            Delivery.objects.create(
                order            = order,
                delivery_number  = request.POST.get('number'),
                delivery_company = request.POST.get('company'),
                delivery_status  = request.POST.get('status')
            )

    orders = Order.objects.all()
    context = {
        'orders':orders
    }
    return render(request,'manage/order_list.html',context)
#주문목록 팝업으로 보기
@login_required
def popup_order_list(request,page):
    order = get_object_or_404(Order,id=page)
    if not isAdmin(request):
        return render(request,'boeun_bread/main.html',{'manage_msg':'권한 없습니다.'})
    order_product = Order_Product.objects.filter(Order=order)
    context = {
        'order':order,
        'order_product':order_product
    }
    return render(request,'manage/popup_order_list.html',context)

#수정상품 리스트
@login_required
def modify_list(request):
    if not isAdmin(request):
        return render(request,'boeun_bread/main.html',{'manage_msg':'권한 없습니다.'})
    product = Product.objects.all()

    return render(request,'manage/modify_list.html',{'product':product})

#상품객체 반환
def getProduct(pk):
    product = Product.objects.filter(id=pk)
    if product:
        return product[0]
    else:
        return redirect("/manage/modify_list")


#상품수정
@login_required
def modify_product(request,pk):
    if not isAdmin(request):
        return render(request,'boeun_bread/main.html',{'manage_msg':'권한 없습니다.'})
    product = getProduct(pk)

    if request.method == "POST":
        is_new = True if request.POST.get('is_new')=="on" else False
        files = request.FILES.get('bread_img')
        if files:
            product.P_img = files
        product.P_name       = request.POST.get('bread_name')
        product.P_price      = request.POST.get('bread_price')
        product.P_newProduct = is_new
        product.P_kind       = request.POST.get('prod_name')
        product.save()
        return redirect("/manage/modify_list")

    context = {
            'p':product,
        }
    return render(request,'manage/modify_product.html',context)


#상품삭제
@login_required
def delete_product(request):
    if not isAdmin(request):
        return render(request,'boeun_bread/main.html',{'manage_msg':'권한 없습니다.'})
    if request.method == "POST":
        product = Product.objects.filter(id=request.POST.get('pk'))
        if product:
            product[0].delete()
        return redirect('/manage/modify_list')

@login_required
def manage_Sales_Status(request):


    prod = Product.objects.all()

    p_name_list = []
    p_salse_list = []

    for p in prod:
        p_name_list.append(p.P_name)
        p_salse_list.append(p.P_sales)


    return render(request, 'manage/manage_Sales_Status.html',{'prod':prod, 'p_name_list':p_name_list,'p_salse_list':p_salse_list})

@login_required
def manage_Sales_Status_table(request):

    bread_list = {}
    for name in Product.objects.all():
        bread_list[name.P_name] = 0

    order = Order.objects.all()

    if request.POST.get('year') != 0 and request.POST.get('month') != 0:
        order = Order.objects.filter(Order_date__year=request.POST.get('year'), Order_date__month=request.POST.get('month'))

    elif request.POST.get('year') != 0 and request.POST.get('month') == 0:
        order = Order.objects.filter(Order_date__year=request.POST.get('year'))

    elif request.POST.get('year') == 0 and request.POST.get('month') != 0:
        order = Order.objects.filter(Order_date__month=request.POST.get('month'))

    for order in order:
        for p_order in Order_Product.objects.filter(Order=order):
            bread_list[p_order.product_name] += p_order.product_count

    return render(request, 'manage/manage_Sales_Status_table.html', {'bread_list':bread_list, 'keyword':"change_table"})

#공지사항 작성
@login_required
def write_board(request):
    if not isAdmin(request):
        return render(request,'boeun_bread/main.html',{'manage_msg':'권한 없습니다.'})
    if request.method == "POST":
        files = request.FILES.getlist('file')
        '''
            client 삭제된 리스트로
            client 삭제된 파일 제외
        '''
        for index in request.POST.getlist('exclude_file'):
            try:
                del files[int(index)]
            except ValueError:
                pass
        board = Board.objects.create(
                    user    = request.user.profile,
                    title   = request.POST.get('title'),
                    content = request.POST.get('content')
                )
        for f in files:
            BoardFile.objects.create(
                board = board,
                file  = f
            )
        return redirect('/manage')
    return render(request,'manage/write_board.html')

#end manage

#로그인
def Login(request):


    return render(request, 'Login/Login.html')

#비회원 주문조회
def non_login(request):

    if request.method == "POST":
        context={}
        user = get_object(Profile,U_name=request.POST.get('user_id'), U_phone=request.POST.get('phone'))
        if user:
            order = Order.objects.filter(User=user)
            return render(request, 'mypage/non_login_order_lookup.html', {'order':order})
        else:
            context['msg'] = "주문내역이 존재하지않습니다."
            return render(request, 'Login/non_login.html',context)
    return render(request, 'Login/non_login.html')

def logout(request):
    auth.logout(request)
    return render(request, 'boeun_bread/main.html')

#회원가입 여부
def is_signup(request):
    if request.method == "POST":
        pass
    return render(request,'SignUp/is_signup.html')
#약관동의

def agreement(request):
    return render(request,'SignUp/agreement.html')
#회원가입
def SignUp(request):
    if request.method == "POST":
        if not request.POST.get('is_check'):
            if not User.objects.filter(username=request.POST.get('user_id')):
                email_text = request.POST.get('email_text')
                email_select = request.POST.get('email_select')
                user_email = email_text+'@'+email_select

                user = User.objects.create_user(
                    username = request.POST.get('user_id'),
                    password = request.POST.get('user_pwd'),

                )
                profile = Profile.objects.create(
                    user    = user,
                    U_phone = request.POST.get('user_phone'),
                    U_name  = request.POST.get('user_name'),
                    U_email = user_email
                )
                profile.U_is_active = False

                return redirect('/SignUp/cert/'+str(profile.pk))
    else:
        if not request.POST.get('is_check'):#이용약관 동의 하지 않으면 이용약관 페이지 이동
            return redirect('/agreement')

    return render(request,'SignUp/SignUp.html')
#회원가입 > 본인인증
def certification(request,pk):
    profile = get_object_or_404(Profile,pk=pk)

    if request.method == "POST":
        pass
    context={
        'profile_pk':profile.pk,
        'email':profile.U_email
    }
    return render(request, 'SignUp/certification.html',context)
#이메일 전송
def send_email(request):
    profile=get_object_or_404(Profile,pk=request.POST['profile_pk'])
    if request.method == "POST":

        current_site = get_current_site(request)
        # localhost:8000
        message = render_to_string('SignUp/user_active.html', {
                'user': profile,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(profile.pk)),
                'token': account_activation_token.make_token(profile),
        })
        mail_subject = "[보은] 회원가입 인증 메일입니다."

        email = EmailMessage(mail_subject, message, to=[profile.U_email])
        email.send()
        context = {
            'success':True
        }
        return HttpResponse(json.dumps(context), content_type="application/json")

def LoginPage(request):
    if request.method == "POST":
        context={}
        user = auth.authenticate(request,username=request.POST['user_id'],password=request.POST['user_pwd'],U_delete=False)
        if user:
            if not user.profile.U_is_active:
                context['msg']="이메일 인증이 완료되지 않았습니다."
            else:
                auth.login(request,user)
                return redirect('/')
            #Profile.objects.get(user=request.user)
        else:
            context['msg'] = "아이디, 비밀번호가 맞지 않습니다."
            return render(request, 'Login/Login.html',context)


        return render(request, 'boeun_bread/main.html',context)
    return redirect('/')

#회원가입 id 중복 체크
def SignUp_idcheck(request):
    id_check = request.POST.get('idcheck')
    UserList = User.objects.filter(username=id_check)
    response = {}
    if not UserList:
        response ={ 'msg' : True}
    else:
        context = {'msg' : False}

    return HttpResponse(json.dumps(response), content_type="application/json")

#이메일
def activate(request, uid64, token):
    uid = force_text(urlsafe_base64_decode(uid64))
    user = Profile.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.U_is_active = True
        user.save()
        return render(request, 'SignUp/signupok.html')
    else:
        return HttpResponse('비정상적인 접근입니다.')

#마이페이지
@login_required
def mypage(request):
    return render(request,'mypage/mypage.html')
#마이페이지 > 개인정보 관리
@login_required
def manage_privacy(request):
    return render(request,'mypage/manage_privacy.html')

#마이페이지 > 개인정보관리 > 회원정보 인증 요청
@login_required
def auth_modify_user(request):
    context = {
        'is_auth':True
    }
    if request.method == "POST":
        user    = auth.authenticate(request,username=request.user.username,password=request.POST.get('user_pw'))
        if user:
            return render(request, 'mypage/modify_user.html')
        context['is_auth'] = False
    return render(request, 'mypage/auth_modify_user.html',context)

#마이페이지 > 개인정보관리 > 회원정보수정
@login_required
def modify_user(request):
    '''
        1. modify_user GET 요청 비활성화
        2. GET 요청 활성화 하면 회원정보수정 인증하지 않고 요청가능
    '''
    if request.method == "POST":
        profile         = Profile.objects.get(user=request.user)
        profile.U_name  = request.POST.get('user_name')
        profile.U_phone = request.POST.get('user_phone')
        profile.save()
        messages.add_message(request, messages.INFO, '회원정보 변경 되었습니다.')
    return redirect('/mypage/modifyAuth')
#마이페이지 > 개인정보관리 > 회원탈퇴
@login_required
def delete_user(request):
    context = {}
    if request.method == "POST":
        user = auth.authenticate(request,username=request.user.username,password=request.POST.get('user_pw'))
        if user:
            for reason in request.POST.getlist('reason'):
                Reason.objects.create(
                user = request.user.profile,
                reason=reason
            )
            user.U_delete=True
            user.save()
            auth.logout(request)
            return redirect('/')
        else:
            context['msg'] = "비밀번호가 일치하지 않습니다."
    return render(request, 'mypage/delete_user.html',context)
#마이페이지 > 개인정보관리 > 비밀번호 변경
def modify_pw(request):
    context = {}
    if request.method == "POST":
        user = auth.authenticate(request,username=request.user.username,password=request.POST.get('current_pw'))
        if user:
            user.set_password(request.POST.get('new_pw'))
            user.save()
            return redirect('/Login')

        context['msg'] = "잘못된 기존비밀번호 입니다."
    return render(request, 'mypage/modify_pw.html',context)

def search_order(request):
    return render(request, 'mypage/search_order.html')

#아이디 찾기
def forget_id(request):
    context = {}
    if request.method == "POST":
        user_name  = request.POST.get('user_name')
        user_phone = request.POST.get('user_phone')
        profile    = Profile.objects.filter(
                        U_name  = user_name,
                        U_phone = user_phone
                    )
        if profile:
            context['user_id'] = profile[0].user.username

        else:
            context['msg']        = "이름 또는 전화번호가 존재하지 않습니다."
            context['user_name']  = user_name
            context['user_phone'] = user_phone
    return render(request,'forget/forget_id.html',context)
#비밀번호 찾기
def forget_pw(request):
    context = {}
    if request.method == "POST":
        user_id    = request.POST.get('user_id')
        user_email = request.POST.get('user_email')
        user       = get_object(
                        User,
                        username         = user_id,
                        profile__U_email = user_email
                     )
        if user:
            password = create_temp_password()
            user.set_password(password)
            user.save()
            email = EmailMessage("임시비밀번호 입니다.", password, to=[user.profile.U_email])
            email.send()
            return redirect("/Login")
        else:
            context['msg']        = "아이디 또는 이메일이 존재하지 않습니다."
            context['user_id']    = user_id
            context['user_email'] = user_email

    return render(request,'forget/forget_pw.html',context)
from random import randint
 #임시 비밀번호 생성
def create_temp_password():
    data = [
        '0','1','2','3','4','5','6','7','8','9',
        'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
        'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
        '?','~','!','@','#','&','(',')'
    ]
    password=""
    for i in range(12):
        password += data[randint(0,len(data)-1)]
    return password

def order_history(request):
    return render(request, 'mypage/order_history.html')

#주문배송조회
@login_required
def order_lookup(request):

    order = Order.objects.filter(User=request.user.profile)

    #Pagination
    page = request.GET.get('page',1)
    paginator = Paginator(order,5)
    posts = paginator.get_page(page)

    return render(request, 'mypage/order_lookup.html', {'order':posts, 'posts':posts})

#주문 배송 조회 날짜 검색
def order_lookup_info(request):

    result = None

    profile =  request.user.profile if request.user.is_authenticated else None
    if not profile:
        cookie_id = request.COOKIES.get('cookie_id')
        profile   = get_object(Profile,cookie_id=cookie_id,U_grade=2)
    else:
        copy_product(request)

    if request.POST.get('type') == "1":
        today = datetime.today()
        result = Order.objects.filter(User=profile,Order_date__year=today.year, Order_date__month=today.month, Order_date__day=today.day)

    elif request.POST.get('type') == "2":

        before_day = datetime.now() + timedelta(days=-7)

        today =  str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str( datetime.today().day)

        result = Order.objects.filter(User=profile,Order_date__range=[before_day,today])

    elif request.POST.get('type') == "3":
        today = datetime.today()
        result = Order.objects.filter(User=profile,Order_date__year=today.year, Order_date__month=today.month)

    elif request.POST.get('type') == "4":
        today = datetime.today()
        month = today.month
        if today.month == 1:
            month = 12
        else:
            month = (today.month-1)
            result = Order.objects.filter(User=profile,Order_date__year=today.year, Order_date__month=month)

    elif request.POST.get('type') == "5":
        b_date = request.POST.get('befor_date')
        a_date = request.POST.get('after_date')

        result = Order.objects.filter(User=profile,Order_date__range=[b_date,a_date])


    #Pagination
    page = request.GET.get('page',1)
    paginator = Paginator(result,5)
    posts = paginator.get_page(page)

    return render(request, 'mypage/order_lookup_info.html', {'order':posts, 'posts':posts})
#배송 조회 
def tracking(request,order_num):
    order = get_object_or_404(Order,Order_Number=order_num)
    context = {
        'order':order,
    }
    return render(request, 'mypage/tracking.html',context)

#상품복제
def copy_product(request):
    '''
    비회원 장바구니를 회원 장바구니에 복제
    '''
    cookie_id     = request.COOKIES.get('cookie_id')
    profile       = get_object(Profile,cookie_id=cookie_id,U_grade=2) #비회원 profile
    non_user_cart = get_object(Cart,User=profile)#비회원 장바구니
    if non_user_cart: # 비회원 cart object가 있으면 밑 내용 실행
        cart = get_object(Cart,User=request.user.profile) # 회원 장바구니
        if not cart:
            cart = Cart.objects.create(User=request.user.profile) #회원 장바구니 없으면 생성
        non_user_cp   = non_user_cart.CartProduct.all()#비회원 장바구니 모든 상품 가져오기
        for obj in non_user_cp:
            cp = get_object(Cart_Product,Cart=cart,product_id=obj.product_id)
            if cp: # 회원장바구니에 해당 상품 있으면 수량만 +
                cp.product_count = cp.product_count + obj.product_count
                cp.save()
            else: # 회원장바구니에 해당 상품 없으면 장바구니 상품 생성
                Cart_Product.objects.create(
                    Cart          = cart,
                    product_id    = obj.product_id,
                    product_img   = obj.product_img,
                    product_name  = obj.product_name,
                    product_price = obj.product_price,
                    product_count = obj.product_count
                )
        non_user_cp.delete() # 비회원 장바구니 모든 상품 삭제




#장바구니
def cart(request):

    profile =  request.user.profile if request.user.is_authenticated else None
    if not profile:
        cookie_id = request.COOKIES.get('cookie_id')
        profile   = get_object(Profile,cookie_id=cookie_id,U_grade=2)
    else:
        copy_product(request)

    cart = get_object(Cart,User=profile)
    cp   = Cart_Product.objects.filter(Cart=cart)
    return render(request, 'cart/cart.html',{'cp':cp,'cart':cart})

#장바구니 담기
def add_cart(request,pk,count):
    product = get_object_or_404(Product,pk=pk)
    response  = HttpResponse("success")
    profile = None
    #회원일 경우
    if request.user.username:
        profile = request.user.profile

    else:
        cookie_id = request.COOKIES.get('cookie_id')

        if not cookie_id:
            response,cookie_id = add_cookie(response)
        else:
            profile = get_object(Profile, cookie_id=cookie_id)

        if not profile:
            profile = Profile.objects.create(cookie_id=cookie_id)

    cart = get_object(Cart,User=profile)
    if not cart:
        cart = Cart.objects.create(User=profile)

    cp = get_object(Cart_Product,Cart=cart,product_id=product.pk)
    if not cp:
        Cart_Product.objects.create(
            Cart          = cart,
            product_id    = product.pk,
            product_img   = product.P_img,
            product_name  = product.P_name,
            product_price =  product.P_price,
            product_count = count
        )
    else:
        cnt = cp.product_count + int(count)
        cp.product_count = cnt
        cp.save()
    return response
#장바구니 상품삭제
def del_cart(request,pk):
    cp = get_object_or_404(Cart_Product,pk=pk)
    cp.delete()
    return HttpResponse("success")
#최근 배송지 정보 JSON 응답
def recently_info(request):

    cookie_id = request.COOKIES.get('cookie_id')
    profile   = get_object(Profile,cookie_id=cookie_id)
    if request.user.is_authenticated:
        profile = request.user.profile
    order    = Order.objects.filter(User=profile).last() #order에서 마직막 object 가져오기, 마지막 == 최근
    response = None
    if order:
        response = {
            'addr' : order.User_address,
            'detail_addr':order.User_detail_address,
            'request_content' : order.Order_request_content

        }
    return HttpResponse(json.dumps(response), content_type="application/json")



#쿠키추가
def add_cookie(response):
    now     = datetime.now()
    max_age = 365*24*60*60

    value = str(now.year)+str(now.month)+\
            str(now.day)+str(now.hour)+\
            str(now.minute)+str(now.second)+str(now.microsecond)
    cookie_id = format(int(value),"#x")
    response.set_cookie('cookie_id',cookie_id,max_age)
    return response,cookie_id

# 각 상품종류 개수 반환
def classfy_product_count():
    count = ""
    count += str(len(Product.objects.filter(P_kind='1')))+","
    count += str(len(Product.objects.filter(P_kind='2')))+","
    count += str(len(Product.objects.filter(P_kind='3')))
    return count

#주문하기
def order(request,path):
    '''
     type:1 -> 제빵
     type:2 -> 제과
     type:3 -> 선물세트
    '''
    product  = None
    type_num = None
    if path == "baking":
        product = Product.objects.filter(P_kind='1')
        type_num=1
    elif path == "confectionery":
        product = Product.objects.filter(P_kind='2')
        type_num=2
    elif path == "giftset":
        product = Product.objects.filter(P_kind='3')
        type_num=3
    else:
        raise Http404
    context={
        'product':product,
        'type' : type_num,
        'count':classfy_product_count()
    }
    return render(request, 'boeun_bread/order.html',context)



#주문 detail 페이지
def order_detail(request,pk):
    prod = get_object_or_404(Product,pk=pk)

    return render(request, 'boeun_bread/order_detail.html',{'prod':prod})

def Before_payment(request):

    user = None

    if request.user.is_authenticated:
        user = request.user.profile
    else:
        cookie_id = request.COOKIES.get('cookie_id')
        user = get_object(Profile, cookie_id=cookie_id)

        user.U_phone = request.POST.get('phone')
        user.U_name = request.POST.get('name')
        user.U_email = request.POST.get('email')

        user.save()

    total = 0
    cart = get_object(Cart,pk=request.POST.get('cart_pk'))
    if cart:
        total = cart.get_total() + 3000 # 배송비 3000원

    order = Order.objects.create(
        User                  = user,
        Order_Number          = str(create_order_number()),
        User_address          = request.POST.get('addr'),
        User_detail_address   = request.POST.get('detail-addr'),
        Total_price           = total,
        Order_hope_date       = request.POST.get('hopeday'),
        Order_request_content = request.POST.get('request_content'),
    )

    m_cart = get_object(Cart, User=user)
    for prod_pk in request.POST.getlist('prod_pk'):
        product = get_object(Product, pk=prod_pk)
        cp = get_object(Cart_Product,Cart=m_cart,product_id=product.pk)
        print(cp)
        Order_Product.objects.create(
            Order = order,
            product_id = product.pk,
            product_img = product.P_img,
            product_name = product.P_name,
            product_price = product.P_price,
            product_count = cp.product_count,
        )

    return redirect('/payment_page/' + order.Order_Number)


#주문하기
def payment_result(request):


    order = get_object(Order,Order_Number=request.POST.get('Order_Number'))

    cart = get_object(Cart, User=order.User)


    order.Order_status = True
    order.save()

    for porduct in Order_Product.objects.filter(Order=order):
        Product.objects.filter(pk=porduct.product_id).update(
            P_sales=F('P_sales')+ porduct.product_count
        )

    Cart_Product.objects.filter(Cart=cart).delete()
    return HttpResponse("success")
#결제 금액 가제오기
from django.http import Http404
def get_total(request):
    context = {
        'total':0
    }
    if request.method == "POST":
        cart = get_object(Cart,pk=request.POST.get('cart_pk'))
        if cart:
            context['total'] = cart.get_total() + 3000 # 배송비 3000원
    else:
        raise Http404
    return HttpResponse(json.dumps(context), content_type="application/json")

#결제 최종페이지
def payment_page(request, ordernumber):

    profile =  request.user.profile if request.user.is_authenticated else None
    if not profile:
        cookie_id = request.COOKIES.get('cookie_id')
        profile   = get_object(Profile,cookie_id=cookie_id,U_grade=2)
    else:
        copy_product(request)

    order = get_object(Order,User=profile, Order_Number=ordernumber)

    cart = get_object(Cart,User=profile)

    cp   = Cart_Product.objects.filter(Cart=cart)


    return render(request,'cart/payment_page.html',{'cp':cp,'cart':cart, 'order':order})

#주문번호 생성
def create_order_number():
    now   = datetime.now()
    date  = str(now.year)+str(now.month)+str(now.day)
    value = str(now.hour)+str(now.minute)+str(now.second)+str(now.microsecond)
    return date+"_"+format(int(value), 'o')


#본빵이야기
def Bread_Birth(request):
    return render(request,'boeun_bread_story/birth.html')

def bread_logo_story(request):
    return render(request,'boeun_bread_story/logo_story.html')

def boeun_jujube_story(request):
    return render(request,'boeun_bread_story/boeun_jujube_story.html')



#추천베스트
def boeun_best(request,keyword):
    product = None
    kind    = None

    if keyword == "all":
        product = Product.objects.all()
        kind    = 0
    elif keyword == "baking":
        product = Product.objects.filter(P_kind='1')
        kind    = 1
    elif keyword == "confectionery":
        product = Product.objects.filter(P_kind='2')
        kind    = 2
    elif keyword == "giftset":
        product = Product.objects.filter(P_kind='3')
        kind    = 3
    else:
        raise Http404

    '''
        1. 상품 판매량 기준 정렬
        2. 판매량 동일하면 최신 등록순 정렬
    '''
    product = product.order_by('-P_sales','-id')

    context = {
        'first_prod':product[0:1], # 1위 빵 object
        'second_prod_list':product[1:5], #2-5위 빵 queryset
        'third_prod_list':product[5:],   # 나머지 빵 queryset
        'kind':kind
    }

    return render(request,'boeun_bread/boeun_best.html',context)

#고객센터
def Service_center(request):
    return render(request,'boeun_bread/Service_center.html')

#공지사항 리스트
def notice_list(request):
    board = Board.objects.all().order_by('-id')
    #Pagination

    page      = request.GET.get('page',1)
    paginator = Paginator(board,10)
    posts     = paginator.get_page(page)
    '''
    type:1 -> 공지사항
    type:2 -> qna
    '''
    context = {
        'board':posts,
        'posts':posts,
        'type':'1'
    }
    return render(request,'boeun_bread/notice_list.html',context)
#공지사항 상세
def notice_detail(request,page):
    board = get_object_or_404(Board,pk=page)
    board.hit = board.hit + 1
    board.save()
    files = board.boardfile_set.all()
    context = {
        'board':board,
        'files':files

    }
    return render(request,'boeun_bread/notice_detail.html',context)
#공지사항 수정
def modify_notice(request,page):
    board = get_object_or_404(Board,id=page)
    if request.method == "POST":
        
        if board.user == request.user.profile:
            files     = request.FILES.getlist('file')
            pre_files = request.POST.get('pre_exclude_file')
            pre_files = pre_files.split(',')
            '''
                client 삭제된 리스트로
                client 삭제된 파일 제외
            '''
            
            for index in request.POST.getlist('exclude_file'):
                try:
                    del files[int(index)]
                except ValueError:
                    pass
            for index in pre_files:
                try:
                    obj = get_object(BoardFile,id=index)
                    if obj:
                        obj.delete()
                except ValueError:
                    pass        
                

            board.title   = request.POST.get('title')
            board.content = request.POST.get('content')
            board.save()
            for f in files:
                BoardFile.objects.create(
                    board = board,
                    file  = f
                )

        return redirect('/Service_center/NoticeDetail/'+page)
    files = BoardFile.objects.filter(board=board)    
    context = {
        'board':board,
        'files':files
    }
    return render(request,'boeun_bread/modify_notice.html',context)
#공지사항 삭제
def delete_notice(request,page):

    board = get_object_or_404(Board,id=page)
    if board.user == request.user.profile:
        board.delete()
    return redirect('/Service_center/NoticeList/')
#qna리스트
def qna_list(request):
    myQna = request.GET.get('myQna')
    qna   = None
    if myQna == '1':
        if request.user.is_authenticated:
            qna = QNA.objects.filter(user=request.user.profile)
        else:
            return redirect('/mypage/')
    elif not myQna :
        qna = QNA.objects.all().order_by('-id')
    else:
        raise Http404

    #Pagination
    page = request.GET.get('page',1)
    paginator = Paginator(qna,10)
    posts = paginator.get_page(page)
    '''
    type:1 -> 공지사항
    type:2 -> qna
    '''
    context={
        'qna' :posts,
        'posts':posts,
        'type':'2'
    }
    return render(request,'boeun_bread/qna_list.html',context)

#qna쓰기
@login_required
def qna_write(request):
    if request.method == "POST":
        is_private = False
        if request.POST.get('private') == "on":
            is_private = True

        QNA.objects.create(
            user           = request.user.profile,
            question_title = request.POST.get('title'),
            question_content = request.POST.get('content'),
            question_kind  = request.POST.get('kind'),
            is_private     = is_private
        )
        return redirect('/Service_center/QnaList/')
    return render(request,'boeun_bread/write_qna.html')
#qna 수정
@login_required
def qna_modify(request,page):
    qna = get_object_or_404(QNA,id=page)
    if qna.user == request.user.profile:
        if request.method == "POST":

            qna.question_title   = request.POST.get('title')
            qna.question_content = request.POST.get('content')
            qna.question_kind        = request.POST.get('kind')
            qna.save()
            return redirect('/Service_center/QnaList/')
        return render(request,'boeun_bread/modify_qna.html',{'qna':qna})

    return redirect('/Service_center/QnaDetail/'+qna_pk)

#qna상세
def qna_detail(request,page):
    qna = get_object_or_404(QNA,pk=page)
    context = {
        'qna':qna
    }
    return render(request,'boeun_bread/detail_qna.html',context)
#qna 삭제
@login_required
def delete_qna(request,page):
    qna = get_object_or_404(QNA,id=page)
    if qna.user == request.user.profile:
        qna.delete()

    return redirect("/Service_center/QnaList/")

#qna 답변 작성
@login_required
def write_answer(request):

    if request.method == "POST":
        if isAdmin(request):# 관리자만 답변 작성가능
            qna_pk = request.POST.get('qna_pk')
            qna    = get_object(QNA,id=qna_pk)

            if qna:
                if not qna.question_status: #최초 답변 작성할때
                    Answer.objects.create(
                        qna = qna,
                        answer=request.POST.get('answer')
                    )
                    qna.question_status=True
                    qna.save()
                else: # 작성한 답변 수정할때
                    answer = get_object(Answer,qna=qna)
                    answer.answer = request.POST.get('answer')
                    answer.save()

            return redirect('/Service_center/QnaDetail/'+qna_pk)
    raise Http404
#공지 및 qna 검색
def search_result(request):
    type1 = request.GET.get('type')
    query = request.GET.get('query')
    if type1 == '1':
        query_set = Board.objects.filter(
                        Q(title__icontains=query) |
                        Q(content__icontains=query) |
                        Q(user__U_name__icontains=query)
                    )
        page      = request.GET.get('page',1)
        paginator = Paginator(query_set,2)
        posts     = paginator.get_page(page)
        context   = {
            'board' :posts,
            'posts':posts,
            'type':'1',
            'query':query,
        }
        return render(request,'boeun_bread/notice_list.html',context)
    elif type1 == '2':
        query_set = QNA.objects.filter(
                        Q(question_title__icontains=query) |
                        Q(question_content__icontains=query) |
                        Q(user__U_name__icontains=query)
                    ).order_by('-id')

        #Pagination

        page      = request.GET.get('page',1)
        paginator = Paginator(query_set,2)
        posts     = paginator.get_page(page)
        context   = {
            'qna' :posts,
            'posts':posts,
            'type':'2',
            'query':query,

        }
        return render(request,'boeun_bread/qna_list.html',context)
    else:
        raise Http404

#찾아오시는 길
def boeun_map(request):
    return render(request,'boeun_bread/boeun_map.html')
#이용약관
def terms_and_conditions(request):
    return render(request, 'mypage/terms_and_conditions.html')
#개인정보처리방침
def Privacy_Policy(request):
    return render(request, 'mypage/Privacy_Policy.html')
#견적서
def estimate(request,order_num):
    
    order = get_object_or_404(Order,Order_Number=order_num)
    order_product = None
    total = 0
    if order:
        order_product = Order_Product.objects.filter(
            Order=order
        )
        for prod in order_product:
            total += (prod.product_price * prod.product_count)
    context = {
        'order_product':order_product,
        'total':total
    }
    
    return render(request,'Estimate/estimate.html',context)
    
