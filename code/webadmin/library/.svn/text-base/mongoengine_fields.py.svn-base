#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from mongoengine import IntField, FloatField, BooleanField, StringField, DynamicField, ObjectIdField
from mongoengine.base import BaseField

import bson

from utils import date2time, time2date


class IntListField(BaseField):

    def to_python(self, value):
        return ', '.join(map(str, value))

    def to_mongo(self, value):
        if value == '':
            return None
        return map(int, value.split(','))

    def validate(self, value):
        if value == '':
            return
        try:
            value = map(int, value.split(','))
        except:
            self.error('%s could not be converted to int' % value)


class PointField(IntListField):

    def validate(self, value):
        if value == '':
            return
        try:
            value = map(int, value.split(','))
        except:
            self.error('%s could not be converted to int' % value)

        if not len(value) == 2:
            self.error("Value (%s) must be a two-dimensional point" % repr(value))


class TimeField(BaseField):
    def to_python(self, value):
        return time2date(int(value))

    def to_mongo(self, value):
        if value == '':
            return 0
        return date2time(value)

    def validate(self, value):
        try:
            value = self.to_mongo(value)
        except:
            self.error('%s could not be converted to int' % value)


format_verbose_name = lambda x, y: '%s(%s)' % (y, x)

def makeIntField(db_field, label_name):
    verbose_name = format_verbose_name(db_field, label_name)
    return IntField(db_field=db_field, verbose_name=verbose_name)

def makeFloatField(db_field, label_name):
    verbose_name = format_verbose_name(db_field, label_name)
    return FloatField(db_field=db_field, verbose_name=verbose_name)

def makeBooleanField(db_field, label_name):
    verbose_name = format_verbose_name(db_field, label_name)
    return BooleanField(db_field=db_field, verbose_name=verbose_name)

def makeStringField(db_field, label_name):
    verbose_name = format_verbose_name(db_field, label_name)
    return StringField(db_field=db_field, verbose_name=verbose_name, max_length=1000000000)

def makeTextField(db_field, label_name):
    verbose_name = format_verbose_name(db_field, label_name)
    return StringField(db_field=db_field, verbose_name=verbose_name)

def makeDynamicField(db_field, label_name):
    verbose_name = format_verbose_name(db_field, label_name)
    help_text = u'需为 JSON 字符串'
    return DynamicField(db_field=db_field, verbose_name=verbose_name,
                        help_text=help_text)

def makeIntListField(db_field, label_name):
    verbose_name = format_verbose_name(db_field, label_name)
    help_text = u'逗号分隔的整数，例如：1, 2, 3'
    return IntListField(db_field=db_field, verbose_name=verbose_name,
                        help_text=help_text)

def makePointField(db_field, label_name):
    verbose_name = format_verbose_name(db_field, label_name)
    help_text = u'逗号分隔的二维坐标，例如：1, 2'
    return PointField(db_field=db_field, verbose_name=verbose_name,
                      help_text=help_text)

def makeTimeField(db_field, label_name):
    verbose_name = format_verbose_name(db_field, label_name)
    help_text = u'整数'
    return TimeField(db_field=db_field, verbose_name=verbose_name,
                     help_text=help_text)

def createIdField():
    return IntField(db_field='_id', verbose_name='ID(id)',
                    min_value=1, primary_key=True)

def createStringIdField():
    return StringField(db_field='_id', verbose_name='ID(id)', primary_key=True)

def createNameField():
    db_field = 'name'
    label_name = '名称'
    verbose_name = format_verbose_name(db_field, label_name)
    help_text = u'不超过 20 个字符'
    return StringField(db_field=db_field, verbose_name=verbose_name,
                       help_text=help_text, max_length=20)

def createKeyField():
    return IntField(db_field='key', verbose_name='KEY(key)',
                    min_value=1, primary_key=True)
