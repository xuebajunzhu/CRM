"""
URL configuration for app01 application.
Defines URL patterns for authentication and customer management views.
"""
from django.urls import path

from app01.views import auth, customer

app_name = 'app01'

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
    path('editorcustomer/<int:pk>/', customer.add_editor_customer, name='editorcustomer'),

    # Consultation record URLs
    path('consult_record/', customer.ConsultRecord.as_view(), name='consult_record'),
    path('editor_consult_record/<int:pk>/', customer.add_editor_consult_record, name='editor_consult_record'),
    path('add_consult_record/', customer.add_editor_consult_record, name='add_consult_record'),

    # Enrollment URLs
    path('enrollment/', customer.Enrollment.as_view(), name='enrollment'),
    path('editor_enrollment/<int:pk>/', customer.add_editor_Enrollment, name='editor_enrollment'),
    path('add_enrollment/', customer.add_editor_Enrollment, name='add_enrollment'),

    # Course record URLs
    path('course_record/', customer.CourseRecord.as_view(), name='course_record'),
    path('editor_course_record/<int:pk>/', customer.add_editor_CourseRecord, name='editor_course_record'),
    path('add_course_record/', customer.add_editor_CourseRecord, name='add_course_record'),

    # Study record URLs
    path('study_record/<int:course_id>/', customer.StudyRecord.as_view(), name='study_record'),
]
