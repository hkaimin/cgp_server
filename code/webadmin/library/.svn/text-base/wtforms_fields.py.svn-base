#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask.ext.mongoengine.wtf import fields

class JSONField(fields.JSONField):
    ''' unicode_escape 过的 JSONField

    即把 \uXXXX 形式转换回汉字
    '''

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        if self.data:
            return unicode(json.dumps(self.data)).decode('unicode_escape')
        else:
            return u''
