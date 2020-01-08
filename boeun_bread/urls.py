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
    path('/bread_birth', views.Bread_Birth, name="Bread_Birth"),
]
