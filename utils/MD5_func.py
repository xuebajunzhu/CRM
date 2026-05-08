# -*- coding:utf-8 -*-
# Author:cqk
# Data:2019/10/18 15:09
"""
Deprecated: This module uses insecure MD5 hashing.
Use Django's built-in password hashing instead:
    from django.contrib.auth.hashers import make_password, check_password
"""
import hashlib
import warnings

def md5_function(value):
    """
    DEPRECATED: Insecure MD5 hashing function.
    This function is kept for backward compatibility only.
    All new code should use Django's make_password() and check_password().
    """
    warnings.warn(
        "md5_function is deprecated and insecure. Use Django's make_password() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    secret_key="username".encode("utf-8")
    md5=hashlib.md5()
    md5.update(value.encode("utf-8"))
    return md5.hexdigest()
    
if __name__ == '__main__':
    s="123"
    print(md5_function(s))
