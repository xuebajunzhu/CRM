# -*- coding:utf-8 -*-
# Author:cqk
# Data:2019/10/18 15:09
import hashlib

def md5_function(value):
    secret_key="username".encode("utf-8")
    md5=hashlib.md5()
    md5.update(value.encode("utf-8"))
    return md5.hexdigest()

if __name__ == '__main__':
    s="123"
    print(md5_function(s))