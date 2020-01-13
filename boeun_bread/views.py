from django.shortcuts import render, redirect
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

def main(request):
    return render(request,'boeun_bread/main.html')

def Login(request):
                
    return render(request, 'Login/Login.html')

def logout(request):
    auth.logout(request)
    return render(request, 'boeun_bread/main.html')


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
           
        )    
        profile.U_is_active = False
        current_site = get_current_site(request) 
        # localhost:8000
        message = render_to_string('SignUp/user_active.html', {
                'user': profile,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(profile.pk)),
                'token': account_activation_token.make_token(profile),
        })
        mail_subject = "[보은] 회원가입 인증 메일입니다."
        email = user_email
        email = EmailMessage(mail_subject, message, to=[user_email])
        email.send()
        return render(request, 'SignUp/emailcheck.html')

    return render(request,'SignUp/SignUp.html')    

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

    