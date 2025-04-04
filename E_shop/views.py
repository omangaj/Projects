from django.shortcuts import render,redirect,HttpResponse
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from cart.cart import Cart
from django.shortcuts import get_object_or_404
from app.models import Cart
from django.views.decorators.csrf import csrf_exempt

import razorpay
from django.conf import settings
from time import time



client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))

def Master(request):
    cart = Cart.objects.filter(user=request.user).first()
    cartitem = CartItem.objects.filter(cart=cart) if cart else []
    context={
        "cart":cart,
        "cartitem":cartitem,
    }

    return render(request, "master.html",context)

@csrf_exempt
def Index(request):
    category = Categories.objects.all()
    brand = Brand.objects.all()
    categoryID = request.GET.get('category')
    brandID = request.GET.get('brand')

    if brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    elif categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')
    else:
        product=Product.objects.all()
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        cartitem=CartItem.objects.filter(cart=cart[0])

        context = {
            "category": category,
            "product": product,
            "brand": brand,
            "cartitem":cartitem
        }
    else:
        context = {
            "category": category,
            "product": product,
            "brand": brand,

        }
    return render(request, "index.html", context)

def Signup(request):
    if request.method == 'POST':
        form= UserCreateForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            new_user=authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request,new_user)
            return redirect('index')
    else:
        form=UserCreateForm()

    context={
        "form": form,
    }
    return render(request,"registration/signup.html", context)

def Logout(request):
    logout(request)
    return redirect('index')

#cart
@login_required(login_url="/users/login")
def cart_add(request, id):
    product = get_object_or_404(Product, id=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("index")

@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart.objects.get(user=request.user)
    CartItem.objects.filter(id=id).delete()
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart.objects.get(user=request.user)
    CartItem.objects.all().delete()
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).first()
    cartitem=CartItem.objects.filter(cart=cart)
    total = float(sum(item.product.price * item.quantity for item in cartitem))
    sub_total= sum(0 + item.quantity for item in cartitem)
    context={
        "cart":cart,
        "cartitem":cartitem,
        "total":total,
        "sub_total":sub_total
    }
    return render(request, 'cart/cart_detail.html', context)


def Contact(request):
    if request.method=="POST":
        contact=Contact_us(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            message = request.POST.get('message'),
            subject = request.POST.get('subject'),
        )
        contact.save()

    contact = Contact_info.objects.all()
    link = Links.objects.all()
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        cartitem = CartItem.objects.filter(cart=cart[0])
        context={
            "contact": contact,
            "link": link,
            'cartitem':cartitem,
        }
    else:
        context = {
            "contact": contact,
        "link": link
        }
    return render(request, 'contact_us.html', context)

def User_detail(request):
    User=get_user_model()
    user=User.objects.filter(username=request.user)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        cartitem = CartItem.objects.filter(cart=cart[0])
        context={
            'cartitem':cartitem,
        }


    if request.method == "POST":
        user = request.POST.get("username")
        user_instance=User.objects.filter(username=user)
        print("user_instance==================================",user_instance)
        user=User_info(
            user=user_instance[0],
            name=request.POST.get("name"),
            surname=request.POST.get("surname"),
            email=request.POST.get("email"),
            mobile=request.POST.get("mobile"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            sub_district=request.POST.get("sub_district"),
            district=request.POST.get("district"),
            state=request.POST.get("state"),
            pincode=request.POST.get("pincode"),
        )
        user.save()
        print("user================================", user)
        return redirect("index")
    return render(request,"user/user_info.html",context)


def Checkout(request):
    action = request.GET.get('action')
    cart = Cart.objects.filter(user=request.user).first()
    cartitem = CartItem.objects.filter(cart=cart)
    total = float(sum(item.product.price * item.quantity for item in cartitem))
    sub_total = sum(0 + item.quantity for item in cartitem)
    amount = total * 100
    address = User_info.objects.filter(user=request.user)




    receipt= f"E_shopper-{int(time())}"
    payment = client.order.create({
        "amount": amount,
        "receipt":receipt,
        "currency": "INR",
        "payment_capture": "1"
    })

    print("payment==================================================",payment)



    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        cartitem = CartItem.objects.filter(cart=cart[0])
        context={
            "cartitem": cartitem,
            "total": total,
            "sub_total": sub_total,
            "address":address,
            "payment":payment
        }

    if request.method=="POST" and action == 'create_payment':
        user_info = request.POST.get("username")
        print("user_info=========================================================", user_info)
        user_instance = User_info.objects.filter(address=user_info)
        print("user_instance=========================================================",user_instance)

        for cart in cartitem:
            pro_total = int(cart.product.price) * int(cart.quantity)
            order=Order(
                user = request.user,
                user_info = user_instance[0],
                order_id = payment["id"],
                image = cart.product.image,
                product = cart.product.name,
                quantity = cart.quantity,
                price = cart.product.price,
                pro_total = pro_total,
            )
            order.save()
        cart = Cart.objects.filter(user=request.user).first()
        CartItem.objects.filter(cart=cart).delete()
        return redirect("index")


    return render(request,"order/checkout.html",context)

# def Place_order(request):
#     cart = Cart.objects.filter(user=request.user).first()
#     cartitem = CartItem.objects.filter(cart=cart)
#     total = float(sum(item.product.price * item.quantity for item in cartitem))
#     amount = total * 100
#     sub_total = sum(0 + item.quantity for item in cartitem)
#
#     if not cartitem.exists():
#         return redirect("index")
#
#     payment = client.order.create({
#         "amount": amount,
#         "currency": "INR",
#         "payment_capture": "1"
#     })
#     order_id = payment["id"]
#     currency = payment['currency']
#
#     user=User_info.objects.all()
#
#     if request.user.is_authenticated:
#         cart = Cart.objects.filter(user=request.user)
#         cartitem = CartItem.objects.filter(cart=cart[0])
#         context={
#             "payment": payment,
#             "currency": currency,
#             "order_id": order_id,
#             "cartitem": cartitem,
#             "total": total,
#             "sub_total": sub_total,
#             "user": user
#         }
#     else:
#         context = {
#             "payment": payment,
#             "currency": currency,
#             "order_id": order_id,
#             "total": total,
#             "sub_total": sub_total,
#             "user": user
#         }
#
#     return render(request,"order/place_order.html",context)
def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    order=Order.objects.filter(user=user).order_by('-id')
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        cartitem = CartItem.objects.filter(cart=cart[0])
        context={
            'order':order,
            'cartitem':cartitem,
        }
    else:
        context = {
            'order': order,
        }
    return render(request,'order/order.html',context)


def Product_page(request):
    category = Categories.objects.all()
    brand = Brand.objects.all()
    categoryID = request.GET.get('category')
    brandID = request.GET.get('brand')

    if brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    elif categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')
    else:
        product = Product.objects.all()


    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        cartitem = CartItem.objects.filter(cart=cart[0])
        context = {
            "category": category,
            "product": product,
            "brand": brand,
            "cartitem":cartitem
        }
    else:
        context = {
            "category": category,
            "product": product,
            "brand": brand
        }
    return render(request,'product.html',context)

def Product_detail(request,id):
    product=Product.objects.get(id=id)
    category = Categories.objects.all()
    brand = Brand.objects.all()
    categoryID = request.GET.get('category')
    brandID = request.GET.get('brand')

    if brandID:
        prod = Product.objects.filter(brand=brandID).order_by('-id')
    elif categoryID:
        prod = Product.objects.filter(sub_category=categoryID).order_by('-id')
    else:
        prod = Product.objects.all()
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        cartitem = CartItem.objects.filter(cart=cart[0])
        context = {
            "category": category,
            "product": product,
            "prod": prod,
            "brand": brand,
            "cartitem":cartitem
        }
    else:
        context = {
            "category": category,
            "product": product,
            "prod": prod,
            "brand": brand
        }
    return render(request,'product_details.html',context)

def Search(request):
    query=request.GET['query']
    product=Product.objects.filter(name__icontains=query)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        cartitem = CartItem.objects.filter(cart=cart[0])
        context = {
            "product":product,
            "cartitem":cartitem
        }
    else:
        context = {
            "product":product
        }
    return render(request,'search.html',context)

