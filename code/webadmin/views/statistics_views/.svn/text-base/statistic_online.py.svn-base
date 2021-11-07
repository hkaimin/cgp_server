#!/usr/bin/env python'
# -*- coding: utf-8 -*-

from flask import request, jsonify, redirect, url_for, current_app as app
from flask.ext.admin import expose, BaseView


class StatisticOnlineView(BaseView):

    def is_visible(self):
        return False

    def logging_db(self):
        zoning = app.extensions['zoning']
        return zoning.my_logging_db()

    @expose('/')
    def index_view(self):
        return redirect(url_for('.detail_view'))

    # 原始数据 #

    @expose('/detail')
    def detail_view(self):
        return self.render('statistics/statistic_online/detail.html')

    @expose('/detail.json')
    def detail_json(self):
        start = request.args.get('start')
        end = request.args.get('end')
        db = self.logging_db()
        statician = app.extensions['statician']
        entries = statician.stat_online_detail(db, start, end)
        result = dict(entries=list(entries))
        return jsonify(result)

    # 按分统计 #

    @expose('/minute')
    def minute_view(self):
        return self.render('statistics/statistic_online/minute.html')

    @expose('/minute.json')
    def minute_json(self):
        start = request.args.get('start')
        end = request.args.get('end')
        minutes = request.args.get('minutes', type=int);
        db = self.logging_db()
        statician = app.extensions['statician']
        entries = statician.stat_online_minute(db, start, end, minutes)
        result = dict(entries=list(entries))
        return jsonify(result)

    # 按月统计 #

    @expose('/month')
    def month_view(self):
        return self.render('statistics/statistic_online/month.html')

    @expose('/month.json')
    def month_json(self):
        start = request.args.get('start')
        end = request.args.get('end')
        db = self.logging_db()
        statician = app.extensions['statician']
        entries = statician.stat_online_month(db, start, end)
        result = dict(entries=list(entries))
        return jsonify(result)
