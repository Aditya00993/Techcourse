from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Categoties,Course,Zara
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Categoties,Course,Zara,Video,Usercource,Payment
from django.db.models import Sum
from income.settings import *
import razorpay
from time import time
client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))
# Create your views here.
def index(request):
    return render(request,'base.html')

def home(request):
    category = Categoties.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    context = {
        'category' :category,
        'course' : course
    }
    return render(request,'main/home.html',context)


def single(request):
    category =  Categoties.get_all_category(Categoties)
    zora = Zara.objects.all()
    course = Course.objects.all()
    free = Course.objects.filter(price = 0).count
    paid = Course.objects.filter(price__gte=1).count
    context = {
        'category':category,
        'level' : zora,
        'course' : course,
        'free' :free,
        'paid' : paid
        
    }
    return render(request,'main/single.html',context)


def contact(request):
    category = Categoties.get_all_category(Categoties)
    context = {
        'category' :category
    }
    return render(request,'main/contact.html',context)

def about(request):
    category = Categoties.get_all_category(Categoties)
    context = {
        'category' :category
    }
    return render(request,'main/about.html',context)



def filter_data(request):

    Categoties = request.GET.getlist('category[]')
    Zara = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    print(price)


    if price == ['pricefree']:
       course = Course.objects.filter(price=0)
    elif price == ['pricepaid']:
       course = Course.objects.filter(price__gte=1)
    elif price == ['priceall']:
       course = Course.objects.all()
    elif Categoties:
       course = Course.objects.filter(category__id__in=Categoties).order_by('-id')
    elif Zara:
       course = Course.objects.filter(level__id__in = Zara).order_by('-id')
    else:
       course = Course.objects.all().order_by('-id')


    t = render_to_string('ajax/course.html', {'course': course})

    return JsonResponse({'data': t})



def search(request):
    category = Categoties.get_all_category(Categoties)
  
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query )
    print(course)
    context= {
        'course' : course,
            'category' :category
    }
    return render(request,'search.html',context)


def Coursedetail(request,slug):
    category = Categoties.get_all_category(Categoties)
   
    course_id = Course.objects.get(slug=slug)
    course = Course.objects.filter(slug=slug)
    try:
        check_enrolled = Usercource.objects.get(user = request.user,course=course_id)
    except Usercource.DoesNotExist:
        check_enrolled = None
    time_duration = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    
    context = {
        'course' : course,
        'category' : category,
        'time_duration': time_duration,
        'check_enrolled' :check_enrolled
    }
    return render(request,'course/coursedetail.html',context)


def pagenot(request):
    category = Categoties.get_all_category(Categoties)
       
    context = {
        
        'category' : category
    }
    return render(request,'error.html',context)

def checkout(request,slug):
    course = Course.objects.get(slug=slug)
    action = request.GET.get('action')
    order = None
    if course.price == 0:
        course = Usercource(
            user= request.user,
            course= course,
        )
        course.save()
        messages.success(request,'Course are successfully Enrolled')
        return redirect('mycourse')
    elif action == 'create_payment' :
        if request.METHOD == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            country = request.POST.get('country')
            address_1 = request.POST.get('address_1')
            address_2 = request.POST.get('address_2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postcode= request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            order_comments = request.POST.get('order_comments')

            amount = course.price * 100
            currency ="INR"
            notes = {
                "name" : f'{first_name} {last_name}',
                "country": country,
                "address": f'{address_1} {address_2} ',
                "state" : state,
                "postcode": postcode,
                "phone" : phone,
                "email" :email,
                "order_comments": order_comments
            
            }
            receipt = f"Techcourse-{int(time())}"
            order = client.order.create(
                {
                    'receipt' : receipt,
                    'notes' :notes,
                    'amount' : amount,
                    'currency' :currency
                    
                }
            )
            payment = Payment(
                course = course,
                user = request.user,
                order_id = order.get('id')
                )
            payment.save()

    context = {
        'course':course
    }
    return render(request,'checkout/checkout.html',context)


def Mycourse(request):
    course = Usercource.objects.filter(user=request.user)
    context ={
        'course':course,
        'order' : order
    }
    return render(request,'course/mycourse.html',context)