from django.shortcuts import render,redirect
from app.models import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Sum
from django.contrib import messages
from django.core.mail import send_mail,EmailMessage

from django.views.decorators.csrf import csrf_exempt
from .settings import *
import razorpay
from time import time

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


def Base(request):
    return render(request, "app/base.html")


def Home(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course= Course.objects.filter(status='PUBLISH').order_by('-id')
    data = {
        "category": category,
        "course": course
    }
    return render(request, "main/home.html", data)


def About(request):
    category = Categories.category(Categories)
    course = Course.objects.filter(status='PUBLISH')
    data = {
        "category": category,
        "course": course
    }
    return render(request, "main/about_us.html",data)


def Contact(request):
    category = Categories.category(Categories)
    course = Course.course(Course)
    data = {
        "category": category,
        "course": course
    }
    try:
        pname = request.POST.get('name')
        pemail = request.POST.get('email')
        pmessage = request.POST.get('message')
        EmailMessage(
            'Contact form submission from {}'.format(pname), pmessage,
            'omkarangaj2018@gmail.com',
            [],
            [],
            reply_to=[pemail]
        ).send()
        pass_data = Contact(name=pname, email=pemail, message=pmessage)
        pass_data.save()
        return redirect('contact_us')
    except:
        pass
    return render(request, 'main/contact_us.html', data)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')

    if price == ['pricefree']:
       course = Course.objects.filter(price=0).order_by("-id")
    elif price == ['pricepaid']:
       course = Course.objects.filter(price__gte=1).order_by("-id")
    elif price == ['priceall']:
       course = Course.objects.all().order_by("-id")
    elif categories:
        course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')

    t = render_to_string('ajax/course.html', {'course': course})
    return JsonResponse({'data': t})

def Single_Course(request):
    category= Categories.category(Categories)
    course = Course.objects.filter(status='PUBLISH').order_by("-id")
    level= Level.objects.all()
    freecourse=Course.objects.filter(price=0)
    paidcourse=Course.objects.filter(price__gte=1)
    data={
        "category":category,
        "course":course,
        "level": level,
        "freecourse":freecourse,
        "paidcourse":paidcourse
    }

    return render(request, "main/single_course.html",data)




def SEARCH_COURSE(request):
    query = request.GET.get('query', '')  # Get the query parameter from the request

    # Check if the query exists
    if query:
        # Filter courses by title or by category name
        course = Course.objects.filter(
            Q(title__icontains = query) , Q(category__name__icontains = query)
        )
    else:
        course = Course.objects.none()  # Empty queryset if no query is provided

    context = {
        'course': course
    }
    return render(request, "search/search.html",context)


def COURSE_DETAILS(request,slug):
    course = Course.objects.filter(slug = slug)
    time_duration = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))
    Course_id =Course.objects.get(slug = slug)
    try:
        check_enroll = UserCourse.objects.get(user = request.user, course = Course_id)
    except UserCourse.DoesNotExist:
        check_enroll = None

    if course.exists():
        course = course.first()
    else:
        return redirect("404")

    wyl = What_you_learn.objects.all()
    require = Requirement.objects.all()
    data = {
        "course": course,
        "wyl": wyl,
        "require": require,
        "time_duration": time_duration,
        "check_enroll": check_enroll
    }
    return render(request,"course/course_details.html",data)


def PAGE_NOT_FOUND(request):

    return render(request,'error/404.html')


def CHECKOUT(request, slug):
    course = Course.objects.get(slug=slug)
    action = request.GET.get('action')
    order = None
    if course.price == 0:
        course = UserCourse(
            user = request.user,
            course = course,
        )
        course.save()
        messages.success(request,'Course Are Successfully Enrolled ....!')
        return redirect('my_course')
    elif action == 'create_payment':
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            company = request.POST.get('company')
            country = request.POST.get('country')
            address_1 = request.POST.get('address_1')
            address_2 = request.POST.get('address_2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            amount = course.price * 100
            currency = "INR"
            notes = {
                "name": f' {first_name} {last_name}',
                "country": country,
                "address": f'{address_1}{address_2}',
                "city": city,
                "state": state,
                "postcode": postcode,
                "phone": phone,
                "email": email,
            }
            receipt = f"Skola-{int(time())}"
            order = client.order.create(
                {
                    'receipt': receipt,
                    'notes': notes,
                    'amount': amount,
                    'currency': currency,
                }
            )
            payment = Payment (
                course=course,
                user=request.user,
                order_id=order.get('id')
            )
            payment.save()

    contex = {
        'course' : course,
        'order': order,
    }
    return render(request, 'checkout/checkout.html', contex)


def CHECKOUT(request, slug):
    course = Course.objects.get(slug=slug)
    if course.price == 0:
        course = UserCourse(
            user = request.user,
            course = course,
        )
        course.save()
        messages.success(request,'Course Is Successfully Enrolled ....!')
        return redirect('my_course')

    contex = {
        'course' : course,
    }
    return render(request, 'checkout/checkout.html', contex)

def MY_COURSE(request):
    course = UserCourse.objects.filter(user=request.user)
    priceall = UserCourse.objects.filter(user=request.user).count
    # time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))
    context = {
        'course': course,
        'priceall': priceall
    }
    return render(request, 'course/my_course.html', context)


@csrf_exempt
def VERIFY_PAYMENT(request):
    if request.method == "POST":
        data=request.POST
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_order_id']

            payment
            Payment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True

            usercourse = UserCource(
                user=payment.user,
                course=payment.course,
            )
            usercourse.save()
            payment.user_course = usercourse
            payment.save()

            context = {
                'data': data,
                'payment': payment,
            }
            return render(request, 'verify_payment/success.html', context)
        except:
            return render(request, 'verify_payment/fail.html')

