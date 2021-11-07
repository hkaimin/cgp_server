#!/usr/bin/env python
# -*- coding: utf-8 -*-

from corelib import RLock

from flask import current_app as app
from mongoengine import Document


class BaseModel(Document):
    meta = {'abstract': True}

    @classmethod
    def cls_init(cls):
        cls._rlock = RLock()
        cls._old_get_collection = cls._get_collection
        cls._get_collection = cls._nocache_get_collection

    @classmethod
    def _nocache_get_collection(cls):
        """ 不缓存, 会递归调用 """
        with cls._rlock:
            if cls._collection:
                return cls._collection
            rs = cls._old_get_collection()
            cls._collection = None
            return rs

    @classmethod
    def clean_cache(cls):
        """ 清除缓存 """
        zone = app.extensions['zoning']
        zone.clean_model_cache(cls)

    @classmethod
    def get_zone_objects(cls):
        """ 支持多数据库 """
        zone = app.extensions['zoning']
        return zone.get_model_objects(cls)


#------------------------
#------------------------

