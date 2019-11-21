from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"pizza/index.html")

def login(request):
    return render(request,"pizza/login.html")

def register(request):
    return render(request,"pizza/register.html")
