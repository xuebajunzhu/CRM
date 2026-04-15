# -*- coding: utf-8 -*-
"""
Authentication views for CRM system.
Handles user login, logout, and registration.
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse

from app01 import models
from utils.MD5_func import md5_function
from app01.MyModelForm.UserInfoForm import UserInfoForm


def logout(request):
    """Clear session data and redirect to login page."""
    request.session.flush()
    return redirect("app01:login")


def login(request):
    """Handle user login with username and password."""
    if request.method == "POST":
        data = request.POST.dict()
        username = data.get("username")
        password = md5_function(data.get("password"))
        
        user = models.UserInfo.objects.filter(
            username=username,
            password=password
        ).first()
        
        if user:
            request.session["username"] = username
            return redirect("app01:home")
        else:
            return HttpResponse("用户名或密码错误")
    
    return render(request, "login/login.html", {})


def register(request):
    """Handle user registration with form validation."""
    if request.method == "POST":
        form = UserInfoForm(data=request.POST)
        
        if form.is_valid():
            # Create user with hashed password
            cleaned_data = form.cleaned_data
            models.UserInfo.objects.create(
                username=cleaned_data["username"],
                password=md5_function(cleaned_data["password"]),
                telephone=cleaned_data["telephone"],
                email=cleaned_data["email"],
            )
            return redirect("app01:login")
        
        return render(request, "login/register.html", {"user": form})
    
    form = UserInfoForm()
    return render(request, "login/register.html", {"user": form})
