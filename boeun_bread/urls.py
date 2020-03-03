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
    path('manage/manage_Sales_Status/',views.manage_Sales_Status,name="manage_Sales_Status"),
    path('manage/manage_Sales_Status_table/',views.manage_Sales_Status_table,name="manage_Sales_Status_table"),
    path('manage/writeBoard/',views.write_board,name="write_board"),#공지사항 작성
    #end manage
    #주문하기
    path('order/<path>/',views.order,name="order"),
    path('order/detail/<pk>/',views.order_detail,name="orderDetail"),
    path('payment_page',views.payment_page,name="payment_page"),
    #end 주문하기

    #로그인
    path('Login/',views.Login, name="Login"),
    path('non_login/',views.non_login, name="non_login"),
    path('logout/',views.logout, name="logout"),
    #마이페이지
    path('mypage/',views.mypage,name="mypage"),
    path('mypage/managePrivacy',views.manage_privacy,name="manage_privacy"),
    path('mypage/modifyAuth',views.auth_modify_user,name="auth_modify_user"),
    path('mypage/modify/',views.modify_user, name="modify_user"),
    path('mypage/modifyPw/',views.modify_pw, name="modify_pw"),
    path('mypage/delete/',views.delete_user, name="delete_user"),
    path('search_order/',views.search_order, name="search_order"),
    path('order_history/', views.order_history, name="order_history"),
    path('order_lookup/',views.order_lookup, name="order_lookup"),
    path('order_lookup_info', views.order_lookup_info, name="order_lookup_info"),

    #장바구니
    path('cart/',views.cart, name="cart"),
    path('addCart/<pk>/<count>',views.add_cart,name='addCart'),
    path('delCart/<pk>',views.del_cart,name='delCart'),
    path('recentlyInfo/',views.recently_info,name="recently_info"),
    #회원가입
    path('agreement',views.agreement, name="agreement"),
    path('isSignup',views.is_signup,name="is_signup"),
    path('SignUp/',views.SignUp, name="SignUp"),
    #path('SignUpOk/',views.SignUpOk, name="SignUpOk"),
    path('Login/LoginPage',views.LoginPage, name="LoginPage"),
    path('SignUp_idcheck', views.SignUp_idcheck, name='SignUp_idcheck'), #user id 중복 확인
    path('SignUp/cert/<pk>',views.certification,name="cert"),
    path('SignUp/sendEmail',views.send_email,name="sendEmail"),

    #결제
    path('payment_result',views.payment_result,name='payment_result'),

    #찾아오시는 길
    path('boeun_map/',views.boeun_map,name="boeun_map"),

    #이용약관
    path('terms_and_conditions/',views.terms_and_conditions,name="terms_and_conditions"),

    #개인정보처리방침
    path('Privacy_Policy/',views.Privacy_Policy,name="Privacy_Policy"),


    #본빵이야기
    path('bread_birth/', views.Bread_Birth, name="Bread_Birth"),
    path('boeun_logo_story/', views.bread_logo_story, name="bread_logo_story"),
    path('boeun_jujube_story/', views.boeun_jujube_story, name="boeun_jujube_story"),
    #추천베스트
    path('boeun_best/<keyword>/', views.boeun_best, name="boeun_best"),
    #고객센터
    path('Service_center/', views.Service_center, name="Service_center"),
    path('Service_center/NoticeList/', views.notice_list, name="notice_list"),#공지사항 리스트
    path('Service_center/NoticeDetail/<page>/', views.notice_detail, name="notice_detail"),#공지사항 리스트
     #견적서
    path('estimate/',views.estimate,name='estimate'),
    #아이디 찾기
    path('forgetId/',views.forget_id,name="forgetId"),
    #비밀번호찾기
    path('forgetPw/',views.forget_pw,name="forgetPw"),
    #총결제 금액 가져오기
    path('total/',views.get_total,name="total"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
