#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pickle import dumps, loads, HIGHEST_PROTOCOL
from cPickle import dumps, loads
from hashlib import md5

from corelib import spawn, log
from redis import StrictRedis, RedisError


class StoreCache(object):
    PROTOCOL = HIGHEST_PROTOCOL
    ERROR_LOG = 50
    def __init__(self, url, redis=None, params=None):
        if not url:
            raise ValueError('no url:%s' % url)
        self.key = md5(url).hexdigest()
        self.url = url
        self.tbkeys = {}
        self.redis = redis
        self.error_count = 0
        if not self.redis:
            self.redis = StrictRedis(**params)
        if 0:
            self.redis = StrictRedis()


    def _get_name(self, tbname):
        try:
            return self.tbkeys[tbname]
        except KeyError:
            self.tbkeys[tbname] = key = '%s%s' % (self.key, tbname)
            log.info('[StoreCache]name: %s:%s = %s', self.url, tbname, key)
            return key

    def _handle_error(self):
        self.error_count += 1
        if self.error_count >= self.ERROR_LOG:
            self.error_count = 0
            log.log_except('[StoreCache]*******cache server error************')

    def get(self, tbname, key):
        """ """
        try:
            v = self.redis.hget(self._get_name(tbname), key)
            if not v:
                return None
            return loads(v)
        except RedisError:
            self._handle_error()

    def set(self, tbname, key, value):
        try:
            s = dumps(value, self.PROTOCOL)
            self.redis.hset(self._get_name(tbname), key, s)
        except RedisError:
            self._handle_error()

    def delete(self, tbname, key):
        """ delete """
        try:
            name = self._get_name(tbname)
            with self.redis.pipeline() as pipe:
                pipe.hexists(name, key)
                pipe.hdel(name, key)
                exists, _ = pipe.execute()
                return exists
        except RedisError:
            self._handle_error()

    def tb_clear(self, tbname):
        """ clear """
        self.redis.delete(self._get_name(tbname))



