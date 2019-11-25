from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .models import Toppings, Base, Category, Size, Type, Order

def index(request):
    context = {
        "user": request.user,
        "toppings": Toppings.objects.all(),
        "base": Base.objects.all(),
        "category": Category.objects.all(),
        "size": Size.objects.all(),
        "type": Type.objects.all(),
        "order": Order.objects.all()
    }
    return render(request,"orders/index.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return render(request,"orders/index.html",{"message":"You are already logged in!"})

    if request.method == "POST":
         username = request.POST["username"]
         password = request.POST["password"]
         user = authenticate(request, username=username, password=password)
         if user is not None:
             login(request, user)
             return HttpResponseRedirect(reverse("index"))
         return render(request, "orders/login.html", {"message": "Invalid credentials."})
    return render(request, "orders/login.html")


def logout_view(request):
    logout(request)
    return render(request,"orders/index.html",{"message":"Logged out."})


def register_view(request):
    if request.user.is_authenticated:
        return render(request,"orders/index.html",{"message":"You are already logged in!"})

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if not password == password2:
            return render(request,"orders/register.html",{"message":"Passwords don't match."})
        user = User.objects.create_user(username,email,password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request,"orders/login.html",{"message":"Registered. You can log in now."})
    return render(request,"orders/register.html")


def cart_view(request):
    return render(request, "orders/cart.html")


def user_view(request):
    return render(request, "orders/user.html")


def add(request, order_id):
    try:
        passenger_id = int(request.POST["passenger"])
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=passenger_id)
    except KeyError:
        return render(request, "flights/error.html", {"message": "No selection."})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No flight."})
    except Passenger.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No passenger."})
    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
