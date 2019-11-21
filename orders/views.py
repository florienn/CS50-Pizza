from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User

def index(request):
    if not request.user.is_authenticated:
        return render(request,"pizza/login.html",{"message":None})
    context = {
        "user": request.user
    }
    return render(request,"pizza/index.html",context)

def login_view(request):
    if request.method == "POST":
         username = request.POST["username"]
         password = request.POST["password"]
         user = authenticate(request, username=username, password=password)
         if user is not None:
             login(request, user)
             return HttpResponseRedirect(reverse("index"))
         return render(request, "pizza/login.html", {"message": "Invalid credentials."})
    return render(request, "pizza/login.html")

def logout_view(request):
    logout(request)
    return render(request, "pizza/login.html", {"message": "Logged out."})

def register_view(request):
    if request.method == "POST":
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        password2=request.POST["password2"]
        if not password==password2:
            return render(request,"pizza/register.html",{"message":"Passwords don't match."})
        user=User.objects.create_user(username,email,password)
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        return render(request,"pizza/login.html",{"message":"Registered. You can log in now."})
    return render(request,"pizza/register.html")
