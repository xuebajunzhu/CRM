"""
Database models for CRM application.
Defines data structures for users, customers, consultations, enrollments, and courses.
"""
from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator, MaxLengthValidator
from multiselectfield import MultiSelectField
from django.utils.safestring import mark_safe


# Course choices
COURSE_CHOICES = (
    ('LinuxL', 'Linux 中高级'),
    ('PythonFullStack', 'Python 高级全栈开发'),
)

# Class type choices
CLASS_TYPE_CHOICES = (
    ('fulltime', '脱产班'),
    ('online', '网络班'),
    ('weekend', '周末班'),
)

# Customer source choices
SOURCE_CHOICES = (
    ('qq', "QQ 群"),
    ('referral', "内部转介绍"),
    ('website', "官方网站"),
    ('baidu_ads', "百度推广"),
    ('office_direct', "直接上门"),
    ('WoM', "口碑"),
    ('public_class', "公开课"),
    ('website_luffy', "路飞官网"),
    ('others', "其它"),
)

# Enrollment status choices
ENROLL_STATUS_CHOICES = (
    ('signed', "已报名"),
    ('unregistered', "未报名"),
    ('studying', '学习中'),
    ('paid_in_full', "学费已交齐")
)

# Consultation seek status choices
SEEK_STATUS_CHOICES = (
    ('A', '近期无报名计划'),
    ('B', '1 个月内报名'),
    ('C', '2 周内报名'),
    ('D', '1 周内报名'),
    ('E', '定金'),
    ('F', '到班'),
    ('G', '全款'),
    ('H', '无效'),
)

# Payment type choices
PAY_TYPE_CHOICES = (
    ('deposit', "订金/报名费"),
    ('tuition', "学费"),
    ('transfer', "转班"),
    ('dropout', "退学"),
    ('refund', "退款"),
)

# Attendance choices
ATTENDANCE_CHOICES = (
    ('checked', "已签到"),
    ('vacate', "请假"),
    ('late', "迟到"),
    ('absence', "缺勤"),
    ('leave_early', "早退"),
)

# Score choices
SCORE_CHOICES = (
    (100, 'A+'),
    (90, 'A'),
    (85, 'B+'),
    (80, 'B'),
    (70, 'B-'),
    (60, 'C+'),
    (50, 'C'),
    (40, 'C-'),
    (0, ' D'),
    (-1, 'N/A'),
    (-100, 'COPY'),
    (-1000, 'FAIL'),
)


class UserInfo(models.Model):
    """User information table for employees (sales, teachers, administrators)."""
    
    username = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=32)
    telephone = models.CharField(max_length=11)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    depart = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "用户信息表"
        verbose_name_plural = "用户信息表"

    def __str__(self):
        return self.username


class Department(models.Model):
    """Department table for organizational structure."""
    
    name = models.CharField(max_length=32)
    count = models.IntegerField()

    class Meta:
        ordering = ["id"]
        verbose_name = "部门表"
        verbose_name_plural = "部门表"

    def __str__(self):
        return self.name


class CustomerManager(models.Manager):
    """Custom manager for Customer model with soft delete support."""
    
    def get_queryset(self):
        return super().get_queryset().filter(delete_status=False)
    
    def all_with_deleted(self):
        return super().get_queryset()


class Customer(models.Model):
    """Customer table for tracking potential and enrolled students."""
    
    qq = models.CharField(
        verbose_name='QQ',
        max_length=64,
        unique=True,
        help_text='QQ 号必须唯一'
    )
    qq_name = models.CharField('QQ 昵称', max_length=64, blank=True, null=True)
    name = models.CharField(
        '姓名',
        max_length=32,
        blank=True,
        null=True,
        help_text='学员报名后，请改为真实姓名'
    )
    sex = models.CharField(
        "性别",
        choices=[('male', '男'), ('female', '女')],
        max_length=16,
        default='male',
        blank=True,
        null=True
    )
    birthday = models.DateField(
        '出生日期',
        default=None,
        blank=True,
        null=True,
        help_text="格式 yyyy-mm-dd"
    )
    phone = models.CharField(
        '手机号',
        max_length=11,
        blank=True,
        null=True,
        validators=[
            RegexValidator(r'^1[3-9]\d{9}$', '手机号格式不正确')
        ]
    )
    source = models.CharField(
        '客户来源',
        max_length=64,
        choices=SOURCE_CHOICES,
        default='qq'
    )
    introduce_from = models.ForeignKey(
        'self',
        verbose_name="转介绍自学员",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    course = MultiSelectField("咨询课程", choices=COURSE_CHOICES)
    class_type = models.CharField(
        "班级类型",
        max_length=64,
        choices=CLASS_TYPE_CHOICES,
        default='fulltime'
    )
    customer_note = models.TextField("客户备注", blank=True, null=True)
    status = models.CharField(
        "状态",
        choices=ENROLL_STATUS_CHOICES,
        max_length=64,
        default="unregistered",
        help_text="选择客户此时的状态"
    )
    date = models.DateTimeField("咨询日期", auto_now_add=True)
    last_consult_date = models.DateField("最后跟进日期", auto_now_add=True)
    next_date = models.DateField("预计再次跟进时间", blank=True, null=True)
    consultant = models.ForeignKey(
        'UserInfo',
        verbose_name="销售",
        related_name='customers',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    class_list = models.ManyToManyField(
        'ClassList',
        verbose_name="已报班级",
        blank=True
    )
    deal_date = models.DateField(null=True, blank=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)

    objects = CustomerManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['id']
        verbose_name = '客户信息表'
        verbose_name_plural = '客户信息表'

    def __str__(self):
        return f"{self.name}:{self.qq}"

    def status_show(self):
        """Display status with color coding."""
        status_color = {
            'paid_in_full': 'green',
            'unregistered': 'red',
            'studying': 'lightblue',
            'signed': 'yellow',
        }
        color = status_color.get(self.status, 'white')
        return mark_safe(
            f"<span style='background-color:{color}'>{self.get_status_display()}</span>"
        )

    def get_classlist(self):
        """Get enrolled class list as comma-separated string."""
        class_names = [str(cls) for cls in self.class_list.all()]
        return mark_safe(",".join(class_names))


class Campuses(models.Model):
    """Campus locations table."""
    
    name = models.CharField(verbose_name='校区', max_length=64)
    address = models.CharField(
        verbose_name='详细地址',
        max_length=512,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = '校区表'
        verbose_name_plural = '校区表'

    def __str__(self):
        return self.name


class ClassList(models.Model):
    """Class/batch information table."""
    
    course = models.CharField("课程名称", max_length=64, choices=COURSE_CHOICES)
    semester = models.IntegerField("学期")
    campuses = models.ForeignKey(
        'Campuses',
        verbose_name="校区",
        on_delete=models.CASCADE
    )
    price = models.IntegerField("学费", default=10000)
    memo = models.CharField('说明', blank=True, null=True, max_length=100)
    start_date = models.DateField("开班日期")
    graduate_date = models.DateField("结业日期", blank=True, null=True)
    teachers = models.ManyToManyField(
        'UserInfo',
        verbose_name="老师"
    )
    class_type = models.CharField(
        choices=CLASS_TYPE_CHOICES,
        max_length=64,
        verbose_name='班额及类型',
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ("course", "semester", 'campuses')
        ordering = ['id']
        verbose_name = '班级表'
        verbose_name_plural = '班级表'

    def __str__(self):
        return f"{self.get_course_display()}{self.semester}期 ({self.campuses})"


class ConsultRecord(models.Model):
    """Consultation/follow-up record table."""
    
    customer = models.ForeignKey(
        'Customer',
        verbose_name="所咨询客户",
        on_delete=models.CASCADE
    )
    note = models.TextField(verbose_name="跟进内容...")
    status = models.CharField(
        "跟进状态",
        max_length=8,
        choices=SEEK_STATUS_CHOICES,
        help_text="选择客户此时的状态"
    )
    consultant = models.ForeignKey(
        "UserInfo",
        verbose_name="跟进人",
        related_name='records',
        on_delete=models.CASCADE
    )
    date = models.DateTimeField("跟进日期", auto_now_add=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)

    class Meta:
        ordering = ['id']
        verbose_name = '跟进记录表'
        verbose_name_plural = '跟进记录表'

    def __str__(self):
        return f"{self.customer.name}<-- {self.consultant.username}"


class Enrollment(models.Model):
    """Enrollment/registration record table."""
    
    why_us = models.TextField(
        "为什么报名",
        max_length=1024,
        blank=True,
        null=True,
        default=None
    )
    your_expectation = models.TextField(
        "学完想达到的具体期望",
        max_length=1024,
        blank=True,
        null=True
    )
    contract_approved = models.BooleanField(
        "审批通过",
        help_text="在审阅完学员的资料无误后勾选此项，合同即生效",
        default=False
    )
    enrolled_date = models.DateTimeField(auto_now_add=True, verbose_name="报名日期")
    memo = models.TextField('备注', blank=True, null=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)
    customer = models.ForeignKey(
        'Customer',
        verbose_name='客户名称',
        on_delete=models.CASCADE
    )
    school = models.ForeignKey(
        'Campuses',
        on_delete=models.CASCADE
    )
    enrolment_class = models.ForeignKey(
        "ClassList",
        verbose_name="所报班级",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('enrolment_class', 'customer')
        ordering = ['id']
        verbose_name = '报名表'
        verbose_name_plural = '报名表'

    def __str__(self):
        return self.customer.name


class CourseRecord(models.Model):
    """Course session record table."""
    
    day_num = models.IntegerField(
        "节次",
        help_text="此处填写第几节课或第几天课程...,必须为数字"
    )
    date = models.DateField(auto_now_add=True, verbose_name="上课日期")
    course_title = models.CharField(
        '本节课程标题',
        max_length=64,
        blank=True,
        null=True
    )
    course_memo = models.TextField(
        '本节课程内容',
        max_length=300,
        blank=True,
        null=True
    )
    has_homework = models.BooleanField(default=True, verbose_name="本节有作业")
    homework_title = models.CharField(
        '本节作业标题',
        max_length=64,
        blank=True,
        null=True
    )
    homework_memo = models.TextField(
        '作业描述',
        max_length=500,
        blank=True,
        null=True
    )
    scoring_point = models.TextField(
        '得分点',
        max_length=300,
        blank=True,
        null=True
    )
    re_class = models.ForeignKey(
        'ClassList',
        verbose_name="班级",
        on_delete=models.CASCADE
    )
    teacher = models.ForeignKey(
        'UserInfo',
        verbose_name="讲师",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('re_class', 'day_num')
        ordering = ["id"]
        verbose_name = "课程记录表"
        verbose_name_plural = "课程记录表"

    def __str__(self):
        return str(self.day_num)


class StudyRecord(models.Model):
    """Student study/attendance record for each course session."""
    
    attendance = models.CharField(
        "考勤",
        choices=ATTENDANCE_CHOICES,
        default="checked",
        max_length=64
    )
    score = models.IntegerField(
        "本节成绩",
        choices=SCORE_CHOICES,
        default=-1
    )
    homework_note = models.CharField(
        max_length=255,
        verbose_name='作业批语',
        blank=True,
        null=True
    )
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(
        "备注",
        max_length=255,
        blank=True,
        null=True
    )
    homework = models.FileField(
        verbose_name='作业文件',
        blank=True,
        null=True,
        default=None,
        upload_to='homeworks/',
        validators=[
            FileExtensionValidator(['pdf', 'doc', 'docx', 'zip', 'txt']),
        ]
    )
    course_record = models.ForeignKey(
        'CourseRecord',
        verbose_name="某节课程",
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        'Customer',
        verbose_name="学员",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('course_record', 'student')
        ordering = ["id"]
        verbose_name = "学习记录"
        verbose_name_plural = "学习记录"

    def __str__(self):
        return f"{self.student.name}:{self.course_record.day_num}"
