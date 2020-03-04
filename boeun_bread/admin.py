from django.contrib import admin

from .models import *
# Register your models here.


admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Cart_Product)
admin.site.register(Order)
admin.site.register(Order_Product)
admin.site.register((Board,BoardFile,QNA,Answer,Delivery))

