#!/usr/bin/env python'
# -*- coding: utf-8 -*-

from flask import request, jsonify, current_app as app
from flask.ext.admin import expose, BaseView

class StatisticGeneralView(BaseView):

    def is_visible(self):
        return False

    def logging_db(self):
        zoning = app.extensions['zoning']
        return zoning.my_logging_db()

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        return self.render('statistics/statistic_general.html')

    @expose('/data.json')
    def data_json(self):
        start_time = request.args.get('start', type=int)
        end_time = request.args.get('end', type=int)
        general_type = request.args.get('type', type=int)

        db = self.logging_db()
        criteria = {
            'ct': {'$gte': start_time, '$lte': end_time},
            't': general_type,
        }
        entries = db['log_general'].find(criteria).sort('ct', -1)
        result = dict(entries=list(entries))
        return jsonify(result)
