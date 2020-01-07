from . import views
from django.urls import path

app_name = 'boeun_bread'

urlpatterns = [
    path('',views.main,name="main"),
]
