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
from django.core.mail import EmailMessage
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User # 회원가입
from django.contrib import auth #로그
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime
from django.db.models import Sum

#객체 반환
def get_object(model,**args):
    query_set = model.objects.filter(**args)
    return query_set[0] if query_set else None


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
        return render(request,'boeun_bread/main.html',{'msg':'권한 없습니다.'})

    return render(request,'manage/manage_main.html')

#상품등록
@login_required
def create_product(request):
    if not isAdmin(request):
        return render(request,'boeun_bread/main.html',{'msg':'권한 없습니다.'})
    if request.method == "POST":
        is_new = True if request.POST.get('is_new')=="on" else False

        Product.objects.create(
            P_img        = request.FILES.get('bread_img'),
            P_name       = request.POST.get('bread_name'),
            P_price      = request.POST.get('bread_price'),
            P_newProduct = is_new
        )
        return redirect('/manage')
    return render(request,'manage/create_product.html')
#수정상품 리스트
@login_required
def modify_list(request):
    if not isAdmin(request):
        return render(request,'boeun_bread/main.html',{'msg':'권한 없습니다.'})
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
        return render(request,'boeun_bread/main.html',{'msg':'권한 없습니다.'})
    product = getProduct(pk)

    if request.method == "POST":
        is_new = True if request.POST.get('is_new')=="on" else False
        files = request.FILES.get('bread_img')
        if files:
            product.P_img = files
        product.P_name       = request.POST.get('bread_name')
        product.P_price      = request.POST.get('bread_price')
        product.P_newProduct = is_new
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
        return render(request,'boeun_bread/main.html',{'msg':'권한 없습니다.'})
    if request.method == "POST":
        product = Product.objects.filter(id=request.POST.get('pk'))
        if product:
            product[0].delete()
        return redirect('/manage/modify_list')



#end manage

#로그인
def Login(request):

    return render(request, 'Login/Login.html')

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
        if not User.objects.filter(username=request.POST.get('user_id')):
            email_text = request.POST.get('email_text')
            email_select = request.POST.get('email_select')
            user_email = email_text+'@'+email_select

            user = User.objects.create_user(
                username = request.POST.get('user_id'),
                password = request.POST.get('user_pwd'),
                email = user_email
            )
            profile = Profile.objects.create(
                user=user,
                U_phone = request.POST.get('user_phone'),
                U_name  = request.POST.get('user_name')

            )
            profile.U_is_active = False

            return redirect('/SignUp/cert/'+str(profile.pk))

    return render(request,'SignUp/SignUp.html')
#회원가입 > 본인인증
def certification(request,pk):
    profile = get_object_or_404(Profile,pk=pk)

    if request.method == "POST":
        pass
    context={
        'profile_pk':profile.pk,
        'email':profile.user.email
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

        email = EmailMessage(mail_subject, message, to=[profile.user.email])
        email.send()
        context = {
            'success':True
        }
        return HttpResponse(json.dumps(context), content_type="application/json")

def LoginPage(request):
    if request.method == "POST":
        context={}
        user = auth.authenticate(request,username=request.POST['user_id'],password=request.POST['user_pwd'])
        if user:
            if not user.profile.U_is_active:
                context['msg']="이메일 인증이 완료되지 않았습니다."
            else:
                auth.login(request,user)
            #Profile.objects.get(user=request.user)
        else:
            context['msg'] = "로그인을 실패했습니다."

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
        return redirect('boeun_bread:SignUpOk')
    else:
        return HttpResponse('비정상적인 접근입니다.')

#회원가입 완료 페이지
def SignUpOk(request):
    return render(request, 'SignUp/signupok.html')

#마이페이지
def mypage(request):
    return render(request, 'mypage/mypage.html')
def search_order(request):
    return render(request, 'mypage/search_order.html')
def order_history(request):
    return render(request, 'mypage/order_history.html')

#장바구니
def cart(request):
    profile =  request.user.profile if request.user.is_authenticated else None
    if not profile:
        cookie_id = request.COOKIES.get('cookie_id')
        profile   = get_object(Profile,cookie_id=cookie_id,U_grade=2)
        
    cart = get_object(Cart,User=profile)
    cp   = Cart_Product.objects.filter(Cart=cart)
    return render(request, 'cart/cart.html',{'cp':cp})

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
    print(pk)
    cp = get_object_or_404(Cart_Product,pk=pk)
    cp.delete()
    return HttpResponse("success")


def add_cookie(response):
    max_age = 365*24*60*60
    now = datetime.now()
    value = str(now.year)+str(now.month)+\
            str(now.day)+str(now.hour)+\
            str(now.minute)+str(now.second)+str(now.microsecond)
    cookie_id = format(int(value),"#x")
    response.set_cookie('cookie_id',cookie_id,max_age)
    return response,cookie_id

#-----manage
#관리자 이냐?
def isAdmin(request):
    profile = Profile.objects.get(user=request.user)
    return True if profile.U_grade == 0 else False


#관리자 main
@login_required
def manage(request):
    if not isAdmin(request):
        return render(request,'boeun_bread/main.html',{'msg':'권한 없습니다.'})

    return render(request,'manage/manage_main.html')

#상품등록
@login_required
def create_product(request):
    if not isAdmin(request):
        return render(request,'boeun_bread/main.html',{'msg':'권한 없습니다.'})
    if request.method == "POST":
        is_new = True if request.POST.get('is_new')=="on" else False

        Product.objects.create(
            P_img        = request.FILES.get('bread_img'),
            P_name       = request.POST.get('bread_name'),
            P_price      = request.POST.get('bread_price'),
            P_newProduct = is_new
        )
        return redirect('/manage')
    return render(request,'manage/create_product.html')
#수정상품 리스트
@login_required
def modify_list(request):
    if not isAdmin(request):
        return render(request,'boeun_bread/main.html',{'msg':'권한 없습니다.'})
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
        return render(request,'boeun_bread/main.html',{'msg':'권한 없습니다.'})
    product = getProduct(pk)

    if request.method == "POST":
        is_new = True if request.POST.get('is_new')=="on" else False
        files = request.FILES.get('bread_img')
        if files:
            product.P_img = files
        product.P_name       = request.POST.get('bread_name')
        product.P_price      = request.POST.get('bread_price')
        product.P_newProduct = is_new
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
        return render(request,'boeun_bread/main.html',{'msg':'권한 없습니다.'})
    if request.method == "POST":
        product = Product.objects.filter(id=request.POST.get('pk'))
        if product:
            product[0].delete()
        return redirect('/manage/modify_list')



#end manage



#주문하기 페이지
def order(request):
    product = Product.objects.all()
    context={
        'product':product
    }
    return render(request, 'boeun_bread/order.html',context)



#본빵이야기
def Bread_Birth(request):
    return render(request,'boeun_bread_story/birth.html')

def bread_logo_story(request):
    return render(request,'boeun_bread_story/logo_story.html')

def boeun_jujube_story(request):
    return render(request,'boeun_bread_story/boeun_jujube_story.html')


#본빵 배달신청
def boeun_delivery(request):
    return render(request,'boeun_bread/boeun_delivery.html')
#추천베스트
def boeun_best(request):
    return render(request,'boeun_bread/boeun_best.html')
#주문안내
def order_guidance(request):
    return render(request,'boeun_bread/order_guidance.html')

#찾아오시는 길
def boeun_map(request):
    return render(request,'boeun_bread/boeun_map.html')
#견적서
def estimate(request):
    return render(request,'Estimate/estimate.html')    
