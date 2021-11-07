#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webadmin.library import mongoengine_fields as f
from .base import BaseModel as Document


class User(Document):
    """ 用户表 """

    meta = {'collection': 'user'}

    id = f.createIdField()
    name = f.makeStringField('name', '用户名')
    password = f.makeStringField('password', '密码')
    groups = f.makeIntListField('groups', '用户组')


class Group(Document):
    """ 用户组表 """

    meta = {'collection': 'group'}

    id = f.createIdField()
    name = f.makeStringField('name', '用户组名')
    note = f.makeStringField('note', '说明')
    permissions = f.makeDynamicField('permissions', '权限')

class Setting(Document):
    """ 设置表 """

    meta = {'collection': 'setting'}

    id = f.createIdField()
    value = f.makeDynamicField('value', '值')

class Gamesvr(Document):
    """ 服务器表 """

    meta = {'collection': 'gamesvr'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    desc = f.makeStringField('desc', '描述')
    host = f.makeStringField('host', '主机')
    port = f.makeIntField('port', '端口')
    resource_db = f.makeStringField('resource_db', '资源库地址')
    user_db = f.makeStringField('user_db', '用户库地址')
    logging_db = f.makeStringField('logging_db', '日志库地址')
    zone = f.makeIntField('zone', '服务器组')

class Zone(Document):
    """ 服务器组表 """

    meta = {'collection': 'zone'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    desc = f.makeStringField('desc', '描述')
    resource_db = f.makeStringField('resource_db', '资源库地址')
    user_db = f.makeStringField('user_db', '用户库地址')
    logging_db = f.makeStringField('logging_db', '日志库地址')

models = [User, Group, Setting,
          Gamesvr, Zone]
