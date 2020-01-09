from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
app_name = 'boeun_bread'

urlpatterns = [
    path('',views.main,name="main"),
    #manage
    path('manage/',views.manage,name="manage"),
    path('manage/create_product/',views.create_product,name="create_product"),
    path('manage/modify_list/',views.modify_list,name="modify_list"),
    path('manage/modify_product/<pk>/',views.modify_product,name="modify_product"),
    path('manage/delete_product/',views.delete_product,name="delete_product"),
    #end manage
    #주문하기
    path('order/',views.order,name="order"),
    #end 주문하기
    #로그인
    path('Login',views.Login, name="Login"),
    path('SignUp',views.SignUp, name="SignUp"),
    path('Login/LoginPage',views.LoginPage, name="LoginPage"),


    #본빵이야기
    path('bread_birth/', views.Bread_Birth, name="Bread_Birth"),
    path('boeun_logo_story/', views.bread_logo_story, name="bread_logo_story"),
    path('boeun_jujube_story/', views.boeun_jujube_story, name="boeun_jujube_story"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
