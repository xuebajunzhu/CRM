from django.contrib import admin
from app01 import models


# Register your models here.
class UserInfo(admin.ModelAdmin):
    list_display=["id", "username", "telephone"]
class CourseRecordAdmin(admin.ModelAdmin):
    list_display=["id","day_num","course_title","re_class","teacher"]
    list_editable = ["day_num","course_title","re_class","teacher"]

admin.site.register(models.UserInfo, UserInfo)
admin.site.register(models.Customer)
admin.site.register(models.Department)
admin.site.register(models.ClassList)
admin.site.register(models.Campuses)

admin.site.register(models.ConsultRecord)
admin.site.register(models.CourseRecord,CourseRecordAdmin)

admin.site.register(models.Enrollment)
admin.site.register(models.StudyRecord)

