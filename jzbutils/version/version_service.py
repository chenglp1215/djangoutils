#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/4/12 下午6:11
# @Author  : chenglp
# @Email   : chenglongping@100tal.com


class Version(object):

    def get_app_version(self):
        app_sign = "patriarch/"
        ua = self.request.META.get("HTTP_USER_AGENT", "").lower()
        if app_sign not in ua:
            return
        start = ua.index(app_sign) + len(app_sign)
        sub = ua[start:]
        v = sub[:sub.index(" ")]
        return v

    def __init__(self, request):
        self.request = request
        self.v = self.get_app_version()

    def compare_version(self, version, op="=="):
        func = {
            "==": lambda a, b: a == b,
            ">=": lambda a, b: a >= b,
            "<=": lambda a, b: a <= b,
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b
        }
        v = self.v
        try:
            float(v)
        except:
            return func[op](v, version)
        else:
            version = version.split(".")
            version = version[0] + "." + "".join(version[1:])
            return func[op](v, version)

    def __lt__(self, version):
        return self.compare_version(version=version, op="<")

    def __le__(self, version):
        return self.compare_version(version=version, op="<=")

    def __ge__(self, other):
        return self.compare_version(version=other, op=">=")

    def __gt__(self, other):
        return self.compare_version(version=other, op=">")

    def __eq__(self, other):
        return self.compare_version(version=other, op="==")



