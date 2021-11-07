#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from os.path import join, exists
import time
import logging
from logging import (ERROR, config)

from corelib import log
from game import Game

import config
import engine
import json

class GameLogger(object):
    def __init__(self):
        import app
        self.appname = app.name

    def log2File(self, sLogName, sText, flag=0):
        # 转换成localtime
        time_local = time.localtime(time.time())
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        engine.C_Log2File("%s/%s/%s/%s.log"%(config.serverNo, self.appname, sLogName, sLogName),
                          "%s|%s|%s|%s"%(dt, config.serverNo, self.appname, sText),
                          flag)

    def log2FileByDict(self, sLogName, data, flag=0):
        # 转换成localtime
        time_local = time.localtime(time.time())
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        TimeKey = time.strftime("%Y-%m-%d", time_local)
        data["name"] = sLogName
        data["appname"] = self.appname
        data["serverNo"] = config.serverNo
        data["dt"] = dt
        data["TimeKey"] = TimeKey
        json_str = json.dumps(data)
        engine.C_Log2File("%s/%s/%s/%s.log"%(config.serverNo, self.appname, sLogName, sLogName),
                          "%s|%s"%(dt, json_str),
                          flag)

    def log2FileByDict2(self, sLogName, rid,  data, flag=0):
        # 转换成localtime
        time_local = time.localtime(time.time())
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        TimeKey = time.strftime("%Y-%m-%d", time_local)
        data["name"] = sLogName
        data["appname"] = self.appname
        data["serverNo"] = config.serverNo
        data["dt"] = dt
        data["TimeKey"] = TimeKey
        json_str = json.dumps(data)
        engine.C_Log2File("%s/%s/%s/%s.log"%(config.serverNo, self.appname, sLogName, sLogName),
                          "%s|%s|%s"%(dt, rid ,json_str),
                          flag)

    # 日志记录异常
    def LogPyException(self, sExtra=""):
        etype, value, tb = sys.exc_info()
        sText = format_exc()
        print sText
        self.log2File("pythonExcepthon", sText)



#
# # 抛出异常
# # sText	异常提示信息
# def RaiseException(sText):
#     etype, value, tb = sys.exc_info()
#     if etype != Exception:
#         raise Exception, "%s;%s:%s" % (sText, etype.__name__, value.message), tb
#     else:
#         raise Exception, "%s;%s" % (sText, value.message), tb

class LogErrorHandler(logging.Handler):
    appname = ''

    def __init__(self):
        logging.Handler.__init__(self)
        import app
        self.appname = app.name
        self.formatter = logging.Formatter(log.shortformat, log.shortdatefmt)

    def emit(self, record):
        sText =  self.format(record)
        Game.glog.log2File("LogErrorHandler", sText)

def createLogErrorHandler():
    r = LogErrorHandler()
    r.setLevel(ERROR)
    logging.root.addHandler(r)

from traceback import *
import sys
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
