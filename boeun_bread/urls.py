from . import views
from django.urls import path

app_name = 'boeun_bread'

urlpatterns = [
    path('',views.main,name="main"),

    #로그인
    path('Login',views.Login, name="Login"),
    path('SignUp',views.SignUp, name="SignUp"),
    path('Login/LoginPage',views.LoginPage, name="LoginPage"),


    #본빵이야기
    path('bread_birth/', views.Bread_Birth, name="Bread_Birth"),
    path('boeun_logo_story/', views.bread_logo_story, name="bread_logo_story"),
    path('boeun_jujube_story/', views.boeun_jujube_story, name="boeun_jujube_story"),
]
