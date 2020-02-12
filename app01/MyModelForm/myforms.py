# -*- coding:utf-8 -*-
# Author:cqk
# Data:2019/10/19 11:54
from app01 import models
from django import forms


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({"class": "form-control"})


class ConsultRecordModelForm(forms.ModelForm):
    class Meta:
        model=models.ConsultRecord
        fields="__all__"
        exclude=["delete_status"]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "customer":
                field.queryset=models.Customer.objects.filter(consultant__username=request.session.get("username"))
            if field_name == "consultant":
                field.queryset=models.UserInfo.objects.filter(username=request.session.get("username"))
            field.widget.attrs.update({"class": "form-control"})


class EnrollmentModelForm(forms.ModelForm):
    class Meta:
        model=models.Enrollment
        fields="__all__"
        exclude=["delete_status"]

    def __init__(self, request, *args, **kwargs):
        super(EnrollmentModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "customer":
                field.queryset=models.Customer.objects.filter(consultant__username=request.session.get("username"))
            field.widget.attrs.update({"class": "form-control"})


class CourseRecordModelForm(forms.ModelForm):
    class Meta:
        model=models.CourseRecord
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super(CourseRecordModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class StudyRecord(forms.ModelForm):
    class Meta:
        model=models.StudyRecord
        fields="__all__"
    # def __init__(self,*args,**kwargs):
    #     super(StudyRecord, self).__init__(*args,**kwargs)
