# -*- coding:utf-8 -*-
# Author:cqk
# Data:2019/10/22 21:25
from django import forms
from django.forms import ValidationError
from app01 import models
class UserInfoForm(forms.Form):
    username=forms.CharField(
        label="用户名",
        max_length=16,
        min_length=4,
        error_messages={
            "min_length": "太短了",
            "required": "不能为空",
        },
        widget=forms.widgets.TextInput(attrs={"class": "username", "placeholder": "您的用户名", "autocomplete": "off"})
    )
    password=forms.CharField(
        label="密码",
        max_length=32,
        min_length=6,
        widget=forms.PasswordInput(attrs={"class": "password", "placeholder": "输入密码", "oncontextmenu": "return false",
                                          "onpaste": "return false"}),
        error_messages={
            "min_length": "太短了",
            "required": "不能为空",

        }

    )
    confirm_password=forms.CharField(
        label="确认密码",
        max_length=32,
        min_length=6,
        widget=forms.PasswordInput(
            attrs={"class": "confirm_password", "placeholder": "再次输入密码", "oncontextmenu": "return false",
                   "onpaste": "return false"}),
        error_messages={
            "min_length": "太短了",
            "required": "不能为空",
        }
    )
    telephone=forms.CharField(
        label="手机号",
        max_length=11,
        min_length=11,
        widget=forms.widgets.TextInput(attrs={"class": "phone_number", "placeholder": "输入手机号码", "autocomplete": "off"}),
        error_messages={
            "min_length": "手机号格式有误!!!",
            "required": "手机号不能为空",
        }
    )
    email=forms.EmailField(
        label="邮箱",
        error_messages={
            "required": "emial不能为空",
            "invalid": "邮箱格式错误",
        },
        widget=forms.widgets.EmailInput(
            attrs={"type": "email", "class": "email", "placeholder": "输入邮箱地址", "oncontextmenu": "return false",
                   "onpaste": "return false"}),
    )

    def clean_username(self):
        user=self.cleaned_data.get("username")
        ret=models.UserInfo.objects.filter(username=user).first()
        if ret:
            raise ValidationError("用户名已经存在!")

    def clean_confirm_password(self):
        pwd=self.cleaned_data.get("password")
        re_pwd=self.cleaned_data.get("confirm_password")
        if pwd != re_pwd:
            raise ValidationError("两次密码输入不一致!")
        else:
            return re_pwd