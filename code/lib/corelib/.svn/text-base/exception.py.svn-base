#!/usr/bin/env python
# -*- coding:utf-8 -*-

def exception_fix():
    """ 修正异常的继承 """
    try:
        import bson
        bson.errors.BSONError.__bases__ = (StandardError, )
        from pymongo import errors as mongo_errors
        mongo_errors.PyMongoError.__bases__ = (StandardError, )
    except ImportError:
        pass

class GameError(StandardError): pass