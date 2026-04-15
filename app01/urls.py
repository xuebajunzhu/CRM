# -*- coding: utf-8 -*-
"""
URL configuration for app01 application.
Defines URL patterns for authentication and customer management views.
"""
from django.conf.urls import url

from app01.views import auth, customer

urlpatterns = [
    # Authentication URLs
    url(r"^login/", auth.login, name="login"),
    url(r"^logout/", auth.logout, name="logout"),
    url(r"^register/", auth.register, name="register"),

    # Home page
    url(r"^home/", customer.home, name="home"),
    
    # Customer management URLs
    url(r"^customer/", customer.Customer.as_view(), name="customer"),
    url(r"^private_customer/", customer.Customer.as_view(), name="private_customer"),
    url(r"^addcustomer/", customer.add_editor_customer, name="addcustomer"),
    url(r"^editorcustomer/(\d+)/", customer.add_editor_customer, name="editorcustomer"),
    
    # Consultation record URLs
    url(r"^consult_record/", customer.Consult_Record.as_view(), name="consult_record"),
    url(r"^editor_consult_record/(\d+)/", customer.add_editor_consult_record, name="editor_consult_record"),
    url(r"^add_consult_record/", customer.add_editor_consult_record, name="add_consult_record"),
    
    # Enrollment URLs
    url(r"^enrollment/", customer.Enrollment.as_view(), name="enrollment"),
    url(r"^editor_enrollment/(\d+)/", customer.add_editor_Enrollment, name="editor_enrollment"),
    url(r"^add_enrollment/", customer.add_editor_Enrollment, name="add_enrollment"),
    
    # Course record URLs
    url(r"^course_record/", customer.CourseRecord.as_view(), name="course_record"),
    url(r"^editor_course_record/(\d+)/", customer.add_editor_CourseRecord, name="editor_course_record"),
    url(r"^add_course_record/", customer.add_editor_CourseRecord, name="add_course_record"),
    
    # Study record URLs
    url(r"^study_record/(\d+)/", customer.StudyRecord.as_view(), name="study_record"),
]
