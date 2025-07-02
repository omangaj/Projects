from django.contrib import admin
from .models import *
# Register your models here.

class User_infoAdmin(admin.ModelAdmin):
    list_display=['user','name']
admin.site.register(User_info,User_infoAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display=['brand']
admin.site.register(Brand,BrandAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    list_display=['brand','category']
admin.site.register(Categories,CategoriesAdmin)

class One_day_dealAdmin(admin.ModelAdmin):
    list_display=['id','title','field','brand','category']
admin.site.register(One_day_deal,One_day_dealAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','title','field','brand','category']
admin.site.register(Product,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=['user','created_at']
admin.site.register(Cart,CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display=['id','one_day','product']
admin.site.register(CartItem,CartItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=['product']
admin.site.register(Order,OrderAdmin)