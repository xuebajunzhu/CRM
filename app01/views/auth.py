# -*- coding:utf-8 -*-
# Author:cqk
# Data:2019/10/23 8:50
from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from utils.MD5_func import md5_function
from app01.MyModelForm.UserInfoForm import UserInfoForm
def logout(request):
    request.session.flush()  # 清除cookie和session
    return redirect("app01:login")


def login(request):
    if request.method == "POST":
        dic=request.POST.dict()
        user=models.UserInfo.objects.filter(username=dic.get("username"),
                                            password=md5_function(dic.get("password"))).first()
        if user:
            request.session["username"]=dic["username"]
            return redirect("app01:home")
        else:
            return HttpResponse("用户名或密码错误")
    return render(request, "login/login.html", {})


def register(request):
    user=UserInfoForm()
    if request.method == "POST":
        dic=request.POST.dict()
        print(dic)
        dic.pop("csrfmiddlewaretoken")
        dic.pop("confirm_password")

        user=UserInfoForm(data=request.POST)
        # print(user)
        if user.is_valid():
            dic.update({"password": md5_function(dic["password"])})
            models.UserInfo.objects.create(**dic)
            return redirect("app01:login")

        else:
            return render(request, "login/register.html", {"user": user})

    return render(request, "login/register.html", {"user": user})

