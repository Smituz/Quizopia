from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, alogin
from django.contrib import messages
from .models import User_info,Quetions,Quiz,Participants
import os

# Create your views here.


def login(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]        
        alluser = User_info.objects.all()
        for user in alluser:
            if user.username==username:
                if user.password==password:
                    alogin(request, user)
                    # request.session['user_id'] = user.id
                    request.session['username']=username
                    # user_info = User_info.objects.get(username=username)
                    return redirect("home")
                else:
                    messages.info(request, "Incorrect Password")
                    return redirect("login")
        messages.info(request, "Username Does not exist")   
    return render(request, "login.html")

def register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        name=request.POST.get('name')
        password=request.POST.get('password')
        if User_info.objects.filter(username=username).exists():
            messages.error(request,"Username already taken")
            return redirect("register")
        ins = User_info(username=username , email=email , password=password , name=name)
        ins.save()
        messages.info(request, "Registerd Successfully.")
        return redirect("login")
    return render(request, "register.html")


