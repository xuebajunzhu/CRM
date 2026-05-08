#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django CRM 测试数据生成脚本
功能：批量生成真实的测试数据并插入数据库
用法：python generate_test_data.py
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRM01.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from app01 import models


def generate_departments():
    """生成部门数据"""
    print("正在生成部门...")
    
    departments = [
        ('销售部', 10),
        ('教学部', 8),
        ('管理部', 5),
        ('技术部', 6)
    ]
    
    dept_objects = []
    for name, count in departments:
        dept, created = models.Department.objects.get_or_create(
            name=name,
            defaults={'count': count}
        )
        dept_objects.append(dept)
    
    print(f"✓ 已生成 {len(dept_objects)} 个部门")
    return dept_objects


def generate_users(departments, count=10):
    """生成用户数据"""
    print(f"正在生成 {count} 个用户...")
    
    users = []
    
    # 创建管理员
    admin, created = models.UserInfo.objects.get_or_create(
        username='admin',
        defaults={
            'password': make_password('admin123'),
            'telephone': '13800138000',
            'email': 'admin@crm.com',
            'is_active': True,
            'depart_id': departments[2].id if len(departments) > 2 else None
        }
    )
    users.append(admin)
    
    # 生成其他用户
    names = [
        '张三', '李四', '王五', '赵六', '孙七', '周八', '吴九', '郑十',
        '陈晨', '林峰', '黄磊', '徐静', '高远', '马超', '朱莉', '秦岭'
    ]
    
    for i in range(count - 1):
        username = f"user{i+1:03d}"
        phone = f"1{random.randint(3, 9)}{random.randint(100000000, 999999999)}"
        
        user, created = models.UserInfo.objects.get_or_create(
            username=username,
            defaults={
                'password': make_password('pass123'),
                'telephone': phone,
                'email': f"{username}@crm.com",
                'is_active': True,
                'depart_id': random.choice(departments).id
            }
        )
        users.append(user)
    
    print(f"✓ 已生成 {len(users)} 个用户")
    return users


def generate_campuses(count=3):
    """生成校区数据"""
    print(f"正在生成 {count} 个校区...")
    
    campuses_data = [
        ('北京校区', '北京市海淀区中关村大街 1 号'),
        ('上海校区', '上海市浦东新区张江高科技园区'),
        ('广州校区', '广州市天河区天河路 100 号'),
        ('深圳校区', '深圳市南山区科技园南区'),
        ('武汉校区', '武汉市洪山区光谷广场'),
    ]
    
    campuses = []
    for i in range(min(count, len(campuses_data))):
        name, address = campuses_data[i]
        campus, created = models.Campuses.objects.get_or_create(
            name=name,
            defaults={'address': address}
        )
        campuses.append(campus)
    
    print(f"✓ 已生成 {len(campuses)} 个校区")
    return campuses


def generate_classes(users, campuses, count=8):
    """生成班级数据"""
    print(f"正在生成 {count} 个班级...")
    
    courses = [
        ('LinuxL', 'Linux 中高级'),
        ('PythonFullStack', 'Python 高级全栈开发'),
    ]
    
    teachers = users[1:4]  # 使用前几个用户作为老师
    
    classes = []
    start_date = datetime(2024, 1, 15)
    
    for i in range(count):
        course_code, course_name = courses[i % len(courses)]
        semester = (i // len(courses)) + 1
        
        class_obj, created = models.ClassList.objects.get_or_create(
            course=course_code,
            semester=semester,
            campuses_id=campuses[0].id if campuses else 1,
            defaults={
                'price': 10000 + random.randint(0, 5000),
                'start_date': start_date + timedelta(days=i * 15),
                'graduate_date': start_date + timedelta(days=i * 15 + 150),
                'class_type': random.choice(['fulltime', 'online', 'weekend']),
            }
        )
        # 关联老师
        class_obj.teachers.add(random.choice(teachers))
        classes.append(class_obj)
    
    print(f"✓ 已生成 {len(classes)} 个班级")
    return classes


def generate_course_records(classes, users, per_class=10):
    """生成课程记录"""
    print(f"正在生成课程记录 (每班级 {per_class} 条)...")
    
    course_titles = {
        'LinuxL': [
            'Linux 系统概述与安装', '文件与目录管理', '用户与权限管理',
            '进程管理与系统监控', '网络配置与服务', 'Shell 脚本编程',
            '磁盘管理与 LVM', '系统安全与防火墙', '日志管理与分析', '综合实战'
        ],
        'PythonFullStack': [
            'Python 基础语法', '数据类型与结构', '函数与模块',
            '面向对象编程', '文件操作与异常处理', '网络编程',
            '数据库编程', 'Django 框架入门', 'RESTful API 开发', '项目实战'
        ],
    }
    
    records = []
    for class_obj in classes:
        titles = course_titles.get(class_obj.course, course_titles['PythonFullStack'])
        teacher = list(class_obj.teachers.all())[0] if class_obj.teachers.all() else users[0]
        
        for day in range(1, per_class + 1):
            record, created = models.CourseRecord.objects.get_or_create(
                re_class_id=class_obj.id,
                day_num=day,
                defaults={
                    'date': class_obj.start_date + timedelta(days=(day - 1) * 2),
                    'course_title': titles[(day - 1) % len(titles)],
                    'teacher_id': teacher.id,
                    'has_homework': True,
                    'homework_title': f'第{day}章练习题',
                }
            )
            records.append(record)
    
    print(f"✓ 已生成 {len(records)} 条课程记录")
    return records


def generate_customers(users, count=30):
    """生成客户数据"""
    print(f"正在生成 {count} 个客户...")
    
    sources = [s[0] for s in models.SOURCE_CHOICES]
    courses = [c[0] for c in models.COURSE_CHOICES]
    statuses = [s[0] for s in models.ENROLL_STATUS_CHOICES]
    
    names = [
        '张伟', '李娜', '王强', '刘芳', '陈杰', '杨敏', '赵磊', '孙丽',
        '周涛', '吴静', '郑浩', '冯雪', '陈晨', '褚明', '卫华', '蒋琳',
        '沈刚', '韩梅', '杨梅', '林峰', '何平', '高翔', '梁勇', '宋佳',
        '唐军', '许婷', '邓超', '范伟', '钟丽', '潘强', '董明', '袁华',
    ]
    
    consultants = users[1:6]  # 使用前几个用户作为销售
    
    customers = []
    for i in range(count):
        name = names[i % len(names)]
        qq = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        phone = f"1{random.randint(3, 9)}{random.randint(100000000, 999999999)}"
        
        customer, created = models.Customer.objects.get_or_create(
            qq=qq,
            defaults={
                'name': name,
                'phone': phone,
                'source': random.choice(sources),
                'course': [random.choice(courses)],
                'consultant_id': random.choice(consultants).id if consultants else None,
                'status': random.choice(statuses),
                'delete_status': False,
                'sex': random.choice(['male', 'female']),
                'class_type': random.choice(['fulltime', 'online', 'weekend']),
            }
        )
        customers.append(customer)
    
    print(f"✓ 已生成 {len(customers)} 个客户")
    return customers


def generate_consult_records(customers, users, avg_records_per_customer=2):
    """生成咨询记录"""
    print("正在生成咨询记录...")
    
    statuses = [s[0] for s in models.SEEK_STATUS_CHOICES]
    
    contents = [
        '客户对课程很感兴趣，想了解就业情况',
        '已发送课程大纲和学费信息，等待回复',
        '客户是朋友介绍来的，想深入学习',
        '预约了来校区参观',
        '客户担心自己零基础学不会',
        '推荐了免费试听课，客户表示考虑',
        '客户之前学过一些相关知识',
        '已安排技术老师进行水平测试',
        '客户对行业前景有疑问',
        '分享了行业报告，客户比较满意',
        '客户想转行，需要了解课程体系',
        '介绍了就业服务和合作企业',
        '客户是在校大学生，想提前学习',
        '推荐了周末班，时间比较合适',
        '客户有编程基础，想提升技能',
        '已报名课程，准备入学',
        '客户对比了几家机构',
        '强调了我们的师资和就业优势',
    ]
    
    consultants = users[1:6]
    
    records = []
    base_date = datetime(2024, 1, 10)
    
    for customer in customers:
        num_records = random.randint(1, avg_records_per_customer + 1)
        
        for j in range(num_records):
            record = models.ConsultRecord.objects.create(
                customer_id=customer.id,
                note=random.choice(contents),
                status=random.choice(statuses),
                consultant_id=random.choice(consultants).id if consultants else None,
                delete_status=False
            )
            records.append(record)
    
    print(f"✓ 已生成 {len(records)} 条咨询记录")
    return records


def generate_study_records(customers, course_records, count=24):
    """生成学习记录"""
    print(f"正在生成 {count} 条学习记录...")
    
    scores = [s[0] for s in models.SCORE_CHOICES]
    attendances = [a[0] for a in models.ATTENDANCE_CHOICES]
    
    homework_notes = [
        '已完成所有章节习题', '作业完成得很认真', '代码规范有待加强',
        '逻辑思维清晰', '需要多练习基础', '进步明显', '创意不错',
        '理解透彻', '可以担任小组长', '动手能力强', '专业素养高',
    ]
    
    notes = [
        '学习态度认真，进步明显', '逻辑思维能力强', '需要多练习类的设计',
        '有相关经验', '整体表现优秀', '需要加强练习', '继续保持',
        '有编程天赋', '数学基础好', '潜力很大', '非常优秀',
    ]
    
    records = []
    for i in range(count):
        student = customers[i % len(customers)]
        course_record = course_records[i % len(course_records)]
        
        score = random.choice(scores[:5])  # 主要生成较好的成绩
        
        try:
            record = models.StudyRecord.objects.create(
                student_id=student.id,
                course_record_id=course_record.id,
                attendance=random.choice(attendances[:2]),  # 主要是已签到
                score=score,
                homework_note=random.choice(homework_notes),
                note=random.choice(notes),
            )
            records.append(record)
        except Exception as e:
            # 可能因为唯一键冲突而失败，跳过
            pass
    
    print(f"✓ 已生成 {len(records)} 条学习记录")
    return records


def print_statistics():
    """打印数据统计"""
    print("\n" + "=" * 50)
    print("数据统计")
    print("=" * 50)
    
    print(f"部门总数：{models.Department.objects.count()}")
    print(f"用户总数：{models.UserInfo.objects.count()}")
    print(f"校区总数：{models.Campuses.objects.count()}")
    print(f"班级总数：{models.ClassList.objects.count()}")
    print(f"课程记录总数：{models.CourseRecord.objects.count()}")
    print(f"客户总数：{models.Customer.objects.count()}")
    print(f"咨询记录总数：{models.ConsultRecord.objects.count()}")
    print(f"学习记录总数：{models.StudyRecord.objects.count()}")
    
    # 按来源统计客户
    print("\n客户来源分布:")
    for source_code, source_name in models.SOURCE_CHOICES:
        count = models.Customer.objects.filter(source=source_code).count()
        if count > 0:
            print(f"  {source_name}: {count}")
    
    # 按状态统计客户
    print("\n客户状态分布:")
    for status_code, status_name in models.ENROLL_STATUS_CHOICES:
        count = models.Customer.objects.filter(status=status_code).count()
        if count > 0:
            print(f"  {status_name}: {count}")
    
    print("=" * 50)


def main():
    """主函数"""
    print("=" * 50)
    print("Django CRM 测试数据生成器")
    print("=" * 50)
    
    try:
        # 生成数据
        departments = generate_departments()
        users = generate_users(departments, 10)
        campuses = generate_campuses(3)
        classes = generate_classes(users, campuses, 8)
        course_records = generate_course_records(classes, users, 10)
        customers = generate_customers(users, 30)
        consult_records = generate_consult_records(customers, users, 2)
        study_records = generate_study_records(customers, course_records, 24)
        
        # 打印统计
        print_statistics()
        
        print("\n✓ 测试数据生成完成!")
        print("\n默认管理员账号:")
        print("  用户名：admin")
        print("  密码：admin123")
        print("\n普通用户账号示例:")
        print("  用户名：user001")
        print("  密码：pass123")
        
    except Exception as e:
        print(f"\n✗ 生成数据时出错：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
