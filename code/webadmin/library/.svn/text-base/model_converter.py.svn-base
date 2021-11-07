#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms.fields import StringField, DateTimeField
from flask.ext.mongoengine.wtf import orm
from flask.ext.admin.contrib.mongoengine.form import CustomModelConverter

from .wtforms_fields import JSONField
from .wtforms_validators import IntList, Point, TimeValid

class ModelConverter(CustomModelConverter):

    @orm.converts('DynamicField')
    def conv_Dynamic(self, model, field, kwargs):
        return JSONField(**kwargs)

    @orm.converts('IntListField')
    def conv_IntList(self, model, field, kwargs):
        kwargs['validators'].append(IntList())
        return StringField(**kwargs)

    @orm.converts('PointField')
    def conv_Point(self, model, field, kwargs):
        kwargs['validators'].append(Point())
        return StringField(**kwargs)

    @orm.converts('TimeField')
    def conv_Time(self, model, field, kwargs):
        kwargs['validators'].append(TimeValid())
        return DateTimeField(**kwargs)
