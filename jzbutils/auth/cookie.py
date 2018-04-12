#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/4/12 下午7:14
# @Author  : chenglp
# @Email   : chenglongping@100tal.com
import logging


class AuthCookie(object):

    def __init__(self, request, logger=logging.getLogger(__name__)):
        self.request = request
        self.logger = logger

    def get_auth_cookie(self):
        """
        返回 "FDX_auth=xxxxxxxxx;"格式的字符串
        """
        auth_cookie = "%s=%s;" % ("FDX_auth", self.get_auth_key())
        return auth_cookie

    def get_auth_key(self):
        request = self.request
        auth_cookie = ''

        if request.GET.get("api_key"):
            return request.GET.get("api_key")

        if request.META.get('HTTP_AUTHORIZATION'):
            return request.META.get('HTTP_AUTHORIZATION').split()[-1]

        for k, v in request.COOKIES.iteritems():
            if k in ['FDX_auth', 'FDA_auth', 'api_key']:
                return v

        return auth_cookie

    def get_auth_header(self):
        return {'Cookie': self.get_auth_cookie()}