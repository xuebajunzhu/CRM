# -*- coding: utf-8 -*-
"""
Customer management views for CRM system.
Handles customer, consultation records, enrollment, course records, and study records.
"""
import json
import copy

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.views import View
from django.db import transaction
from django.forms.models import modelformset_factory

from app01 import models
from app01.MyModelForm import myforms
from utils.page import InitPage


def home(request):
    """Home page view."""
    return render(request, "customer/home.html", {})


class Customer(View):
    """Customer management view with list and bulk operations."""

    def get(self, request):
        """Display customer list with search and pagination."""
        search_field = request.GET.get("field")
        keyword = request.GET.get("keyword")
        get_data = copy.copy(request.GET)

        # Build query based on search criteria
        if keyword:
            q = Q()
            q.children.append([search_field, keyword])
            all_customer = models.Customer.objects.filter(q)
        else:
            all_customer = models.Customer.objects.all()

        # Filter by customer type (private vs public)
        if request.path == reverse("app01:private_customer"):
            all_customer = all_customer.filter(
                consultant__username=request.session.get("username")
            )
        else:
            all_customer = all_customer.filter(consultant__isnull=True)

        # Pagination
        all_customer_number = all_customer.count()
        page = InitPage(
            request.GET.get("page", 1),
            all_customer_number,
            get_data=get_data
        )

        return render(
            request,
            "customer/customer.html",
            {
                "all_customer": all_customer[page.start_data_number:page.end_data_number],
                "page_html": page.page_html_func(),
                "keyword": keyword,
                "search_field": search_field,
            }
        )

    def post(self, request):
        """Handle bulk actions on customers."""
        pk_data = json.loads(request.POST.get("pk_data"))
        action = request.POST.get("action")

        if hasattr(self, action):
            return getattr(self, action)(request, pk_data)
        return reverse("app01:customer")

    def publish_private(self, request, pk_data):
        """Assign customers to current user."""
        with transaction.atomic():
            customer_obj = models.Customer.objects.select_for_update().filter(
                id__in=pk_data
            )
            user_obj = models.UserInfo.objects.select_for_update().filter(
                username=request.session.get("username")
            ).first()
            customer_obj.update(consultant_id=user_obj.id)
        return JsonResponse({"status": 1, "url": reverse("app01:private_customer")})

    def private_publish(self, request, pk_data):
        """Release customers from current user."""
        with transaction.atomic():
            models.Customer.objects.filter(id__in=pk_data).update(consultant=None)
        return JsonResponse({"status": 1, "url": reverse("app01:customer")})

    def bluk_delete(self, request, pk_data):
        """Bulk delete customers."""
        with transaction.atomic():
            models.Customer.objects.filter(id__in=pk_data).delete()
        return JsonResponse({"status": 1, "url": reverse("app01:customer")})


def add_editor_customer(request, n=None):
    """Add or edit customer record."""
    head = "编辑客户" if n else "添加客户"
    
    if request.method == "POST":
        next_path = request.GET.get("next")
        form = myforms.CustomerModelForm(
            data=request.POST,
            instance=models.Customer.objects.filter(pk=n).first()
        )
        
        if form.is_valid():
            form.save()
            return redirect("app01:customer") if not n else redirect(next_path)
        return render(request, "customer/add_editor_customer.html", {
            "old_obj": form,
            "head": head
        })
    
    old_obj = myforms.CustomerModelForm(
        instance=models.Customer.objects.filter(pk=n).first()
    )
    return render(request, "customer/add_editor_customer.html", {
        "old_obj": old_obj,
        "head": head
    })


class ConsultRecord(View):
    """Consultation record management view."""

    def get(self, request):
        """Display consultation records with search and pagination."""
        search_field = request.GET.get("field")
        keyword = request.GET.get("keyword")
        get_data = copy.copy(request.GET)
        customer_id = request.GET.get("customer_id")

        # Build query based on search criteria
        if keyword:
            q = Q()
            q.children.append([search_field, keyword])
            all_records = models.ConsultRecord.objects.filter(q)
        else:
            all_records = models.ConsultRecord.objects.all()

        # Filter by current user and active status
        all_records = all_records.filter(
            consultant__username=request.session.get("username"),
            delete_status=False
        )

        if customer_id:
            all_records = all_records.filter(customer_id=customer_id)

        # Pagination
        all_records_number = all_records.count()
        page = InitPage(
            request.GET.get("page", 1),
            all_records_number,
            get_data=get_data
        )

        return render(
            request,
            "consult_record/consult_record.html",
            {
                "all_records": all_records[page.start_data_number:page.end_data_number],
                "page_html": page.page_html_func(),
                "keyword": keyword,
                "search_field": search_field,
            }
        )

    def post(self, request):
        """Handle bulk actions on consultation records."""
        pk_data = json.loads(request.POST.get("pk_data"))
        action = request.POST.get("action")

        if hasattr(self, action):
            return getattr(self, action)(request, pk_data)
        return reverse("app01:consult_record")

    def bluk_delete(self, request, pk_data):
        """Soft delete consultation records."""
        with transaction.atomic():
            models.ConsultRecord.objects.filter(
                id__in=pk_data
            ).update(delete_status=True)
        return JsonResponse({"status": 1, "url": reverse("app01:consult_record")})


def add_editor_consult_record(request, n=None):
    """Add or edit consultation record."""
    head = "编辑记录" if n else "添加记录"
    
    # Get existing record with ownership check
    instance = models.ConsultRecord.objects.filter(
        pk=n,
        consultant__username=request.session.get("username")
    ).first()
    
    if not instance and n:
        return HttpResponse("数据被抢走了!")

    if request.method == "POST":
        next_path = request.GET.get("next")
        form = myforms.ConsultRecordModelForm(
            request=request,
            data=request.POST,
            instance=instance
        )
        
        if form.is_valid():
            form.save()
            return redirect("app01:consult_record") if not next_path else redirect(next_path)
        return render(request, "consult_record/add_editor_consult_record.html", {
            "old_obj": form,
            "head": head
        })
    
    form = myforms.ConsultRecordModelForm(request=request, instance=instance)
    return render(request, "consult_record/add_editor_consult_record.html", {
        "old_obj": form,
        "head": head
    })


class Enrollment(View):
    """Enrollment management view."""

    def get(self, request):
        """Display enrollment records with search and pagination."""
        search_field = request.GET.get("field")
        keyword = request.GET.get("keyword")
        get_data = copy.copy(request.GET)

        # Build query based on search criteria
        if keyword:
            q = Q()
            q.children.append([search_field, keyword])
            all_enrollment = models.Enrollment.objects.filter(q)
        else:
            all_enrollment = models.Enrollment.objects.all()

        # Filter by current user's customers and active status
        all_enrollment = all_enrollment.filter(
            customer__consultant__username=request.session.get("username"),
            delete_status=False
        )

        # Pagination
        all_enrollment_number = all_enrollment.count()
        page = InitPage(
            request.GET.get("page", 1),
            all_enrollment_number,
            get_data=get_data
        )

        return render(
            request,
            "Enrollment/Enrollment.html",
            {
                "all_enrollment": all_enrollment[page.start_data_number:page.end_data_number],
                "page_html": page.page_html_func(),
                "keyword": keyword,
                "search_field": search_field,
            }
        )

    def post(self, request):
        """Handle bulk actions on enrollments."""
        pk_data = json.loads(request.POST.get("pk_data"))
        action = request.POST.get("action")

        if hasattr(self, action):
            return getattr(self, action)(request, pk_data)
        return reverse("app01:consult_record")

    def bluk_delete(self, request, pk_data):
        """Soft delete enrollment records."""
        with transaction.atomic():
            models.Enrollment.objects.filter(
                id__in=pk_data
            ).update(delete_status=True)
        return JsonResponse({"status": 1, "url": reverse("app01:enrollment")})


def add_editor_Enrollment(request, n=None):
    """Add or edit enrollment record."""
    head = "编辑报名表" if n else "添加报名表"
    
    # Get existing record with ownership check
    instance = models.Enrollment.objects.filter(
        pk=n,
        customer__consultant__username=request.session.get("username")
    ).first()
    
    if not instance and n:
        return HttpResponse("数据被抢走了!")

    if request.method == "POST":
        next_path = request.GET.get("next")
        form = myforms.EnrollmentModelForm(
            request=request,
            data=request.POST,
            instance=instance
        )
        
        if form.is_valid():
            form.save()
            return redirect("app01:enrollment") if not next_path else redirect(next_path)
        return render(request, "Enrollment/add_editor_Enrollment.html", {
            "old_obj": form,
            "head": head
        })
    
    form = myforms.EnrollmentModelForm(request=request, instance=instance)
    return render(request, "Enrollment/add_editor_Enrollment.html", {
        "old_obj": form,
        "head": head
    })


class CourseRecord(View):
    """Course record management view."""

    def get(self, request):
        """Display course records with search and pagination."""
        search_field = request.GET.get("field")
        keyword = request.GET.get("keyword")
        get_data = copy.copy(request.GET)

        # Build query based on search criteria
        if keyword:
            q = Q()
            q.children.append([search_field, keyword])
            all_course_record = models.CourseRecord.objects.filter(q)
        else:
            all_course_record = models.CourseRecord.objects.all()

        # Pagination
        all_course_record_number = all_course_record.count()
        page = InitPage(
            request.GET.get("page", 1),
            all_course_record_number,
            get_data=get_data
        )

        return render(
            request,
            "CourseRecord/CourseRecord.html",
            {
                "all_course_record": all_course_record[page.start_data_number:page.end_data_number],
                "page_html": page.page_html_func(),
                "keyword": keyword,
                "search_field": search_field,
            }
        )

    def post(self, request):
        """Handle bulk actions on course records."""
        pk_data = json.loads(request.POST.get("pk_data"))
        action = request.POST.get("action")

        if hasattr(self, action):
            return getattr(self, action)(request, pk_data)
        return reverse("app01:consult_record")

    def bluk_delete(self, request, pk_data):
        """Soft delete course records."""
        with transaction.atomic():
            models.CourseRecord.objects.filter(
                id__in=pk_data
            ).update(delete_status=True)
        return JsonResponse({"status": 1, "url": reverse("app01:course_record")})

    def bluk_create_staudy_records(self, request, pk_data):
        """Bulk create study records for selected course records."""
        with transaction.atomic():
            course_record_list = models.CourseRecord.objects.filter(id__in=pk_data)
            
            for course_record in course_record_list:
                student_objs = course_record.re_class.customer_set.all().exclude(
                    status="unregistered"
                )
                
                obj_list = [
                    models.StudyRecord(course_record=course_record, student=student)
                    for student in student_objs
                ]
                
                models.StudyRecord.objects.bulk_create(obj_list)

        return JsonResponse({"status": 1, "url": reverse("app01:course_record")})


def add_editor_CourseRecord(request, n=None):
    """Add or edit course record."""
    head = "编辑课程记录表" if n else "添加课程记录表"
    
    instance = models.CourseRecord.objects.filter(pk=n).first()
    
    if not instance and n:
        return HttpResponse("数据被抢走了!")

    if request.method == "POST":
        next_path = request.GET.get("next")
        form = myforms.CourseRecordModelForm(
            data=request.POST,
            instance=instance
        )
        
        if form.is_valid():
            form.save()
            return redirect("app01:course_record") if not next_path else redirect(next_path)
        return render(request, "CourseRecord/add_editor_CourseRecord.html", {
            "old_obj": form,
            "head": head
        })
    
    form = myforms.CourseRecordModelForm(instance=instance)
    return render(request, "CourseRecord/add_editor_CourseRecord.html", {
        "old_obj": form,
        "head": head
    })


class StudyRecord(View):
    """Study record management view."""

    def get(self, request, course_id):
        """Display study records for a specific course."""
        formset_factory = modelformset_factory(
            model=models.StudyRecord,
            form=myforms.StudyRecord,
            extra=0
        )
        formset = formset_factory(
            queryset=models.StudyRecord.objects.filter(id=course_id)
        )
        return render(request, "StudyRecord/StudyRecord.html", {
            "formset_obj": formset
        })

    def post(self, request, course_id):
        """Update study records."""
        formset_factory = modelformset_factory(
            model=models.StudyRecord,
            form=myforms.StudyRecord,
            extra=0
        )
        formset = formset_factory(request.POST)
        
        if formset.is_valid():
            formset.save()
            return redirect("app01:course_record")
        return render(request, "StudyRecord/StudyRecord.html", {
            "formset_obj": formset
        })
