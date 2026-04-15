"""
URL configuration for app01 application.
Defines URL patterns for authentication and customer management views.
"""
from django.urls import path, re_path

from app01.views import auth, customer

urlpatterns = [
    # Authentication URLs
    path('login/', auth.login, name='login'),
    path('logout/', auth.logout, name='logout'),
    path('register/', auth.register, name='register'),

    # Home page
    path('home/', customer.home, name='home'),

    # Customer management URLs
    path('customer/', customer.Customer.as_view(), name='customer'),
    path('private_customer/', customer.Customer.as_view(), name='private_customer'),
    path('addcustomer/', customer.add_editor_customer, name='addcustomer'),
    re_path(r'^editorcustomer/(\d+)/$', customer.add_editor_customer, name='editorcustomer'),

    # Consultation record URLs
    path('consult_record/', customer.Consult_Record.as_view(), name='consult_record'),
    re_path(r'^editor_consult_record/(\d+)/$', customer.add_editor_consult_record, name='editor_consult_record'),
    path('add_consult_record/', customer.add_editor_consult_record, name='add_consult_record'),

    # Enrollment URLs
    path('enrollment/', customer.Enrollment.as_view(), name='enrollment'),
    re_path(r'^editor_enrollment/(\d+)/$', customer.add_editor_Enrollment, name='editor_enrollment'),
    path('add_enrollment/', customer.add_editor_Enrollment, name='add_enrollment'),

    # Course record URLs
    path('course_record/', customer.CourseRecord.as_view(), name='course_record'),
    re_path(r'^editor_course_record/(\d+)/$', customer.add_editor_CourseRecord, name='editor_course_record'),
    path('add_course_record/', customer.add_editor_CourseRecord, name='add_course_record'),

    # Study record URLs
    re_path(r'^study_record/(\d+)/$', customer.StudyRecord.as_view(), name='study_record'),
]
