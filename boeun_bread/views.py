from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User # 회원가입
from django.contrib import auth #로그
from django.contrib.auth.decorators import login_required

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
            return render(request,'Login/LoginPage.html')
        else:
            return render(request, 'boeun_bread/main.html')

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
