#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/4/11 上午11:03
# @Author  : chenglp
# @Email   : chenglongping@100tal.com
# -*- coding: utf-8 -*-

from urlparse import urlparse

from django.conf import settings
import requests


DEFAULT_TIMEOUT = 2  # 3 秒


class HttpError(Exception):
    pass


class HttpHelperMeta(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance


class HttpHelper(HttpHelperMeta):
    _requests = {}
    _pool_connections = 128
    _pool_maxsize = 128
    _max_retries = 1

    def get_instance(self, url):
        parse = urlparse(url)
        if not parse.scheme or not parse.netloc:
            raise HttpError("url invalid")
        domain = "%s://%s" % (parse.scheme, parse.netloc)
        if domain not in self._requests:
            http_obj = requests.Session()
            http_obj.mount(
                parse.scheme,
                requests.adapters.HTTPAdapter(
                    pool_connections=self._pool_connections,
                    pool_maxsize=self._pool_maxsize,
                    max_retries=self._max_retries
                )
            )
            self._requests[domain] = http_obj
        else:
            http_obj = self._requests[domain]
        return http_obj

    def post(self, url, *args, **kwargs):
        http_obj = self.get_instance(url)
        if "timeout" not in kwargs:
            kwargs["timeout"] = DEFAULT_TIMEOUT

        if settings.DEBUG:
            print url, args, kwargs
        return http_obj.post(url, *args, **kwargs)

    def get(self, url, *args, **kwargs):
        http_obj = self.get_instance(url)
        if "timeout" not in kwargs:
            kwargs["timeout"] = DEFAULT_TIMEOUT

        if settings.DEBUG:
            print url, args, kwargs
        return http_obj.get(url, *args, **kwargs)


http = HttpHelper()
