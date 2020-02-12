# -*- coding:utf-8 -*-
# Author:cqk
# Data:2019/10/23 8:55
import json

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.views import View
from django.db import transaction
from django.forms.models import modelformset_factory  # 工厂
from app01 import models
from app01.MyModelForm import myforms
from utils.page import InitPage


# Create your views here.


def home(request):
    return render(request, "customer/home.html", {})


class Customer(View):

    def get(self, request):
        search_field = request.GET.get("field")  # 搜索条件name__contains
        keyword = request.GET.get("keyword")  # 搜索数据 "陈"
        # models.Customer.objects.filter(**{search_field:keyword})#方式一
        import copy
        get_data = copy.copy(request.GET)  # GET获取的原始数据

        if keyword:
            q = Q()  # 实例化一个对象
            q.children.append([search_field, keyword])  # Q(name__contains="陈")
            all_customer = models.Customer.objects.filter(q)  # 方式三
        else:

            all_customer = models.Customer.objects.all()
        if request.path == reverse("app01:private_customer"):
            all_customer = all_customer.filter(consultant__username=request.session.get("username"))
        else:
            all_customer = all_customer.filter(consultant__isnull=True)
        all_customer_number = all_customer.count()
        Page = InitPage(request.GET.get("page", 1), all_customer_number, get_data=get_data)

        return render(request, "customer/customer.html",
                      {"all_customer": all_customer[Page.start_data_number:Page.end_data_number],
                       "page_html": Page.page_html_func(),
                       "keyword": keyword,
                       "search_field": search_field})

    def post(self, request):
        pk_data = request.POST.get("pk_data")
        pk_data = json.loads(pk_data)

        action = request.POST.get("action")
        if hasattr(self, action):
            return getattr(self, action)(request, pk_data)
        else:
            return reverse("app01:customer")

    def publish_private(self, request, pk_data):
        with  transaction.atomic():
            customer_obj = models.Customer.objects.select_for_update().filter(id__in=pk_data)
            user_obj = models.UserInfo.objects.select_for_update().filter(
                username=request.session.get("username")).first()
            customer_obj.update(consultant_id=user_obj.id)
        return JsonResponse({"status": 1, "url": reverse("app01:private_customer")})

    def private_publish(self, request, pk_data):
        with  transaction.atomic():
            customer_obj = models.Customer.objects.filter(id__in=pk_data)
            customer_obj.update(consultant=None)
        return JsonResponse({"status": 1, "url": reverse("app01:customer")})

    def bluk_delete(self, request, pk_data):
        with  transaction.atomic():
            customer_obj = models.Customer.objects.filter(id__in=pk_data)
            customer_obj.delete()
        return JsonResponse({"status": 1, "url": reverse("app01:customer")})


def add_editor_customer(request, n=None):
    head = "编辑客户" if n else "添加客户"
    old_obj = myforms.CustomerModelForm(instance=models.Customer.objects.filter(pk=n).first())
    if request.method == "POST":
        next_path = request.GET.get("next")

        old_obj = myforms.CustomerModelForm(data=request.POST, instance=models.Customer.objects.filter(pk=n).first())
        if old_obj.is_valid():
            old_obj.save()

            return redirect("app01:customer") if not n else redirect(next_path)
        else:
            render(request, "customer/add_editor_customer.html", {"old_obj": old_obj, "head": head})
    return render(request, "customer/add_editor_customer.html", {"old_obj": old_obj, "head": head})


# def consult_record(request):
#     consult_record_obj=myforms.ConsultRecordModelForm(request)
#     return render(request, "consult_record/consult_record.html", {"consult_record_obj": consult_record_obj})


class Consult_Record(View):
    def get(self, request):
        search_field = request.GET.get("field")  # 搜索条件name__contains
        keyword = request.GET.get("keyword")  # 搜索数据 "陈"
        import copy
        get_data = copy.copy(request.GET)  # GET获取的原始数据

        # 单个客户的id
        customer_id = request.GET.get("customer_id")
        if keyword:
            q = Q()  # 实例化一个对象
            q.children.append([search_field, keyword])  # Q(name__contains="陈")
            all_records = models.ConsultRecord.objects.filter(q)  # 方式三
        else:
            all_records = models.ConsultRecord.objects.all()
        all_records = all_records.filter(consultant__username=request.session.get("username"), delete_status=False)
        if customer_id:
            all_records = all_records.filter(customer_id=customer_id)
        all_records_number = all_records.count()
        Page = InitPage(request.GET.get("page", 1), all_records_number, get_data=get_data)

        return render(request, "consult_record/consult_record.html",
                      {"all_records": all_records[Page.start_data_number:Page.end_data_number],
                       "page_html": Page.page_html_func(),
                       "keyword": keyword,
                       "search_field": search_field})

    def post(self, request):
        pk_data = request.POST.get("pk_data")
        pk_data = json.loads(pk_data)

        action = request.POST.get("action")
        if hasattr(self, action):
            return getattr(self, action)(request, pk_data)
        else:
            return reverse("app01:consult_record")

    def bluk_delete(self, request, pk_data):
        with transaction.atomic():
            consult_record_list = models.ConsultRecord.objects.filter(id__in=pk_data)
            consult_record_list.update(delete_status=True)
        return JsonResponse({"status": 1, "url": reverse("app01:consult_record")})


def add_editor_consult_record(request, n=None):
    head = "编辑记录" if n else "添加记录"
    old_obj = myforms.ConsultRecordModelForm(request=request, instance=models.ConsultRecord.objects.filter(pk=n,
                                                                                                           consultant__username=request.session.get(
                                                                                                               "username")).first())
    if not old_obj:
        return HttpResponse("数据被抢走了!")
    if request.method == "POST":
        next_path = request.GET.get("next")
        old_obj = myforms.ConsultRecordModelForm(request=request, data=request.POST,
                                                 instance=models.ConsultRecord.objects.filter(pk=n,
                                                                                              consultant__username=request.session.get(
                                                                                                  "username")).first())
        if old_obj.is_valid():
            old_obj.save()
            return redirect("app01:consult_record") if not next_path else redirect(next_path)
        else:
            render(request, "consult_record/add_editor_consult_record.html", {"old_obj": old_obj, "head": head})
    return render(request, "consult_record/add_editor_consult_record.html", {"old_obj": old_obj, "head": head})


class Enrollment(View):
    """
    报名表
    """

    def get(self, request):
        search_field = request.GET.get("field")  # 搜索条件name__contains
        keyword = request.GET.get("keyword")  # 搜索数据 "陈"
        import copy
        get_data = copy.copy(request.GET)  # GET获取的原始数据

        # 单个客户的id
        # customer_id=request.GET.get("customer_id")
        if keyword:
            q = Q()  # 实例化一个对象
            q.children.append([search_field, keyword])  # Q(name__contains="陈")
            all_enrollment = models.Enrollment.objects.filter(q)  # 方式三
        else:
            all_enrollment = models.Enrollment.objects.all()
        all_enrollment = all_enrollment.filter(customer__consultant__username=request.session.get("username"),
                                               delete_status=False)
        # if customer_id:
        #     all_records=all_records.filter(customer_id=customer_id)
        all_enrollment_number = all_enrollment.count()
        Page = InitPage(request.GET.get("page", 1), all_enrollment_number, get_data=get_data)

        return render(request, "Enrollment/Enrollment.html",
                      {"all_enrollment": all_enrollment[Page.start_data_number:Page.end_data_number],
                       "page_html": Page.page_html_func(),
                       "keyword": keyword,
                       "search_field": search_field})

    def post(self, request):
        pk_data = request.POST.get("pk_data")
        pk_data = json.loads(pk_data)

        action = request.POST.get("action")
        if hasattr(self, action):
            return getattr(self, action)(request, pk_data)
        else:
            return reverse("app01:consult_record")

    def bluk_delete(self, request, pk_data):
        with transaction.atomic():
            consult_record_list = models.Enrollment.objects.filter(id__in=pk_data)
            consult_record_list.update(delete_status=True)
        return JsonResponse({"status": 1, "url": reverse("app01:enrollment")})


def add_editor_Enrollment(request, n=None):
    head = "编辑报名表" if n else "添加报名表"
    old_obj = myforms.EnrollmentModelForm(request=request, instance=models.Enrollment.objects.filter(pk=n,
                                                                                                     customer__consultant__username=request.session.get(
                                                                                                         "username")).first())
    if not old_obj:
        return HttpResponse("数据被抢走了!")
    if request.method == "POST":
        next_path = request.GET.get("next")
        old_obj = myforms.EnrollmentModelForm(request=request, data=request.POST,
                                              instance=models.Enrollment.objects.filter(pk=n,
                                                                                        customer__consultant__username=request.session.get(
                                                                                            "username")).first())
        if old_obj.is_valid():
            old_obj.save()
            return redirect("app01:enrollment") if not next_path else redirect(next_path)
        else:
            render(request, "Enrollment/add_editor_Enrollment.html", {"old_obj": old_obj, "head": head})
    return render(request, "Enrollment/add_editor_Enrollment.html", {"old_obj": old_obj, "head": head})


class CourseRecord(View):
    """
    课程记录
    """

    def get(self, request):
        search_field = request.GET.get("field")  # 搜索条件name__contains
        keyword = request.GET.get("keyword")  # 搜索数据 "陈"
        import copy
        get_data = copy.copy(request.GET)  # GET获取的原始数据

        # 单个客户的id
        # customer_id=request.GET.get("customer_id")
        if keyword:
            q = Q()  # 实例化一个对象
            q.children.append([search_field, keyword])  # Q(name__contains="陈")
            all_course_record = models.CourseRecord.objects.filter(q)  # 方式三
        else:
            all_course_record = models.CourseRecord.objects.all()
        # all_course_record=all_course_record.filter(customer__consultant__username=request.session.get("username"))
        # if customer_id:
        #     all_records=all_records.filter(customer_id=customer_id)
        all_course_record_number = all_course_record.count()
        Page = InitPage(request.GET.get("page", 1), all_course_record_number, get_data=get_data)

        return render(request, "CourseRecord/CourseRecord.html",
                      {"all_course_record": all_course_record[Page.start_data_number:Page.end_data_number],
                       "page_html": Page.page_html_func(),
                       "keyword": keyword,
                       "search_field": search_field})

    def post(self, request):
        pk_data = request.POST.get("pk_data")
        pk_data = json.loads(pk_data)

        action = request.POST.get("action")
        if hasattr(self, action):
            return getattr(self, action)(request, pk_data)
        else:
            return reverse("app01:consult_record")

    def bluk_delete(self, request, pk_data):
        with transaction.atomic():
            consult_record_list = models.CourseRecord.objects.filter(id__in=pk_data)
            consult_record_list.update(delete_status=True)
        return JsonResponse({"status": 1, "url": reverse("app01:course_record")})

    def bluk_create_staudy_records(self, request, pk_data):
        with transaction.atomic():
            course_recode_list = models.CourseRecord.objects.filter(id__in=pk_data)
            for course_record in course_recode_list:
                student_objs = course_record.re_class.customer_set.all().exclude(status="unregistered", )
                obj_list = []
                for student in student_objs:
                    obj_list.append(models.StudyRecord(
                        course_record=course_record,
                        student=student
                    ))
                models.StudyRecord.objects.bulk_create(obj_list)

        return JsonResponse({"status": 1, "url": reverse("app01:course_record")})


def add_editor_CourseRecord(request, n=None):
    head = "编辑课程记录表" if n else "添加课程记录表"
    old_obj = myforms.CourseRecordModelForm(instance=models.CourseRecord.objects.filter(pk=n).first())
    if not old_obj:
        return HttpResponse("数据被抢走了!")
    if request.method == "POST":
        next_path = request.GET.get("next")
        old_obj = myforms.CourseRecordModelForm(data=request.POST,
                                                instance=models.CourseRecord.objects.filter(pk=n).first())
        if old_obj.is_valid():
            old_obj.save()
            return redirect("app01:course_record") if not next_path else redirect(next_path)
        else:
            render(request, "Enrollment/add_editor_Enrollment.html", {"old_obj": old_obj, "head": head})
    return render(request, "Enrollment/add_editor_Enrollment.html", {"old_obj": old_obj, "head": head})


class StudyRecord(View):
    def get(self, request, course_id):
        formset_obj = modelformset_factory(model=models.StudyRecord, form=myforms.StudyRecord, extra=0)
        formset_obj = formset_obj(queryset=models.StudyRecord.objects.filter(id=course_id))
        return render(request, "StudyRecord/StudyRecord.html", {"formset_obj": formset_obj})

    def post(self, request, course_id):
        formset_obj = modelformset_factory(model=models.StudyRecord, form=myforms.StudyRecord, extra=0)
        formset_obj = formset_obj(request.POST)
        if formset_obj.is_valid():
            formset_obj.save()
            return redirect("app01:course_record")  # 跳转到本页面可以使用 request.path  直接用反向解析不好使  没法获取(\d)这路径
        else:
            return render(request, "StudyRecord/StudyRecord.html", {"formset_obj": formset_obj})
