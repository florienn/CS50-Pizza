"""
views.py

Minor programmeren (CS50), Web App Studio
November 2019
Florien Altena

Pizza ordering web application using Django.

"""

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from decimal import *

from .models import Toppings, Base, Category, Size, Type, Order

def index(request):
    """
    Menu page, add orders
    """
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
        type = request.POST.get('type')
        quantity = request.POST.get('quantity')
        user = request.user
        type = Type.objects.get(id=type)
        topping = request.POST.get('topping')
        topping2 = request.POST.get('topping2')
        topping3 = request.POST.get('topping3')

        try:
            topping = Toppings.objects.get(id=topping)
            topping2 = Toppings.objects.get(id=topping2)
            topping3 = Toppings.objects.get(id=topping3)
            topping_price = topping.price
            price = (type.price + topping_price) * int(quantity)
            order = Order(type=type, topping=topping, topping2=topping2, topping3=topping3, user=user, price=price, quantity=quantity, is_added=True)
            order.save()
        except ObjectDoesNotExist:
            price = type.price * int(quantity)
            order = Order(type=type, user=user, price=price, quantity=quantity, is_added=True)
            order.save()

    elif request.method == 'POST' and request.user.is_authenticated == False:
        return render(request,'orders/login.html', {'message_danger':'Please log in to add an order.'})
    return render(request,'orders/index.html', context)

def login_view(request):
    """
    Logs user in
    """
    if request.user.is_authenticated:
        return render(request,'orders/login.html',{'message_danger':'You are already logged in!'})

    if request.method == 'POST':
         username = request.POST['username']
         password = request.POST['password']
         user = authenticate(request, username=username, password=password)

         if user is not None:
             login(request, user)
             return HttpResponseRedirect('/')
         return render(request, 'orders/login.html', {'message_danger': 'Invalid username/password.'})
    return render(request, 'orders/login.html')


def logout_view(request):
    """
    Logs user out
    """
    logout(request)
    return HttpResponseRedirect(reverse(login_view))


def register_view(request):
    """
    Creates new user
    """
    if request.user.is_authenticated:
        return render(request,'orders/register.html', {'message_danger':'You are already logged in!'})

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if not password == password2:
            return render(request,'orders/register.html', {'message_danger':'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request,'orders/register.html', {'message_danger':'Username already exists.'})

        if User.objects.filter(email=email).exists():
            return render(request,'orders/register.html', {'message_danger':'You already have an account with that email address.'})

        try:
            user = User.objects.create_user(username,email,password)
        except ValueError:
            return render(request,'orders/register.html', {'message_danger':'Please fill in all fields'})

        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request,'orders/login.html', {'message_success':'Registered. Please log in now.'})
    return render(request,'orders/register.html')


def cart_view(request):
    """
    Shopping cart contents, adds comments, places orders and sends order verification email
    """
    user = request.user
    context = {
        'user': request.user,
        'order': Order.objects.filter(user=user, is_added=True, is_ordered=False).exclude(price='0.00'),
        'total': Order.objects.filter(user=user, is_added=True, is_ordered=False).exclude(price='0.00').aggregate(Sum('price')),
        'items_total': Order.objects.filter(user=user, is_added=True, is_ordered=False).exclude(price='0.00').count()

    }
    if request.method == 'POST':
        try:
            address = request.POST.get('address', False)
            city = request.POST['city']
            zip = request.POST['zip']
            comment = request.POST['comment']
            order = Order.objects.filter(user=user, is_added=True, is_ordered=False).update(address=address, city=city, zip=zip, comment=comment)
            order = Order.objects.filter(user=user, is_added=True, is_ordered=False).all()

            orders = []
            for o in order:
                orders.append(o.quantity)
                orders.append(o.type)

            all_orders = ' '.join(map(str, orders))
            price = Order.objects.filter(user=user, is_added=True, is_ordered=False).aggregate(Sum('price'))
            user_email = User.objects.get(username=user)
            user_email = user_email.email
            subject = 'Thank you for your order!'
            message = 'Thank you for your order! Your pizza will arrive soon. The total price for your order is €%s. Your order includes: %s. We will be delivering your order to %s %s %s. Your additional comments are: "%s".' % (
                round(price['price__sum'], 2),
                all_orders,
                address,
                zip,
                city,
                comment,
            )
            email_from = settings.EMAIL_HOST_USER
            to_email = [email_from , user_email]
            send_mail(subject, message, email_from, to_email, fail_silently=False)
            order = Order.objects.filter(user=user, is_added=True, is_ordered=False).update(is_ordered=True)
            return render(request, 'orders/cart.html', {'message_success':'Order placed. You will receive a verification email shortly!'})
        except TypeError:
            return render(request, 'orders/cart.html', {'message_danger':'Something went wrong. Please try again.'})
    return render(request, 'orders/cart.html', context)


def delete_cart(request):
    """
    Deletes shopping cart contents
    """
    order = Order.objects.filter(user=request.user, is_ordered=False).delete()
    return HttpResponseRedirect(reverse(cart_view))


def user_view(request):
    """
    Shows user's previous orders or all orders for superuser
    """
    user = request.user
    context = {
        'user': request.user,
        'order': Order.objects.exclude(price='0.00').filter(user=user, is_ordered=True, is_added=True),
        'order_total': Order.objects.exclude(price='0.00').filter(user=user, is_ordered=True, is_added=True).count(),
        'all_orders': Order.objects.exclude(price='0.00').filter(is_ordered=True),
        'all_orders_total': Order.objects.exclude(price='0.00').filter(is_ordered=True).count()
    }
    return render(request, 'orders/user.html', context)
