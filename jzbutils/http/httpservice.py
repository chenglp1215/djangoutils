#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/4/11 上午11:03
# @Author  : chenglp
# @Email   : chenglongping@100tal.com
# -*- coding: utf-8 -*-

import hashlib
import importlib
import cPickle
import logging
from django.conf import settings
from requests.exceptions import RequestException

from jzbutils.http.httphelper import http

logger = logging.getLogger(__name__)


class Error(Exception):
    def __init__(self, err_msg, err_code=-1, **kwargs):
        self.err_msg = str(err_msg)
        self.err_code = err_code
        super(Error, self).__init__(err_msg, **kwargs)


class HttpService(object):
    url = None
    cache_seconds = 600
    error_count_prefix = '_ecp'
    error_count_cache_seconds = 60
    error_count_max_time = 3
    request_timeout = 2
    request_time = 0
    status_code = 0
    errmsg = ""

    def __init__(self, **kwargs):
        for each in ['cache_seconds', 'error_count_cache_seconds', 'error_count_max_time', 'request_timeout', 'request_time']:
            if each in kwargs and isinstance(kwargs.get(each), int):
                setattr(self, each, kwargs.get(each))
        self.requests = http

        if hasattr(settings, "JZBHTTP_CACHE"):
            self.cache_backend = importlib.import_module(settings.JZBHTTP_CACHE).cache
        else:
            raise ImportError("Could not find jzbhttp backend: JZBHTTP_CACHE")

    def hash_url(self, url):
        return hashlib.md5(url).hexdigest()

    def get(self, url, key=None, hash_method=None, **kwargs):
        hash_method = hash_method or self.hash_url
        error_key = hash_method(url)

        if not kwargs.get('timeout'):
            kwargs['timeout'] = self.request_timeout

        # 跨网请求单位时间超过指定值直接从缓存返回数据
        error_number = self.get_error_count(error_key)
        if error_number >= self.error_count_max_time:
            return key and self.get_cache(key) or None

        # 优先从缓存中返回有效结果
        if key and self.cache_seconds > 0:
            data = self.get_cache(key)
            if data:
                return data

        # 请求目标接口
        data = None
        try:
            data = self.requests.get(url, **kwargs)

            if data.status_code == 200 and key and self.cache_seconds > 0:
                self.set_cache(key, data)

            self.request_time = data.elapsed.total_seconds() * 1000  # ms
            self.status_code = data.status_code
        except RequestException as e:
            self.set_error_count(error_key)
            logger.error(e.message, exc_info=True)
            self.errmsg = str(e.message)

        return data

    def get_cache(self, key):
        try:
            ret = self.cache_backend.get(key)
            if ret:
                return cPickle.loads(ret)
        except Exception:
            return None

    def set_cache(self, key, value, timeout=None):
        timeout = timeout or self.cache_seconds

        self.cache_backend.set(key, cPickle.dumps(value), timeout)

    def set_error_count(self, key):
        error_count = self.get_error_count(key) + 1
        if error_count == 3:
            logger.error('Request %s' % self.url, exc_info=True)

        self.cache_backend.set(key + self.error_count_prefix, error_count,
                  self.error_count_cache_seconds)

    def get_error_count(self, key):
        try:
            return self.cache_backend.get(key + self.error_count_prefix)
        except Exception:
            return 0
