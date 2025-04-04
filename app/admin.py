from django.contrib import admin
from .models import *
from tinymce.widgets import TinyMCE
from django.db import models

class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


# Register your models here.

class Contact_infoAdmin(admin.ModelAdmin):
    list_display=['id','mobile']
admin.site.register(Contact_info,Contact_infoAdmin)

class LinksAdmin(admin.ModelAdmin):
    list_display=['id','name']
admin.site.register(Links,LinksAdmin)

class Sub_categoriesAdmin(admin.ModelAdmin):
    list_display=['id','name']
admin.site.register(Sub_categories,Sub_categoriesAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display=['id','name']
admin.site.register(Brand,BrandAdmin)


class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name']
class CombinedProductAdmin(ProductAdmin, MyModelAdmin):
    pass

admin.site.register(Product, CombinedProductAdmin)

class Contact_usAdmin(admin.ModelAdmin):
    list_display=['id','name']
admin.site.register(Contact_us,Contact_usAdmin)

class User_infoAdmin(admin.ModelAdmin):
    list_display=['id','user','name']
admin.site.register(User_info,User_infoAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','product']
admin.site.register(Order,OrderAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=['id','user']
admin.site.register(Cart,CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display=['id','product']
admin.site.register(CartItem,CartItemAdmin)

