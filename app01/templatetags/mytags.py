# -*- coding:utf-8 -*-
# Author:cqk
# Data:2019/10/22 11:45
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http.request import QueryDict

register=template.Library()


# @register.simple_tag
# def show_info(request):
#     path = request.path
#     if path == reverse("app01:customer"):
#         return mark_safe("""
#
#         """)
#     else:
#         return mark_safe("""
#
#                """)
@register.simple_tag
def reverse_url(url_name, id, request):
    path=request.get_full_path()
    query_dict_obj=QueryDict(mutable=True)
    query_dict_obj["next"]=path
    encode_url=query_dict_obj.urlencode()
    prefix_path=reverse(url_name, args=(id,))
    full_path=prefix_path + "?" + encode_url
    return full_path

@register.simple_tag
def myname(request):
    name=request.session.get("username")
    return name