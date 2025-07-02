from django.urls import path,include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home,name="home"),

    #registration
    path('signup/', views.Signup, name="signup"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/',views.Logout,name='logout'),

    #profile
    path('profile/',views.Profile,name="profile"),
    path('address/',views.Address,name="address"),

    #product
    path("product_detail/<int:pk>/",views.Product_detail,name="product_detail"),
    path("deal_product/<int:id>/",views.Deal_product,name="deal_product"),

    #search
    path('search/', views.Search, name='search'),
    # cart
    path('cart/add/<int:id>,<str:field>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),

    #checkout
    path('checkout/',views.Checkout,name="checkout"),
    path('buy/<int:id>,<str:field>/',views.Buy_now,name="buy"),

    #payment
    path('verify_payment/',views.Verify_payment,name='verify_payment'),
    path('payment_success/',views.Success,name='payment_success'),
    path('payment_failed/',views.Failed,name='payment_failed'),

    #order
    path('order_product/', views.Order_product, name='order_product'),

    # path('changepassword/', views.change_password, name='changepassword'),
    # path('mobile/', views.mobile, name='mobile'),
    # path('registration/', views.customerregistration, name='customerregistration'),
    # path('checkout/', views.checkout, name='checkout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
