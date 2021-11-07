#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app, request, flash, session
from flask.ext.admin import expose, BaseView
from flask import (request, redirect, flash, abort, jsonify,
                   url_for, make_response, current_app as app)

def gamesvr():
    rsapp = app.extensions['gamesvr']
    if 0:
        from webadmin.extension.gamesvr import Gamesvr
        rsapp = Gamesvr()
    return rsapp


class GMBaseView(BaseView):
    host = ""
    port = 0
    rpc_server = None
    def user_db(self):
        zoning = app.extensions['zoning']
        return zoning.my_user_db()

    def logging_db(self, id):
        zoning = app.extensions['zoning']
        return zoning.get_logging_db(id)


    def admin_db(self):
        zoning = app.extensions['zoning']
        return zoning.get_admin_db()

    @expose('/')
    def index_view(self):
        if not 'host' in session:
            return redirect('dev/ctrl_svr/')
        self.host = session['host']
        self.port = session['port']
        self.rpc_server = gamesvr().get_server(self.host, self.port)
        if not self.rpc_server:
            return redirect('dev/ctrl_svr/')
