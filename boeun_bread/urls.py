from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
app_name = 'boeun_bread'

urlpatterns = [
    path('',views.main,name="main"),

    #이메일
    path('activate/<uid64>/<token>', views.activate, name='activate'),

    #manage
    path('manage/',views.manage,name="manage"),
    path('manage/create_product/',views.create_product,name="create_product"),
    path('manage/modify_list/',views.modify_list,name="modify_list"),
    path('manage/modify_product/<pk>/',views.modify_product,name="modify_product"),
    path('manage/delete_product/',views.delete_product,name="delete_product"),
    #end manage
    #주문하기
    path('order/',views.order,name="order"),
    path('order/detail/<pk>/',views.order_detail,name="orderDetail"),
    #end 주문하기
    #로그인
    path('Login/',views.Login, name="Login"),
    path('logout/',views.logout, name="logout"),
    #마이페이지
    path('mypage/modify/',views.modify_user, name="modify_user"),
    path('mypage/delete/',views.delete_user, name="delete_user"),
    path('search_order/',views.search_order, name="search_order"),
    path('order_history/', views.order_history, name="order_history"),
    #장바구니
    path('cart/',views.cart, name="cart"),
    path('addCart/<pk>/<count>',views.add_cart,name='addCart'),
    path('delCart/<pk>',views.del_cart,name='delCart'),
    #회원가입
    path('agreement',views.agreement, name="agreement"),
    path('isSignup',views.is_signup,name="is_signup"),
    path('SignUp/',views.SignUp, name="SignUp"),
    path('SignUpOk/',views.SignUpOk, name="SignUpOk"),
    path('Login/LoginPage',views.LoginPage, name="LoginPage"),
    path('SignUp_idcheck', views.SignUp_idcheck, name='SignUp_idcheck'), #user id 중복 확인
    path('SignUp/cert/<pk>',views.certification,name="cert"),
    path('SignUp/sendEmail',views.send_email,name="sendEmail"),


    #찾아오시는 길
    path('boeun_map/',views.boeun_map,name="boeun_map"),

    #본빵이야기
    path('bread_birth/', views.Bread_Birth, name="Bread_Birth"),
    path('boeun_logo_story/', views.bread_logo_story, name="bread_logo_story"),
    path('boeun_jujube_story/', views.boeun_jujube_story, name="boeun_jujube_story"),
    #추천베스트
    path('boeun_best/', views.boeun_best, name="boeun_best"),
    #고객센터
    path('Service_center/', views.Service_center, name="Service_center"),


     #견적서
    path('estimate/',views.estimate,name='estimate'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
