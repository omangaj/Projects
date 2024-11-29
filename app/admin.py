from django.contrib import admin
from .models import *

class What_you_learn_TabularInline(admin.TabularInline):
    model = What_you_learn

class Requirement_TabularInline(admin.TabularInline):
    model = Requirement

class Video_TabularInline(admin.TabularInline):
    model = Video

class Courseline(admin.ModelAdmin):
    inlines= (What_you_learn_TabularInline,Requirement_TabularInline,Video_TabularInline)

# Register your models here.

admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course,Courseline)
admin.site.register(Level)
admin.site.register(Language)
admin.site.register(What_you_learn)
admin.site.register(Requirement)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(UserCourse)
admin.site.register(Payment)