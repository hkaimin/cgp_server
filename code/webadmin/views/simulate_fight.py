#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, flash, current_app as app
from flask.ext.admin import expose, BaseView

class SimulateFightView(BaseView):

    def is_visible(self):
        return False

    def resource_db(self):
        zoning = app.extensions['zoning']
        return zoning.my_resource_db()

    def get_servers(self):
        db = self.resource_db()
        return list(db['server'].find())

    @property
    def gamesvr(self):
        return app.extensions['gamesvr']

    @expose('/', methods=('GET', ))
    def index_view(self):

        servers = self.get_servers()
        default = lambda: self.render('simulate_fight.html',
                                      servers=servers, args=request.args)

        if not request.args:
            return default()

        args = dict(request.args.items())

        try:
            server_name = args.pop('server', None)
            args = {key: int(value) for key, value in args.iteritems()}
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

        try:
            result = self.gamesvr.simulate_fight(
                                    server['host'], server['port'], args)
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render('simulate_fight.html',
                            servers=servers, args=request.args,
                            result=result)

