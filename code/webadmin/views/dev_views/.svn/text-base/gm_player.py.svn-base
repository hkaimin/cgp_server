#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gm_base_view import *
from flask import current_app as app, request, flash, session
from flask.ext.admin import expose, BaseView
from flask import (request, redirect, flash, abort, jsonify,
                   url_for, make_response, current_app as app)
from webadmin.define.constant import *


class GMPlayerView(GMBaseView):
    html = 'dev/gm_player.html'

    def get_player_db(self, cond):
        db = self.user_db()
        listcond = []
        dictcond = {}
        dictcond['name']=str(cond)
        listcond.append(dictcond)
        dictcond = {}
        if cond.isdigit():
            dictcond['_id'] = int(cond)
            listcond.append(dictcond)

        cond = MDBOpe().oror(listcond)
        rs = db['player'].find(cond)
        return rs

    @expose('/', methods=('POST', 'GET'))
    def index_view(self):
        super(GMPlayerView, self).index_view()
        players = []
        postvar = dict(request.form.items())
        if postvar:
            searchcond = postvar['value']
            if searchcond:
                players = self.get_player_db(searchcond)

        return self.render(self.html, list=players)


    @expose('/nocache/', methods=('POST', 'GET'))
    def on_cache(self):
        postvar = dict(request.form.items())

        if postvar:
            playerid = postvar['id']
            self.rpc_server = gamesvr().get_server(session['host'], int(session['port']))
            if self.rpc_server:
                su = self.rpc_server.cls_player_cache(int(playerid))
                return jsonify(success=su)
        return jsonify(success=False)
