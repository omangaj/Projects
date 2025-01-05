from django.shortcuts import render,redirect,HttpResponse
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from cart.cart import Cart

def Master(request):

    return render(request, "master.html",)

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

    context = {
        "category": category,
        "product": product,
        "brand": brand
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
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")

@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
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
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


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
    context = {
        "contact": contact,
        "link": link
    }
    return render(request, 'contact_us.html', context)

def Checkout(request):
    if request.method=="POST":
        mobile = request.POST.get("mobile")
        address=request.POST.get("address")
        pincode=request.POST.get("pincode")
        cart=request.session.get('cart')
        uid=request.session.get('_auth_user_id')
        user=User.objects.get(pk=uid)

        for i in cart:
            a=cart[i]['price']
            b=cart[i]['quantity']
            total= int(a) * int(b)
            order=Order(
                user=user,
                product=cart[i]['name'],
                price=cart[i]['price'],
                quantity=cart[i]['quantity'],
                image=cart[i]['image'],
                address=address,
                mobile=mobile,
                pincode=pincode,
                total=total
            )
            order.save()
        request.session['cart']={}
        return redirect("index")
    return HttpResponse("This is Checkout page")

def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    order=Order.objects.filter(user=user)
    context={
        'order':order,
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
    context={
        "category": category,
        "product": product,
        "prod": prod,
        "brand": brand
    }
    return render(request,'product_details.html',context)

def Search(request):
    query=request.GET['query']
    product=Product.objects.filter(name__icontains=query)
    context={
        "product":product
    }
    return render(request,'search.html',context)