#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webadmin import statsets

class Statician(object):
    ''' 统计员 '''

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.extensions['statician'] = self
        self.init()

    def init(self):
        pass

    def stat_rpc(self, db, start, end, type):
        return statsets.rpc.rpc(db, start, end, type)

    def stat_register_minute(self, db, start, end, minutes):
        return statsets.register.minute(db, start, end, minutes)

    def stat_register_month(self, db, start, end):
        return statsets.register.month(db, start, end)

    def stat_online_detail(self, db, start, end):
        return statsets.online.detail(db, start, end)

    def stat_online_minute(self, db, start, end, minutes):
        return statsets.online.minute(db, start, end, minutes)

    def stat_online_month(self, db, start, end):
        return statsets.online.month(db, start, end)

    def stat_living_day(self, db, start, end):
        return statsets.living.day(db, start, end)

    def stat_living_retain(self, db, start, end, days):
        return statsets.living.retain(db, start, end, days)

    def stat_player_level(self, db):
        return statsets.player.level(db)

    def stat_ranking_level(self, db, limit):
        return statsets.ranking.level(db, limit)

    def stat_reg_by_type(self, db, start, end, logtype):
        return statsets.player.reg(db, start, end, logtype)

    def stat_rrt_by_day(self, db, start, logtype, gid, svrid):
        return statsets.player.rrt(db, start, logtype, gid, svrid)

