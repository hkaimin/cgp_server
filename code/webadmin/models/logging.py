#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webadmin.library import mongoengine_fields as f
from .base import BaseModel as Document


class LogRpc(Document):
    """ RPC表 """

    meta = {'collection': 'log_rpc'}

    id = f.createStringIdField()
    func = f.makeStringField('func', '函数')
    total = f.makeIntField('total', '总调用次数')
    use = f.makeFloatField('use', '总耗时')
    t = f.makeIntField('t', '分类')
    err = f.makeIntField('err', '错误次数')
    ct = f.makeIntField('ct', '时间')

class LogOnline(Document):
    """ 在线表 """

    meta = {'collection': 'log_online'}

    id = f.createStringIdField()
    ct = f.makeIntField('ct', '时间')
    c = f.makeFloatField('c', '瞬间在线')
    pids = f.makeIntListField('pids', '同时在线')
    ACU = f.makeIntField('ACU', '同时在线数')

class LogInfo(Document):
    """ 上下线表 """

    meta = {'collection': 'log_info'}

    id = f.createStringIdField()
    ip = f.makeStringField('ip', 'IP')
    t = f.makeIntField('t', '分类')
    login = f.makeIntField('login', '登录时间')
    ct = f.makeIntField('ct', '时间')

class TraceBack(Document):
    """ TraceBack 表 """
    meta = {'collection': 'log_tb'}
    id = f.createStringIdField()
    tb = f.makeStringField('tb', 'traceback 信息')
    ct = f.makeTimeField('ct', '创建时间')
    appn = f.makeStringField('appn', '程序名字')

class LuaTraceBack(Document):
    """LuaTraceBack 表 """
    meta = {'collection': 'log_lua_tb'}
    id = f.createStringIdField()
    status = f.makeStringField('status', '状态')
    tb = f.makeStringField('tb', 'traceback 信息')
    counter = f.makeIntField('counter','累积出错次数')
    ct = f.makeStringField('ct', '最后出错时间')
    ver = f.makeStringField('ver', '最后出错客户端版本号')
    package_ver = f.makeStringField('package_ver', '安装包版本号')

class LuaTraceBackVar(Document):
    """LuaTraceBack 表 """
    meta = {'collection': 'log_lua_tb_var'}
    id = f.createStringIdField()
    tb = f.makeStringField('tb', 'traceback 信息')    
    ct = f.makeStringField('ct', '出错时间')
    ver = f.makeStringField('ver', '出错客户端版本号')
    package_ver = f.makeStringField('package_ver', '安装包版本号')
    info = f.makeStringField('info', '记录的变量信息')
    net_history = f.makeStringField('net_history', '网络通信数据')
    
models = [LogRpc, LogOnline, LogInfo, TraceBack, LuaTraceBack, LuaTraceBackVar]
