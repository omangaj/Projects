from django.contrib import admin
from .models import *
from tinymce.widgets import TinyMCE
from django.db import models

class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


# Register your models here.
admin.site.register(Contact_info)
admin.site.register(Links)
admin.site.register(Categories)
admin.site.register(Sub_categories)
admin.site.register(Brand)
admin.site.register(Product, MyModelAdmin)
admin.site.register(Contact_us)
admin.site.register(Order)

