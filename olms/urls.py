from django.contrib import admin
from . import views
from app import user_login
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include




urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.Base,name="base"),
    path('404/', views.PAGE_NOT_FOUND,name="404"),
    path('', views.Home, name="home"),
    path('about_us/', views.About, name="about_us"),
    path('contact_us/', views.Contact, name="contact_us"),
    path('courses/', views.Single_Course, name="single_course"),
    path('course/<slug:slug>',views.COURSE_DETAILS,name="course_details"),
    path('product/filter-data',views.filter_data,name="filter-data"),
    path('search',views.SEARCH_COURSE,name='search_course'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', user_login.Register, name="register"),
    path('dologin/', user_login.Dologin, name="dologin"),
    path('checkout/<slug:slug>', views.CHECKOUT, name="checkout"),
    path('checkout/<slug:slug>', views.CHECKOUT, name='checkout'),
    path('my_course/', views.MY_COURSE, name='my_course'),
    path('verify_payment', views.VERIFY_PAYMENT, name='verify_payment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)