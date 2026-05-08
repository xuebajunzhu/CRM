# -*- coding: utf-8 -*-
"""
Authentication views for CRM system.
Handles user login, logout, and registration.
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

from app01 import models
from app01.MyModelForm.UserInfoForm import UserInfoForm


def logout(request):
    """Clear session data and redirect to login page."""
    request.session.flush()
    return redirect("app01:login")


def login(request):
    """Handle user login with username and password using secure password hashing."""
    if request.method == "POST":
        data = request.POST.dict()
        username = data.get("username")
        password = data.get("password")
        
        user = models.UserInfo.objects.filter(username=username).first()
        
        if user and check_password(password, user.password):
            request.session["username"] = username
            # Set session expiry for security
            request.session.set_expiry(3600)  # 1 hour
            return redirect("app01:home")
        else:
            # Log failed attempt (for audit)
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed login attempt for username: {username}")
            return HttpResponse("用户名或密码错误")
    
    return render(request, "login/login.html", {})


def register(request):
    """Handle user registration with form validation and secure password hashing."""
    if request.method == "POST":
        form = UserInfoForm(data=request.POST)
        
        if form.is_valid():
            # Create user with securely hashed password
            cleaned_data = form.cleaned_data
            models.UserInfo.objects.create(
                username=cleaned_data["username"],
                password=make_password(cleaned_data["password"]),  # Secure hashing
                telephone=cleaned_data["telephone"],
                email=cleaned_data["email"],
            )
            return redirect("app01:login")
        
        return render(request, "login/register.html", {"user": form})
    
    form = UserInfoForm()
    return render(request, "login/register.html", {"user": form})
