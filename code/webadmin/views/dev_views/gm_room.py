#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .gm_base_view import *
from flask import current_app as app, request, flash, session
from flask.ext.admin import expose, BaseView
from flask import (request, redirect, flash, abort, jsonify,
                   url_for, make_response, current_app as app)




class GMRoomView(GMBaseView):
    html = 'dev/gm_room.html'

    host = ""
    port = 0
    operation_function = None
    rpc_server = None

    def add_hero_base_property(self, pid, caty, value, *args):
        self.rpc_server.add_online_hero_property(pid, caty, value)
        return 1

    def update_hero_base_property(self, pid, caty, value, *args):
        self.rpc_server.update_online_hero_property(pid, caty, value)
        return 1

    def set_online_hero_pos(self, pid, type, value, *args):
        self.rpc_server.set_online_hero_pos(pid, value)
        return 1

    def set_online_hero_dice(self, pid, type, value, *args):
        self.rpc_server.set_online_hero_dice(pid, value)
        return 1

    def add_online_hero_card(self, pid, type, value, *args):
        self.rpc_server.add_online_hero_card(pid, value)
        return 1

    def set_end_time(self, pid, type, value, *args):
        self.rpc_server.set_end_time(pid, value)
        return 1

    @expose('/')
    def index_view(self):
        super(GMRoomView, self).index_view()
        self.operation_function = {'cash': self.add_hero_base_property,
                                   'ring': self.add_hero_base_property,
                                   'pos': self.set_online_hero_pos,
                                   'dice': self.set_online_hero_dice,
                                   'card': self.add_online_hero_card,
                                   'end': self.set_end_time}
        return self.render('dev/gm_room.html')

    @expose('/plist/', methods=('POST', ))
    def get_player_list(self):
        import webadmin.views.dev_views.dev as dev
        addr = dev.get_servers()[0]
        self.host = addr["host"]
        self.port = addr["port"]
        self.rpc_server = gamesvr().get_server(self.host, self.port)
        rpc_players = self.rpc_server.get_online_plist()
        return jsonify(rs=rpc_players)

    @expose('/roomplayer/', methods=('POST', 'GET'))
    def player_info_view(self):
        _pid = request.args["pid"]
        postvar = dict(request.form.items())
        key = ''
        if postvar:
            key = str(postvar['type'])
            self.rpc_server = gamesvr().get_server(self.host, self.port)
            if self.rpc_server:
                self.operation_function[key](_pid, postvar['type'], postvar['value'])

        return self.render('dev/room_player.html', pid=_pid, subtype=key)

    @expose('/roomplayerinfo/', methods=('POST', 'GET'))
    def player_info_table(self):
        _pid = request.args["pid"]
        self.rpc_server = gamesvr().get_server(self.host, self.port)
        rpc_player_in_room_info = None
        if self.rpc_server:
            rpc_player_in_room_info = self.rpc_server.get_online_room_player(_pid)
        return jsonify(rs=rpc_player_in_room_info)




