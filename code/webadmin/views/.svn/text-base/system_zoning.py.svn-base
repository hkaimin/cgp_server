#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, flash, redirect, url_for, current_app as app
from flask.ext.admin import expose, BaseView

class SystemZoningView(BaseView):

    def is_visible(self):
        return False

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        zoning = app.extensions['zoning']
        if request.method == 'POST':
            zoning.reload()
            zoning.make_force_reselect()
            flash('服务器信息已从数据库重载', 'success')
            return redirect(url_for('.index_view'))

        return self.render('system_zoning.html')

    @expose('/rebuild', methods=('POST',))
    def rebuild(self):
        zoning = app.extensions['zoning']
        zoning.auto_create_gamesvrs_from_running_server()
        flash('服务器信息已每个服务器重载', 'success')
        return redirect(url_for('.index_view'))
