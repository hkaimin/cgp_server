#!/usr/bin/env python'
# -*- coding: utf-8 -*-

from flask import jsonify, redirect, url_for, current_app as app
from flask.ext.admin import expose, BaseView

class StatisticPlayerView(BaseView):

    def is_visible(self):
        return False

    def user_db(self):
        zoning = app.extensions['zoning']
        return zoning.my_user_db()

    @expose('/')
    def index_view(self):
        return redirect(url_for('.level_view'))

    # 等级分布 #

    @expose('/level')
    def level_view(self):
        return self.render('statistics/statistic_player/level.html')

    @expose('/level.json')
    def level_json(self):
        db = self.user_db()
        statician = app.extensions['statician']
        entries = statician.stat_player_level(db)
        result = dict(entries=list(entries))
        return jsonify(result)
