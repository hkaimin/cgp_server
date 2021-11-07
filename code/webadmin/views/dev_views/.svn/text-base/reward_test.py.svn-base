#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, flash, current_app as app
from flask.ext.admin import expose, BaseView

defualt_args = dict(reward='''
[
    {"i":2,"c":999,"t":"i"}
]
'''.strip())


class RewardTestView(BaseView):
    html = 'dev/reward_test.html'

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

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):

        servers = self.get_servers()
        default = lambda: self.render(self.html,
                                      servers=servers, args=defualt_args)

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())

        try:
            server_name = args.pop('server', None)
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

        if args['params'].strip() == '':
            args['params'] = None

        if args['rewardid'].strip() == "":
            args['rewardid'] = None
        if args['pid'].strip() == "":
            args['pid'] = None

        try:
            result = self.gamesvr.reward_test(
                                    server['host'], server['port'], **args)
        except StandardError as error:
            flash('服务器错误：' + str(error), 'error')
            result = None

        return self.render(self.html,
                            servers=servers, args=request.form,
                            result=result)
