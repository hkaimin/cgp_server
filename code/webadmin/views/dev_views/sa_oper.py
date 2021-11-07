#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, flash, current_app as app
from flask.ext.admin import expose, BaseView

class P1View(BaseView):

    def get_servers(self):
        db = self.resource_db()
        return list(db['server'].find())

    def resource_db(self):
        zoning = app.extensions['zoning']
        return zoning.my_resource_db()

    @property
    def gamesvr(self):
        return app.extensions['gamesvr']

class BlockView(P1View):

    html = 'dev/block.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()

        default = lambda : self.render(self.html, servers=servers, args={})

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
        args['pid'] = int(args['pid'])
        args['time'] = int(args['time'])

        try:
            result = self.gamesvr.block(server['host'], server['port'], args["pid"], args["time"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)

class UnBlockView(P1View):

    html = 'dev/unblock.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()

        default = lambda : self.render(self.html, servers=servers, args={})

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
        args['pid'] = int(args['pid'])

        try:
            result = self.gamesvr.unblock(server['host'], server['port'], args["pid"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)

class IsBlockView(P1View):

    html = 'dev/is_block.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()

        default = lambda : self.render(self.html, servers=servers, args={})

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
        args['pid'] = int(args['pid'])

        try:
            result = self.gamesvr.is_block(server['host'], server['port'], args["pid"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)

class KickPlayerView(P1View):

    html = 'dev/kick_player.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()

        default = lambda : self.render(self.html, servers=servers, args={})

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
        args['pid'] = int(args['pid'])

        try:
            result = self.gamesvr.kick_player(server['host'], server['port'], args["pid"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)

class SetNameView(P1View):

    html = 'dev/set_name.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()

        default = lambda : self.render(self.html, servers=servers, args={})

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
        args['pid'] = int(args['pid'])

        try:
            result = self.gamesvr.set_name(server['host'], server['port'], args["pid"], args["name"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)

class LimitSpeakView(P1View):

    html = 'dev/limit_speak.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()

        default = lambda : self.render(self.html, servers=servers, args={})

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
        args['pid'] = int(args['pid'])
        args['time'] = int(args['time'])

        try:
            result = self.gamesvr.limit_speak(server['host'], server['port'], args["pid"], args["time"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)

class UnLimitSpeakView(P1View):

    html = 'dev/unlimit_speak.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()

        default = lambda : self.render(self.html, servers=servers, args={})

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
        args['pid'] = int(args['pid'])

        try:
            result = self.gamesvr.unlimit_speak(server['host'], server['port'], args["pid"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)

class LimitSpeakSpeedView(P1View):

    html = 'dev/limit_speak_speed.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()

        default = lambda : self.render(self.html, servers=servers, args={})

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
        args['pid'] = int(args['pid'])
        args['last_time'] = int(args['last_time'])
        args['interval'] = int(args['interval'])

        try:
            result = self.gamesvr.limit_speak_speed(server['host'], server['port'], args["pid"], args["last_time"], args["interval"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)

class AddCoin1View(P1View):

    html = 'dev/coin1.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()

        default = lambda : self.render(self.html, servers=servers, args={})

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
        args['pid'] = int(args['pid'])
        args['coin1'] = int(args['amount'])

        try:
            result = self.gamesvr.add_coin1(server['host'], server['port'], args["pid"], args["coin1"], args["reason"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)

class CostCoin1View(P1View):

    html = 'dev/coin1.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()

        default = lambda : self.render(self.html, servers=servers, args={})

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
        args['pid'] = int(args['pid'])
        args['coin1'] = int(args['amount'])

        try:
            result = self.gamesvr.cost_coin1(server['host'], server['port'], args["pid"], args["coin1"], args["reason"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)

class AddCoin2View(P1View):

    html = 'dev/coin2.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()

        default = lambda : self.render(self.html, servers=servers, args={})

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
        args['pid'] = int(args['pid'])
        args['coin2'] = int(args['amount'])

        try:
            result = self.gamesvr.add_coin2(server['host'], server['port'], args["pid"], args["coin2"], args["reason"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)

class CostCoin2View(P1View):

    html = 'dev/coin2.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()

        default = lambda : self.render(self.html, servers=servers, args={})

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
        args['pid'] = int(args['pid'])
        args['coin2'] = int(args['amount'])

        try:
            result = self.gamesvr.cost_coin2(server['host'], server['port'], args["pid"], args["coin2"], args["reason"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)

class AddGameObjView(P1View):

    html = 'dev/game_objs.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()

        default = lambda : self.render(self.html, servers=servers, args={})

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
        args['pid'] = int(args['pid'])
        args['id'] = int(args['id'])
        args['amount'] = int(args['amount'])

        try:
            result = self.gamesvr.add_game_objs(server['host'], server['port'], args["pid"], args["type"], args["id"], args["amount"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)

class DelGameObjView(P1View):

    html = 'dev/game_objs.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()

        default = lambda : self.render(self.html, servers=servers, args={})

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
        args['pid'] = int(args['pid'])
        args['id'] = int(args['id'])
        args['amount'] = int(args['amount'])

        try:
            result = self.gamesvr.del_game_objs(server['host'], server['port'], args["pid"], args["type"], args["id"], args["amount"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)


class SendMailView(P1View):
    html = 'dev/send_mail.html'
    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()
        default = lambda : self.render(self.html, servers=servers, args={})
        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['pid'].strip() == "":
            args['pid'] = None
            return default()
        args['pid'] = int(args['pid'])
        try:
            result = 'send_mail done'
            self.gamesvr.send_mail(server['host'], server['port'], args["pid"], args['title'], args['content'])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)


class AnnouncementView(P1View):
    html = 'dev/announcement.html'
    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        servers = self.get_servers()
        default = lambda : self.render(self.html, servers=servers, args={})
        if request.method == 'GET':
            return default()

        args = dict(request.form.items())
        try:
            server_name = args["server"]
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

        rpc_server = None
        for server in servers:
            if server_name == server['name']:
                rpc_server = server
                break
        if rpc_server is None:
            flash('服务器不存在', 'error')
            return default()

        if args['msg'].strip() == "":
            args['msg'] = ""
        try:
            result = 'announcement done'
            self.gamesvr.announcement(server['host'], server['port'], args["msg"])
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html, servers=servers, args=request.form, result=result)


class NoticeBoardView(P1View):
    html = 'dev/notice_board.html'
    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        import os, json, os.path as path
        from release_version import ReleaseVersionView
        announce_s = 'announce'
        dest_path = ReleaseVersionView.res_path()
        announce_path = path.join(dest_path, announce_s)
        if not path.exists(announce_path):
            os.makedirs(announce_path)

        # dest_path = r'c:\see\rich9\tmp'
        source_path = path.join(dest_path, 'board.json')
        if path.exists(source_path):
            with open(source_path, 'rb') as f:
                d = f.read()
        else:
            d = ''

        args = dict(request.form.items())
        default = lambda params=None: self.render(self.html, args=params)
        if request.method == 'GET':
            args['msg'] = d
            return default(args)

        if args['msg'].strip() == "":
            args['msg'] = ""
            result = 'no value to update notice board'
        else:
            d = args['msg'].encode('utf8')
            with open(source_path, 'wb') as f:
                f.write(d)
            objs = json.loads(d)
            titles, contents = [], {}
            for obj in objs:
                contents[obj['ver']] = obj.pop('content')
                titles.append(obj)

            with open(path.join(dest_path, 'announce.list'), 'wb') as f:
                d = json.dumps(titles, ensure_ascii=False)
                f.write(d)
            for key, value in contents.iteritems():
                with open(path.join(dest_path, announce_s, '%s.announce' % key), 'wb') as f:
                    f.write(value)

            result = 'update notice board done'

        return self.render(self.html, args=request.form, result=result)

