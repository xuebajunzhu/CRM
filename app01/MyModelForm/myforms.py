# -*- coding: utf-8 -*-
"""
Model forms for CRM application.
Provides form classes with consistent styling and custom field handling.
"""
from django import forms
from multiselectfield.forms.fields import MultiSelectFormField

from app01 import models


class CustomerModelForm(forms.ModelForm):
    """ModelForm for Customer model with Bootstrap styling."""
    
    class Meta:
        model = models.Customer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap form-control class to all fields except MultiSelectField
        for field_name, field in self.fields.items():
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({"class": "form-control"})


class ConsultRecordModelForm(forms.ModelForm):
    """ModelForm for ConsultRecord with user-specific filtering."""
    
    class Meta:
        model = models.ConsultRecord
        fields = "__all__"
        exclude = ["delete_status"]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username = request.session.get("username")
        
        for field_name, field in self.fields.items():
            # Filter customer field to show only current user's customers
            if field_name == "customer":
                field.queryset = models.Customer.objects.filter(
                    consultant__username=username
                )
            # Set consultant field to current user only
            elif field_name == "consultant":
                field.queryset = models.UserInfo.objects.filter(
                    username=username
                )
            # Add Bootstrap styling
            field.widget.attrs.update({"class": "form-control"})


class EnrollmentModelForm(forms.ModelForm):
    """ModelForm for Enrollment with user-specific customer filtering."""
    
    class Meta:
        model = models.Enrollment
        fields = "__all__"
        exclude = ["delete_status"]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username = request.session.get("username")
        
        for field_name, field in self.fields.items():
            # Filter customer field to show only current user's customers
            if field_name == "customer":
                field.queryset = models.Customer.objects.filter(
                    consultant__username=username
                )
            # Add Bootstrap styling
            field.widget.attrs.update({"class": "form-control"})


class CourseRecordModelForm(forms.ModelForm):
    """ModelForm for CourseRecord with Bootstrap styling."""
    
    class Meta:
        model = models.CourseRecord
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap form-control class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class StudyRecord(forms.ModelForm):
    """ModelForm for StudyRecord batch editing."""
    
    class Meta:
        model = models.StudyRecord
        fields = "__all__"
