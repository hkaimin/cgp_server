#!/usr/bin/env python'
# -*- coding: utf-8 -*-

from flask import request, jsonify, redirect, url_for, current_app as app
from flask.ext.admin import expose, BaseView


class StatisticLivingView(BaseView):

    def is_visible(self):
        return False

    def logging_db(self):
        zoning = app.extensions['zoning']
        return zoning.my_logging_db()

    @expose('/')
    def index_view(self):
        return redirect(url_for('.day_view'))

    # 按天统计 #

    @expose('/day')
    def day_view(self):
        return self.render('statistics/statistic_living/day.html')

    @expose('/day.json')
    def day_json(self):
        start = request.args.get('start')
        end = request.args.get('end')
        db = self.logging_db()
        statician = app.extensions['statician']
        entries = statician.stat_living_day(db, start, end)
        result = dict(entries=list(entries))
        return jsonify(result)

    # 留存率 #

    @expose('/retain')
    def retain_view(self):
        return self.render('statistics/statistic_living/retain.html')

    @expose('/retain.json')
    def retain_json(self):
        start = request.args.get('start')
        end = request.args.get('end')
        days = request.args.get('days', type=int);
        db = self.logging_db()
        statician = app.extensions['statician']
        entries = statician.stat_living_retain(db, start, end, days)
        result = dict(entries=list(entries))
        return jsonify(result)
