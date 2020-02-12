# -*- coding:utf-8 -*-
# Author:cqk
# Data:2019/10/18 18:06
from app01.views import auth
from app01.views import customer

from django.conf.urls import url

urlpatterns = [
    url("^login/", auth.login, name="login"),
    url("^logout/", auth.logout, name="logout"),
    url("^register/", auth.register, name="register"),

    url("^home/", customer.home, name="home"),
    # 客户信息展示
    url("^customer/", customer.Customer.as_view(), name="customer"),
    url("^private_customer/", customer.Customer.as_view(), name="private_customer"),
    url("^addcustomer/", customer.add_editor_customer, name="addcustomer"),
    url("^editorcustomer/(\d+)/", customer.add_editor_customer, name="editorcustomer"),
    # 跟进记录
    url("^consult_record/", customer.Consult_Record.as_view(), name="consult_record"),
    url("^editor_consult_record/(\d+)/", customer.add_editor_consult_record, name="editor_consult_record"),
    url("^add_consult_record/", customer.add_editor_consult_record, name="add_consult_record"),
    # 报名报
    url("^enrollment/", customer.Enrollment.as_view(), name="enrollment"),
    url("^editor_enrollment/(\d+)/", customer.add_editor_Enrollment, name="editor_enrollment"),
    url("^add_enrollment/", customer.add_editor_Enrollment, name="add_enrollment"),
    # 课程记录展示
    url("^course_record/", customer.CourseRecord.as_view(), name="course_record"),
    url("^editor_course_record/(\d+)/", customer.add_editor_CourseRecord, name="editor_course_record"),
    url("^add_course_record/", customer.add_editor_CourseRecord, name="add_course_record"),
    # 学习记录详情
    url("^study_record/(\d+)/", customer.StudyRecord.as_view(), name="study_record"),
    url("^editor_study_record/(\d+)/", customer.add_editor_CourseRecord, name="editor_study_record"),
    url("^add_study_record/", customer.add_editor_CourseRecord, name="add_study_record"),
]
