from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User # 회원가입
from django.contrib import auth #로그

def main(request):
    return render(request,'boeun_bread/main.html')


#로그인
def Login(request):
    return render(request, 'Login/Login.html')

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
        Profile.objects.create(
            user=user,
            U_phone = request.POST['user_phone'],
    )
        return render(request,'boeun_bread/main.html')

    return render(request,'SignUp/SignUp.html')

def LoginPage(request):
    if request.method == "POST":
        user = auth.authenticate(request,username=request.POST['user_id'],password=request.POST['user_pwd'])
        if user:
            auth.login(request,user)
            #Profile.objects.get(user=request.user)

            return render(request,'Login/LoginPage.html')
        else:
            return render(request, 'boeun_bread/main.html')





#본빵이야기
def Bread_Birth(request):
    return render(request,'boeun_bread_story/birth.html')
