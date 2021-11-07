#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from wtforms.validators import ValidationError

from utils import date2time

class JSON(object):

    def __init__(self):
        self.message = u'无效的 JSON 格式字符串。'

    def __call__(self, form, field):
        try:
            json.loads(field.data)
        except:
            raise ValidationError(self.message)

class IntList(object):

    def __init__(self):
        self.message = u'无效的整数列表'

    def __call__(self, form, field):
        try:
            map(int, field.data.split(','))
        except:
            raise ValidationError(self.message)

class Point(object):

    def __init__(self):
        self.message = u'无效的坐标'

    def __call__(self, form, field):
        try:
            value = map(int, field.data.split(','))
        except:
            raise ValidationError(self.message)

        if len(value) != 2:
            raise ValidationError(self.message)

class TimeValid(object):
    def __init__(self):
        self.message = u'无效的整数'

    def __call__(self, form, field):
        try:
            date2time(field.data)
        except:
            raise ValidationError(self.message)



