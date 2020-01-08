from . import views
from django.urls import path

app_name = 'boeun_bread'

urlpatterns = [
    path('',views.main,name="main"),
    path('boeun/Login',views.Login, name="Login"),
    path('boeun/SignUp',views.SignUp, name="SignUp"),
    path('boeun/Login/LoginPage',views.LoginPage, name="LoginPage"),
]
