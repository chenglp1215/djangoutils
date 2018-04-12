#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/4/12 下午6:11
# @Author  : chenglp
# @Email   : chenglongping@100tal.com

import cPickle
from cacheops import cache


class CacheService(object):

    @classmethod
    def lpush(cls, key, lst, timeout):
        need_set_expire = not cache.conn.exists(key)
        cache.conn.lpush(key, *lst)
        if need_set_expire and timeout:
            cache.conn.expire(key, timeout)

    @classmethod
    def rpush(cls, key, lst, timeout=None):
        need_set_expire = not cache.conn.exists(key)
        cache.conn.rpush(key, *lst)
        if need_set_expire and timeout:
            cache.conn.expire(key, timeout)

    @classmethod
    def lrange(cls, key, start=0, end=-1):
        return cache.conn.lrange(key, start, end)

    @classmethod
    def get(cls, key):
        return cache.conn.get(key)

    @classmethod
    def set(cls, key, value, timeout=None):
        if timeout:
            cache.conn.set(key, value, timeout)
        else:
            cache.conn.set(key, value)

    @classmethod
    def get_obj(cls, key):
        value = cache.conn.get(key)
        if value:
            return cPickle.loads(value)
        return value

    @classmethod
    def set_obj(cls, key, value, timeout=None):
        if timeout:
            cache.conn.set(key, cPickle.dumps(value), timeout)
        else:
            cache.conn.set(key, cPickle.dumps(value))

    @classmethod
    def zadd(cls, key, **kwargs):
        need_set_expire = not cache.conn.exists(key)
        timeout = kwargs.pop("timeout", None)
        cache.conn.zadd(key, **kwargs)
        if need_set_expire and timeout:
            cache.conn.expire(key, timeout)

    @classmethod
    def zrange(cls, key, start=0, end=-1, desc=True):
        return cache.conn.zrange(key, start, end, desc=desc)

    @classmethod
    def zincrby(cls, key, field, num=1):
        return cache.conn.zincrby(key, field, num)

    @classmethod
    def sismember(cls, key, val):
        return cache.conn.sismember(key, val)

    @classmethod
    def sadd(cls, key, val):
        return cache.conn.sadd(key, val)

    @classmethod
    def smembers(cls, key):
        return cache.conn.smembers(key)

    @classmethod
    def srem(cls, key, *vals):
        return cache.conn.srem(key, *vals)

    @classmethod
    def incrby(cls, key, num=1):
        return cache.conn.incrby(key, num)

    @classmethod
    def decrby(cls, key, num=-1):
        return cache.conn.decr(key)

    @classmethod
    def exists(cls, key):
        return cache.conn.exists(key)

    @classmethod
    def ltrim(cls, key, start, end):
        return cache.conn.ltrim(key, start, end)

    @classmethod
    def expire(cls, key, time=-1):
        return cache.conn.expire(key, time)

    @classmethod
    def hget(cls, key, field):
        return cache.conn.hget(key, field)

    @classmethod
    def hmget(cls, key, fields):
        return cache.conn.hmget(key, fields)

    @classmethod
    def hgetall(cls, key):
        return cache.conn.hgetall(key)

    @classmethod
    def hset(cls, key, field, value):
        return cache.conn.hset(key, field, value)

    @classmethod
    def hmset(cls, key, timeout=None, **value):
        need_set_expire = not cache.conn.exists(key)
        cache.conn.hmset(key, value)
        if need_set_expire and timeout:
            cache.conn.expire(key, timeout)

    @classmethod
    def hdel(cls, key, field):
        return cache.conn.hdel(key, field)

    @classmethod
    def hkeys(cls, key):
        return cache.conn.hkeys(key)

    @classmethod
    def hincrby(cls, key, field, value=1):
        return cache.conn.hincrby(key, field, value)

    @classmethod
    def ttl(cls, key):
        return cache.conn.ttl(key)

    @classmethod
    def flush_time(cls, key, rest_limit, time):
        rest_timeout = cls.ttl(key)
        if rest_timeout in [-2, -1]:
            return rest_timeout
        else:
            if rest_timeout < rest_limit:
                return cls.expire(key=key, time=time)
            else:
                return rest_timeout

    @classmethod
    def pipe_hmget(cls, keys, fields):
        with cache.conn.pipeline() as pipe:
            for key in keys:
                pipe.hmget(key, fields)
            ret = pipe.execute()
        return ret

    @classmethod
    def pipe_hmset(cls, command_lines):
        with cache.conn.pipeline() as pipe:
            for cmd in command_lines:
                pipe.hmset(*cmd)
            ret = pipe.execute()
        return ret

    @classmethod
    def expireat(cls, name, dt_or_tm):
        return cache.conn.expireat(name, dt_or_tm)

    @classmethod
    def pipeline(cls, transaction=True, shard_hint=None):
        return cache.conn.pipeline(transaction, shard_hint)
