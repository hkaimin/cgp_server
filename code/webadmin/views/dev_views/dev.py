#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app, request, flash, session

from flask.ext.admin import expose, BaseView
from release_version import ReleaseVersionView
from ..cache_control import CacheControlView
from ..simulate_fight import SimulateFightView
from .reward_test import RewardTestView
from ..ai_test import AITestView
from ..clone_database import CloneDatabaseView
from webadmin.views.statistics_views.statistic_rpc import StatisticRpcView
from .gm_room import GMRoomView
from .gm_player import GMPlayerView
from .stot_ttos import Stot_ttosView
from .upload_lng import UploadLngView
from .addExchangeCode import AddExchangeCodeView
from .sa_oper import *

def resource_db():
    zoning = app.extensions['zoning']
    return zoning.my_resource_db()


def get_servers():
    db = resource_db()
    return list(db['server'].find())


def get_rpc_server(servers, name):
    rpc_server = None
    for server in servers:
        if name == server['name']:
            rpc_server = server
            break
    return rpc_server


def gamesvr():
    return app.extensions['gamesvr']


class CtrlSvrView(BaseView):
    """ 服控制类 """
    html = 'dev/ctrl_svr.html'
    defualt_args = dict(robot="", robot_time=0,)
    arg_types = dict(robot=int, robot_time=int)

    def get_rpc_server(self, servers, args, server_name=None):
        if server_name is None:
            try:
                server_name = args.pop('server', None)
            except ValueError as error:
                flash('无效的表单参数：' + str(error), 'error')
                return

        rpc_server = get_rpc_server(servers, server_name)
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return
        return rpc_server

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = get_servers()
        form_args = dict(request.form.items())
        args = form_args.copy()
        def _call(rpc_server):
            """ 远程调用设置 """
            try:
                result = gamesvr().ctrl_svr(
                    rpc_server['host'], rpc_server['port'],
                    **args)
                session['host'] = rpc_server['host']
                session['port'] = rpc_server['port']
                for k, v in result.iteritems():
                    form_args[k] = v
                return result
            except StandardError as error:
                flash('服务器错误：' + str(error), 'error')

        default = lambda args=None: self.render(self.html,
                          servers=servers, args=self.defualt_args if args is None else args)

        #请求页面
        if request.method == 'GET':
            default_args = self.defualt_args

            if 'refresh' in request.args:
                name = request.args['refresh']
                rpc_server = self.get_rpc_server(servers, args, server_name=name)
                if rpc_server:
                    result = _call(rpc_server)
                    form_args['server'] = name
                    return self.render(self.html,
                                       servers=servers, args=form_args,
                                       result=result)
            return default(default_args)

        #设置
        rpc_server = self.get_rpc_server(servers, args)

        if not rpc_server:
            return default()

        for arg in self.defualt_args.iterkeys():
            t = self.arg_types[arg]
            if args[arg].strip() == '':
                args[arg] = None
            else:
                args[arg] = t(args[arg])

        result = _call(rpc_server)
        return self.render(self.html,
                           servers=servers, args=form_args,
                           result=result)


class MailTestView(BaseView):
    """ 邮件测试 """
    html = 'dev/mail_test.html'
    defualt_args = dict(mtype=1, stype=0, save=0)

    def is_visible(self):
        return False

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = get_servers()
        default = lambda: self.render(self.html,
                                      servers=servers, args=self.defualt_args)

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())

        try:
            server_name = args.pop('server', None)
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = get_rpc_server(servers, server_name)
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        for arg in ['content', 'title', 'pid', 'mtype', 'mitems', 'save', 'stype', 'rid']:
            if args[arg].strip() == '':
                args[arg] = None

        try:
            result = gamesvr().mail_test(
                                    rpc_server['host'], rpc_server['port'],
                                    **args)
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html,
                            servers=servers, args=request.form,
                            result=result)


class DevIndexView(BaseView):
    @expose('/')
    def index(self):
        return self.render('dev/dev.html')


class RunCodeView(BaseView):
    """ 执行代码 """
    html = 'dev/run_code.html'
    defualt_args = dict()

    def is_visible(self):
        return False

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = get_servers()
        default = lambda: self.render(self.html,
                                      servers=servers, args=self.defualt_args)

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())

        try:
            server_name = args.get('server', None)
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = get_rpc_server(servers, server_name)
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        for arg in ['content', 'pid',]:
            if args[arg].strip() == '':
                args[arg] = None

        try:
            result = gamesvr().run_code(rpc_server['host'], rpc_server['port'], request.form["pid"],request.form["content"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html,
                            servers=servers,
                            args=args,
                            result=result)

views = [
    DevIndexView(name=u'开发调试',
                 endpoint='dev',
                 url='/dev/'),
    ReleaseVersionView(name=u'发布版本',
                       endpoint='release_version',
                       url='/dev/release_version'),
    CacheControlView(name=u'数据缓存',
                     endpoint='cache_control',
                     url='/dev/cache_control'),
    SimulateFightView(name=u'战斗模拟',
                      endpoint='simulate_fight',
                      url='/dev/simulate_fight'),
    CtrlSvrView(name=u'服控制',
                 endpoint='ctrl_svr',
                 url='/dev/ctrl_svr'),

    RewardTestView(name=u'奖励测试',
                   endpoint='reward_test',
                   url='/dev/reward_test'),
    MailTestView(name=u'邮件测试',
                   endpoint='mail_test',
                   url='/dev/mail_test'),
    RunCodeView(name=u'执行代码',
                   endpoint='run_code',
                   url='/dev/run_code'),
    AITestView(name=u'AI测试',
                   endpoint='ai_test',
                   url='/dev/ai_test'),

    CloneDatabaseView(name=u'复制数据库',
                      endpoint='clone_database',
                      url='/dev/clone_database'),
    StatisticRpcView(name=u'RPC 统计',
                     endpoint='statistic_rpc',
                     url='/dev/statistic_rpc'),
    GMRoomView(name=u'房间GM',
               endpoint='gm_room',
               url='/dev/gm_room'),
    GMPlayerView(name=u'玩家GM',
                 endpoint='gm_player',
                 url='/dev/gm_player'),
    Stot_ttosView(name=u'数据库简繁互转',
                  endpoint='stot_ttos',
                  url='/dev/stot_ttos'),
    UploadLngView(name=u'上传资源包',
                  endpoint='upload_lng',
                  url='/dev/upload_lng'),

    BlockView(name=u'禁止玩家登陆',
                   endpoint='block',
                   url='/dev/block'),
    UnBlockView(name=u'取消禁止玩家登陆',
                   endpoint='unblock',
                   url='/dev/unblock'),
    IsBlockView(name=u'查询玩家是否被禁止登陆',
                   endpoint='is_block',
                   url='/dev/is_block'),

    KickPlayerView(name=u'踢下线',
                   endpoint='kick',
                   url='/dev/kick'),
    SetNameView(name=u'设置名字',
                   endpoint='name',
                   url='/dev/name'),
    LimitSpeakSpeedView(name=u'设置发言频率',
                   endpoint='speakspeed',
                   url='/dev/speakspeed'),
    LimitSpeakView(name=u'禁言',
                   endpoint='limitspeak',
                   url='/dev/limitspeak'),
    UnLimitSpeakView(name=u'取消禁言',
                   endpoint='unlimitspeak',
                   url='/dev/unlimitspeak'),

    AddCoin1View(name=u'奖励金币',
                   endpoint='add_coin1',
                   url='/dev/add_coin1'),
    CostCoin1View(name=u'扣除金币',
                   endpoint='cost_coin1',
                   url='/dev/cost_coin1'),
    AddCoin2View(name=u'奖励幸运星',
                   endpoint='add_coin2',
                   url='/dev/add_coin2'),
    CostCoin2View(name=u'扣除幸运星',
                   endpoint='cost_coin2',
                   url='/dev/cost_coin2'),

    AddGameObjView(name=u'奖励物品',
                   endpoint='add_objs',
                   url='/dev/add_objs'),
    DelGameObjView(name=u'扣除物品',
                   endpoint='del_objs',
                   url='/dev/del_obs'),
    SendMailView(name=u'发送邮件',
                     endpoint='send_mail',
                     url='/dev/send_mail'),
    AnnouncementView(name=u'系统公告',
                   endpoint='announcement',
                   url='/dev/announcement'),
    NoticeBoardView(name=u'公告栏',
                     endpoint='notice_board',
                     url='/dev/notice_board'),
    AddExchangeCodeView(name=u'兑换码',
                     endpoint='addExchangeCode',
                     url='/dev/addExchangeCode'),

]



