from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.mail import send_mail
from django.conf import settings
from decimal import *

from .models import Toppings, Base, Category, Size, Type, Order


def index(request):
    context = {
        'user': request.user,
        'toppings': Toppings.objects.all(),
        'base': Base.objects.all(),
        'category': Category.objects.all(),
        'size': Size.objects.all(),
        'type': Type.objects.all(),
        'order': Order.objects.all()
    }

    if request.method == 'POST' and request.user.is_authenticated == True:
        try:
            type = request.POST.get('type')
            quantity = request.POST.get('quantity')
            user = request.user
            type = Type.objects.get(id=type)
        except:
            return render(request,'orders/index.html', context)

        try:
            topping = request.POST.get('topping')
            topping2 = request.POST.get('topping2')
            topping3 = request.POST.get('topping3')
        except:
            topping = None
            topping2 = None
            topping3 = None

        try:
            topping = Toppings.objects.get(id=topping)
            topping2 = Toppings.objects.get(id=topping2)
            topping3 = Toppings.objects.get(id=topping3)
            topping_price = topping.price
            price = (type.price + topping_price) * int(quantity)
            order = Order(type=type, topping=topping, topping2=topping2, topping3=topping3, user=user, price=price, quantity=quantity, is_added=True)
            order.save()
        except:
            price = type.price * int(quantity)
            order = Order(type=type, user=user, price=price, quantity=quantity, is_added=True)
            order.save()
    elif request.method == 'POST' and request.user.is_authenticated == False:
        return render(request,'orders/login.html', {'message':'Please log in to add an order.'})
    return render(request,'orders/index.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return render(request,'orders/login.html',{'message':'You are already logged in!'})

    if request.method == 'POST':
         username = request.POST['username']
         password = request.POST['password']
         user = authenticate(request, username=username, password=password)
         if user is not None:
             login(request, user)
             return HttpResponseRedirect('/')
         return render(request, 'orders/error.html', {'message': 'Invalid username/password.'})
    return render(request, 'orders/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse(index))


def register_view(request):
    if request.user.is_authenticated:
        return render(request,'orders/index.html',{'message':'You are already logged in!'})

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if not password == password2:
            return render(request,'orders/register.html',{'message':"Passwords don't match."})

        if User.objects.filter(username=username).exists():
            return render(request,'orders/register.html',{'message':"Username already exists."})

        user = User.objects.create_user(username,email,password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request,'orders/login.html',{'message':'Registered. Please log in now.'})
    return render(request,'orders/register.html')


def cart_view(request):
    user = request.user
    if request.method == 'POST':
        comment = request.POST['comment']
        order = Order.objects.filter(user=user, is_added=True, is_ordered=False).update(comment=comment)
        order = Order.objects.filter(user=user, is_added=True, is_ordered=False)
        price = Order.objects.filter(user=user, is_added=True, is_ordered=False).aggregate(Sum('price'))
        user_email = User.objects.get(username=request.user)
        user_email = user_email.email
        subject = 'Thank you for your order!'
        message = "Thank you for your order! The total price for your order is €%s. Comments: '%s.' Order = %s " % (
        round(price['price__sum'], 2),
        comment,
        order
        )
        email_from = settings.EMAIL_HOST_USER
        to_email = [email_from , user_email]
        send_mail(subject, message, email_from, to_email, fail_silently=False)
        order = Order.objects.filter(user=user, is_ordered=False, is_added=True).exclude(price='0.00').update(is_ordered=True)
        return render(request, 'orders/cart.html', {'message':'Order placed'})

    context = {
        'user': request.user,
        'order': Order.objects.filter(user=user, is_added=True, is_ordered=False).exclude(price='0.00'),
        'total': Order.objects.filter(user=user, is_added=True, is_ordered=False).exclude(price='0.00').aggregate(Sum('price')),
        'items_total': Order.objects.filter(user=user, is_added=True, is_ordered=False).exclude(price='0.00').count()

    }
    return render(request, 'orders/cart.html', context)


def delete_cart(request):
    user = request.user
    order = Order.objects.filter(user=user, is_ordered=False).update(is_added=False)
    return HttpResponseRedirect(reverse(cart_view))


def user_view(request):
    user = request.user
    context = {
        'user': request.user,
        'order': Order.objects.exclude(price='0.00').filter(user=user, is_ordered=True, is_added=True),
        'order_total': Order.objects.exclude(price='0.00').filter(user=user, is_ordered=True, is_added=True).count(),
        'all_orders': Order.objects.exclude(price='0.00').filter(is_ordered=True),
        'all_orders_total': Order.objects.exclude(price='0.00').filter(is_ordered=True).count()
    }
    return render(request, 'orders/user.html', context)

def error_view(request):
    return render(request, 'orders/error.html')
