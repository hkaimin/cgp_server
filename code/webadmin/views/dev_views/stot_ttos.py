#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask.ext.admin import expose, BaseView
from corelib.langconv import *
from flask import (request ,current_app as app)

class Stot_ttosView(BaseView):
    html = 'dev/stot_ttos.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        if 'to' in request.args:
            mod = request.args['to']
            zoning = app.extensions['zoning']
            res_db = zoning.my_resource_db()
            tra_tables = res_db.collection_names(include_system_collections=False)
            exclude = [ '_auto_inc_',
                        'gconfig',
                        'server',
                        'pay_log',
                        'pay_pre',]
            for ex in exclude:
                if ex in tra_tables:
                    tra_tables.remove(ex)
            #
            # tra_table = res_db["translation"].find()
            print '11111', tra_tables

            if int(mod) == 1:
                conv_func = Converter('zh-hant').convert
            if int(mod) == 2:
                conv_func = Converter('zh-hans').convert
            # for v in tra_tables:
            #     tablename = v['tname']
            #     tablefields = v['tfields']
            for tablename in tra_tables:
                tra_table = res_db[tablename]

                for v in tra_table.find():
                    updatedata = {}
                    for _key, _value in v.iteritems():
                        if _key == '_id':
                            continue
                        updatedata[_key] = self.trato(conv_func, _value)
                    tra_table.update({"_id": v["_id"]}, {"$set": updatedata})
        return self.render(self.html)

    def trato(self, convert_func, content):
        if isinstance(content, str):
            return convert_func(content.decode('utf-8')).encode('utf-8')
        elif isinstance(content, unicode):
            return convert_func(content)
        elif isinstance(content, (tuple, list, dict)):
            u = json.dumps(content, ensure_ascii=False)
            d = convert_func(u)
            return json.loads(d)
        return content

