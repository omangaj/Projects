from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from cart.cart import Cart
from .models import Cart,Order
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from time import time

from django.shortcuts import redirect
from urllib.parse import urlencode

import razorpay
from django.conf import settings
from time import time
client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))


@csrf_exempt
def home(request):
    cart = Cart.objects.filter(user=request.user).first()
    cartitem = CartItem.objects.filter(cart=cart)
    product=Product.objects.all().order_by('-id')
    one_day=One_day_deal.objects.all().order_by('-id')
    context={
        "product":product,
        "cart": cart,
        "cartitem": cartitem,
        "one_day":one_day,
    }
    return render(request, 'app/home.html',context)

def Profile(request):
    cart = Cart.objects.filter(user=request.user).first()
    cartitem = CartItem.objects.filter(cart=cart)
    next=request.GET.get('next') or request.POST.get('next') or '/'
    context = {
        "cart": cart,
        "cartitem": cartitem,
    }

    User = get_user_model()
    user = User.objects.filter(username=request.user)

    if request.method == 'POST':
        user = request.user
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        village = request.POST.get("village")
        city = request.POST.get("city")
        sub_district = request.POST.get("sub_district")
        district = request.POST.get("district")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")

        user_instance = User.objects.filter(username=user)

        user_info=User_info(
            user=user_instance[0],
            name= name,
            email = email,
            mobile = mobile,
            address = address,
            village = village,
            city = city,
            sub_district = sub_district,
            district = district,
            state = state,
            pincode = pincode,
        )
        user_info.save()
        if next:
            return redirect(next)
        else:
            return redirect("address")
    return render(request,'profile/profile.html',context)

def Address(request):
    cart = Cart.objects.filter(user=request.user).first()
    cartitem = CartItem.objects.filter(cart=cart)
    user_info=User_info.objects.filter(user=request.user).order_by('-id')
    context={
        "user_info":user_info,
        "cart": cart,
        "cartitem": cartitem,
    }
    return render(request,'profile/address.html',context)

@csrf_exempt
def Signup(request):
    cart = Cart.objects.filter(user=request.user).first()
    cartitem = CartItem.objects.filter(cart=cart)
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect('home')
    else:
        form = UserCreateForm()

    context = {
        "form": form,
        "cart": cart,
        "cartitem": cartitem,
    }
    return render(request, "registration/signup.html", context)

@csrf_exempt
def Logout(request):
    logout(request)
    return redirect('login')


def Product_detail(request,pk):
    cart = Cart.objects.filter(user=request.user).first()
    cartitem = CartItem.objects.filter(cart=cart)
    product=Product.objects.get(pk=pk)
    products=Product.objects.all()

    context={
        "product":product,
        "products":products,
        "cart": cart,
        "cartitem": cartitem,
    }
    return render(request, 'app/product_detail.html', context)

def Deal_product(request,id):
    cart = Cart.objects.filter(user=request.user).first()
    cartitem = CartItem.objects.filter(cart=cart)
    one_day = One_day_deal.objects.get(id=id)

    context={
        "one_day":one_day,
        "cart": cart,
        "cartitem": cartitem,
    }
    return render(request, 'app/product_detail.html', context)

def Search(request):
    query=request.GET['query']
    product=Product.objects.filter(title__icontains=query)
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
    return render(request,'search/search.html',context)

#cart
@login_required(login_url="/users/login")
def cart_add(request, id,field):
    if field=="one_day":
        one_day = get_object_or_404(One_day_deal, id=id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, one_day=one_day)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        product = get_object_or_404(Product, id=id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart.objects.get(user=request.user)
    CartItem.objects.filter(id=id).delete()
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_increment(request, id):
    cartitem = CartItem.objects.get(id=id)
    if id == cartitem.id:
        if cartitem.quantity >= 1:
            cartitem.quantity += 1
            cartitem.save()
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cartitem=CartItem.objects.get(id=id)
    if id == cartitem.id:
        if cartitem.quantity > 1:
            cartitem.quantity -= 1
            cartitem.save()
        else:
            item_clear(request,id)

    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart.objects.get(user=request.user)
    CartItem.objects.all().delete()
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).first()
    cartitem = CartItem.objects.filter(cart=cart)

    # Handle product and one_day separately
    product_items = [item for item in cartitem if item.product is not None]
    one_day_items = [item for item in cartitem if item.one_day is not None]

    product_total = sum(item.product.offer_price * item.quantity for item in product_items)
    product_delivery = sum(item.product.delivery * item.quantity for item in product_items)
    one_day_total = sum(item.one_day.offer_price * item.quantity for item in one_day_items)
    one_day_delivery = sum(item.one_day.delivery * item.quantity for item in one_day_items)
    total=product_total+one_day_total
    delivery=product_delivery+one_day_delivery
    total_amount = total + delivery
    sub_total = sum(item.quantity for item in cartitem)

    context = {
        "cart": cart,
        "cartitem": cartitem,
        "total" : total,
        "delivery" :delivery,
        "total_amount": total_amount,
        "sub_total": sub_total
    }

    return render(request, 'cart/cart.html', context)


def Checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    cartitem = CartItem.objects.filter(cart=cart)
    user_info = User_info.objects.filter(user=request.user).order_by('-id')

    # Handle product and one_day separately
    product_items = [item for item in cartitem if item.product is not None]
    one_day_items = [item for item in cartitem if item.one_day is not None]

    product_total = sum(item.product.offer_price * item.quantity for item in product_items)
    product_delivery = sum(item.product.delivery * item.quantity for item in product_items)
    one_day_total = sum(item.one_day.offer_price * item.quantity for item in one_day_items)
    one_day_delivery = sum(item.one_day.delivery * item.quantity for item in one_day_items)
    total = product_total + one_day_total
    delivery = product_delivery + one_day_delivery
    total_amount = total + delivery
    sub_total = sum(item.quantity for item in cartitem)

    if request.method == "POST":
        user_add = request.POST.get("selected_address_id")
        print("user_add==========================================", user_add)
        address = User_info.objects.get(id=user_add)
        print("address==========================================", address)

        amount = int(total_amount * 100)  # Razorpay needs amount in paise
        receipt = f"E_shopper-{int(time())}"

        # Razorpay Order Create
        payment = client.order.create({
            "amount": amount,
            "receipt": receipt,
            "currency": "INR",
            "payment_capture": "1",
        })
        print("payment==========================================", payment)

        # Save all products as orders
        for prod in cartitem:
            print("prod==========================================", prod)
            if prod.product:
                prod_total = (prod.product.offer_price + prod.product.delivery) * prod.quantity
                delivery=prod.product.delivery * prod.quantity
                order = Order(
                    user=request.user,
                    user_info=address,
                    order_id=payment["id"],
                    image=prod.product.prod_image,
                    product=prod.product.title,
                    quantity=prod.quantity,
                    price=prod.product.offer_price,
                    delivery=delivery,
                    pro_total=prod_total,
                )
                order.save()
            else:
                prod_total = (prod.one_day.offer_price + prod.one_day.delivery) * prod.quantity
                delivery = prod.one_day.delivery * prod.quantity
                order = Order(
                    user=request.user,
                    user_info=address,
                    order_id=payment["id"],
                    image=prod.one_day.prod_image,
                    product=prod.one_day.title,
                    quantity=prod.quantity,
                    price=prod.one_day.offer_price,
                    delivery=delivery,
                    pro_total=prod_total,
                )
                order.save()

        # Optional: Clear cart after creating order
        # cartitem.delete()

        # Return Razorpay order info to frontend
        return JsonResponse({
            "id": payment["id"],
            "amount": payment["amount"],
            "currency": payment["currency"],
            "receipt": receipt
        })

    # GET Request
    context = {
        "cart": cart,
        "cartitem": cartitem,
        "user_info": user_info,
        "total": total,
        "delivery": delivery,
        "total_amount": total_amount,
        "sub_total": sub_total,
    }

    return render(request, 'checkout/checkout.html', context)



@login_required(login_url="/users/login")
def Buy_now(request, id, field):
    cart = Cart.objects.filter(user=request.user).first()
    cartitem = CartItem.objects.filter(cart=cart)
    user_info = User_info.objects.filter(user=request.user).order_by('-id')
    context = {
        "cart": cart,
        "cartitem": cartitem,
        "user_info":user_info
    }
    if field == "one_day":
        one_day = One_day_deal.objects.get(id=id)
        context["one_day"] = one_day
        if request.method == "POST":
            user_add = request.POST.get("selected_address_id")
            print("user_add==========================================", user_add)
            address = User_info.objects.get(id=user_add)
            print("address==========================================", address)
            amount = (one_day.offer_price + one_day.delivery) * 100
            receipt = f"ShoppinglyX-{int(time())}"
            payment = client.order.create({
                "amount": amount,
                "receipt": receipt,
                "currency": "INR",
                "payment_capture": "1",
            })
            print("payment===============================================", payment)

            order = Order(
                user=request.user,
                user_info=address,
                order_id=payment["id"],
                image=one_day.prod_image,
                product=one_day.title,
                quantity=1,
                price=one_day.offer_price,
                delivery=one_day.delivery,
                pro_total=amount / 100,
            )
            order.save()

            return JsonResponse(payment)  # Return Razorpay order details via AJAX

        # On GET request, no payment is created
        context["payment"] = None,

        return render(request, 'checkout/buynow.html', context)
    else:
        product = Product.objects.get(id=id)
        context["product"] = product

        if request.method == "POST":
            user_add = request.POST.get("selected_address_id")
            print("user_add==========================================",user_add)
            address = User_info.objects.get(id=user_add)
            print("address==========================================", address)
            amount = (product.offer_price + product.delivery) * 100
            receipt = f"ShoppinglyX-{int(time())}"
            payment = client.order.create({
                "amount": amount,
                "receipt": receipt,
                "currency": "INR",
                "payment_capture": "1",
            })
            print("payment===============================================",payment)

            order = Order(
                user=request.user,
                user_info=address,
                order_id=payment["id"],
                image=product.prod_image,
                product=product.title,
                quantity=1,
                price=product.offer_price,
                delivery=product.delivery,
                pro_total=amount/100,
            )
            order.save()

            return JsonResponse(payment)  # Return Razorpay order details via AJAX

        # On GET request, no payment is created
        context  ["payment"]= None,


    return render(request, 'checkout/buynow.html', context)


@csrf_exempt
def Verify_payment(request):
    if request.method=="POST":
        razorpay_order_id=request.POST.get('razorpay_order_id')
        razorpay_payment_id=request.POST.get('razorpay_payment_id')
        razorpay_signature=request.POST.get('razorpay_signature')
        client=razorpay.Client(auth=(settings.KEY_ID,settings.KEY_SECRET))

        try:
            # Verify the signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            client.utility.verify_payment_signature(params_dict)

            order=Order.objects.filter(order_id=razorpay_order_id)
            for order in order:
                order.payment="paid"
                order.save()
            cart = Cart.objects.filter(user=request.user).first()
            cartitem = CartItem.objects.filter(cart=cart)
            cartitem.delete()
            return redirect("payment_success")

        except razorpay.errors.SignatureVerificationError:
            return redirect("payment_failed")
    return None


@csrf_exempt
def Success(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        cartitem=CartItem.objects.filter(cart=cart[0])

        context = {
            "cartitem":cartitem
        }
    return render(request,'payment/success.html',context)

@csrf_exempt
def Failed(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        cartitem=CartItem.objects.filter(cart=cart[0])

        context = {
            "cartitem":cartitem
        }
    return render(request,'payment/failed.html',context)

def Order_product(request):
    cart = Cart.objects.filter(user=request.user).first()
    cartitem = CartItem.objects.filter(cart=cart)
    ordered=Order.objects.filter(user=request.user).order_by('-id')

    context = {
        "cart": cart,
        "cartitem": cartitem,
        "ordered":ordered
    }
    return render(request, 'order/order.html',context)





#
# def change_password(request):
#     return render(request, 'app/changepassword.html')
#
#
# def mobile(request):
#     return render(request, 'app/mobile.html')
#
#

