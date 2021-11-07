#!/usr/bin/env python'
# -*- coding: utf-8 -*-

from flask import request, jsonify, redirect, url_for, current_app as app
from flask.ext.admin import expose, BaseView
from webadmin.library.utils import *
from webadmin.define.constant import *
from webadmin.extension.zoning import *
import time



class StatisticRetention(BaseView):


    def user_db(self):
        zoning = app.extensions['zoning']
        return zoning.my_user_db()

    def logging_db(self, id):
        zoning = app.extensions['zoning']
        return zoning.get_logging_db(id)

    def admin_db(self):
        zoning = app.extensions['zoning']
        return zoning.get_admin_db()

    def get_statician(self):
        s = app.extensions['statician']
        if 0:
            from webadmin.extension.statician import Statician
            s = Statician()
        return s

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        gid = None
        args = {}
        rs = []
        servers = Zoning.share().get_curren_server_list()
        if 'server' in request.args:
            svrid = int(request.args['server'])
            gid = Zoning.share().get_zone_by_svid(svrid)
            args['serverid'] = svrid

        if 'start' in request.args:
            start = request.args['start']
            rs = self.response_rrt_search(start, gid, svrid)

        return self.render('statistics/statistic_retention/retention.html', p=rs, servers=servers, args=args)

    @expose('/r.json', methods=('GET', 'POST'))
    def index_view_json_rs(self):
        gid = None
        svrid = None

        rs = []
        if 'server' in request.args:
            svrid = int(request.args['server'])
            gid = Zoning.share().get_zone_by_svid(svrid)

        if 'start' in request.args:
            start = request.args['start']
            rs = self.response_rrt_search(start, gid, svrid)
        rrs = []
        day = ['次日', '3日', '7日']
        i =0
        for v in rs:
            v1 = {"type": day[i], "rate": v*100}
            rrs.append(v1)
            i += 1
        return jsonify(en=rrs)


    def response_rrt_search(self, start, gid, svrid):
        """ 处理查询存留率 """
        rrt_rs = []
        rrt_day = [RRT_NEXTDAY, RRT_3DAY, RRT_7DAY]
        for v in rrt_day:
            rrt = self.get_rrt(start, v, gid, svrid)
            if not rrt:
                startrs, rrt = self.create_retention(start, v, svrid)
                if rrt:
                    self.insertDB(startrs, rrt, v, gid, svrid)
            rrt_rs.append(rrt)
        return rrt_rs

    def create_retention(self, start, rtype, svrid):
        """ 创建留存率 """
        db = self.logging_db(svrid)
        s_timestmp = self.make_time_to_stamp(start)
        e_timestmp = s_timestmp + DAY_FOR_SEC * rtype
        ne_timestmp = e_timestmp + DAY_FOR_SEC * rtype

        now_timestmp = self.make_today_stamp()
        if now_timestmp < ne_timestmp:
            return 0, 0

        #注册量
        start_day_reg = self.get_statician().stat_reg_by_type(db, s_timestmp, e_timestmp, PL_LOG_REG_HERO)

        #登录量
        next_day_login = self.get_statician().stat_reg_by_type(db, e_timestmp, ne_timestmp, PL_LOG_LOGIN)
        s_pidlist = [v['p'] for v in start_day_reg]
        nd_pidlist = [v['p'] for v in next_day_login]

        start_day_reg_count = start_day_reg.count()

        inlist = list(set(s_pidlist).intersection(set(nd_pidlist)))
        next_day_login_count = len(inlist)
        rrt = float(next_day_login_count) / float(start_day_reg_count)
        return time2str(s_timestmp), rrt

    def insertDB(self, ct, rrt, rtype, gid, svrid):
        """ 插入数据库 """
        db = self.admin_db()
        from store.mongodb import auto_inc_
        row = {}
        row['_id'] = auto_inc_(db, 'log_retention')
        row['gid'] = gid
        row['svrid'] =svrid
        row['ct'] = ct
        row['rtype'] = rtype
        row['rrt'] = rrt
        db['log_retention'].insert(row)

    def get_rrt(self, ct, rtype, gid, svrid):
        """ 在结果表 获取留存率 """
        db = self.admin_db()
        ct = time2str(self.make_time_to_stamp(ct))

        rrt = self.get_statician().stat_rrt_by_day(db, ct, rtype, gid, svrid)
        if rrt.count() > 0:
            return rrt[0]['rrt']
        return None

    def make_time_to_stamp(self, start):
        """ 创建查询时间戳 """
        d1 = unixtime(start)
        s_t = datetime.datetime.fromtimestamp(d1)
        s_t = datetime.datetime(s_t.year, s_t.month, s_t.day)
        s_t = time.mktime(s_t.timetuple())
        return s_t

    def make_today_stamp(self):
        """ 获取今天0:0:0时间戳"""
        now_t = time.time()
        now_t = datetime.datetime.fromtimestamp(now_t)
        now_t = datetime.datetime(now_t.year, now_t.month, now_t.day)
        now_t = time.mktime(now_t.timetuple())
        return now_t
