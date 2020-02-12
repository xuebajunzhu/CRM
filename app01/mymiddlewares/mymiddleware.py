# -*- coding:utf-8 -*-
# Author:cqk
# Data:2019/10/22 10:03
from  django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
class Auth(MiddlewareMixin):
    white_list=[reverse("app01:login"),reverse("app01:register")]
    def process_request(self,request):
        path=request.path
        if path not in self.white_list:
            value=request.session.get("username")
            if not value:
                return redirect("app01:login")
