#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.admin import expose, BaseView
from webadmin.views.statistics_views.statistic_general import StatisticGeneralView
from webadmin.views.statistics_views.statistic_register import StatisticRegisterView
from webadmin.views.statistics_views.statistic_online import StatisticOnlineView
from webadmin.views.statistics_views.statistic_living import StatisticLivingView
from webadmin.views.statistics_views.statistic_player import StatisticPlayerView
from webadmin.views.statistics_views.statistic_ranking import StatisticRankingView
from webadmin.views.statistics_views.statistic_retention import StatisticRetention

class OpeIndexView(BaseView):

    @expose('/')
    def index(self):
        return self.render('ope.html')

views = [
    OpeIndexView(name=u'运营管理',
                 endpoint='ope',
                 url='/ope/'),

    StatisticGeneralView(name=u'综合报表',
                         endpoint='statistic_general',
                         url='/ope/statistic_general'),

    StatisticRegisterView(name=u'注册账户数统计',
                        endpoint='statistic_register',
                        url='/ope/statistic_register'),

    StatisticOnlineView(name=u'在线账户数统计',
                        endpoint='statistic_online',
                        url='/ope/statistic_online'),

    StatisticLivingView(name=u'在线时长统计',
                        endpoint='statistic_living',
                        url='/ope/statistic_living'),

    StatisticPlayerView(name=u'玩家属性分布统计',
                        endpoint='statistic_player',
                        url='/ope/statistic_player'),

    StatisticRankingView(name=u'玩家排行统计',
                        endpoint='statistic_ranking',
                        url='/ope/statistic_ranking'),

    StatisticRetention(name=u'留存率统计',
                       endpoint='statistic_retention',
                       url='/ope/statistic_retention')
]
