# -*- coding:utf-8 -*-
# Author:cqk
# Data:2019/10/21 9:29
#外部文件使用django文件
import os
if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRM01.settings")
    import django
    django.setup()
    from app01 import models
    import random
    course_choices = (('LinuxL', 'Linux中高级'),
                      ('PythonFullStack', 'Python高级全栈开发'),)
    sex_type=(("male","男"),("female","女"))
    source_type = (('qq', "qq群"),
                   ('referral', "内部转介绍"),
                   ('website', "官方网站"),
                   ('baidu_ads', "百度推广"),
                   ('office_direct', "直接上门"),
                   ('WoM', "口碑"),
                   ('public_class', "公开课"),
                   ('website_luffy', "路飞官网"),
                   ('others', "其它"),)
    obj_list=[]
    for i in range(1000):
        obj_list.append(models.Customer(
          qq=F"{random.randint(1000000000,9999999999)}",
          name=f"liye{i}",
          sex=random.choice(sex_type)[0],
          source=random.choice(source_type)[0],
          course=random.choice(course_choices[0]),
        ))
    models.Customer.objects.bulk_create(obj_list)