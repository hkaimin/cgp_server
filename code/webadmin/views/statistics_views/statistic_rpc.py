#!/usr/bin/env python'
# -*- coding: utf-8 -*-

from flask import request, jsonify, current_app as app
from flask.ext.admin import expose, BaseView


class StatisticRpcView(BaseView):
    html = 'dev/statistic_rpc.html'

    def is_visible(self):
        return False

    def logging_db(self):
        zoning = app.extensions['zoning']
        return zoning.my_logging_db()

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        return self.render(self.html)

    @expose('/data.json')
    def data_json(self):
        start = request.args.get('start')
        end = request.args.get('end')
        type = request.args.get('type', type=int)
        db = self.logging_db()
        statician = app.extensions['statician']
        entries = statician.stat_rpc(db, start, end, type)
        result = dict(entries=list(entries))
        return jsonify(result)
