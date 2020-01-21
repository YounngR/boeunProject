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

        email_text = request.POST['email_text']
        email_select = request.POST['email_select']
        user_email = email_text+'@'+email_select

        user = User.objects.create_user(
            username = request.POST['user_id'],
            password = request.POST['user_pwd'],
            email = user_email
        )
        profile = Profile.objects.create(
            user=user,
            U_phone = request.POST['user_phone'],
            U_name  = request.POST['user_name']

        )
        profile.U_is_active = False
        # current_site = get_current_site(request)
        # # localhost:8000
        # message = render_to_string('SignUp/user_active.html', {
        #         'user': profile,
        #         'domain': current_site.domain,
        #         'uid': urlsafe_base64_encode(force_bytes(profile.pk)),
        #         'token': account_activation_token.make_token(profile),
        # })
        # mail_subject = "[보은] 회원가입 인증 메일입니다."
        # email = user_email
        # email = EmailMessage(mail_subject, message, to=[user_email])
        # email.send()
        
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
    id_check = request.POST['idcheck']
    UserList = User.objects.filter(username=id_check)
    if not UserList:
        context ={ 'msg' : '사용가능한 아이디입니다.'}
    else:
        context = {'msg' : '이미 사용하고 있는 아이디입니다.'}

    return render(request,'SignUp/SignUp.html')

#이메일
def activate(request, uid64, token):
    uid = force_text(urlsafe_base64_decode(uid64))
    user = Profile.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.U_is_active = True
        user.save()
        return redirect('boeun_bread:SignUpGo')
    else:
        return HttpResponse('비정상적인 접근입니다.')

#회원가입 완료 페이지
def SignUpGo(request):
    return render(request, 'SignUp/signupok.html')


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
