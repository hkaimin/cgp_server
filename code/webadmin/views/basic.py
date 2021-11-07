#!/usr/bin/env python'
# -*- coding: utf-8 -*-

from flask import redirect, url_for
from flask.ext.admin import expose, BaseView, AdminIndexView

class IndexView(AdminIndexView):

    def is_visible(self):
        return False

    @expose('/')
    def index(self):
        return redirect(url_for('gamesvr.index_view'))

class ErrorView(BaseView):

    def is_visible(self):
        return False

    @expose('/')
    def index_view(self):
        return self.render('error.html')

index_view = IndexView()
error_view = ErrorView(name=u'错误', endpoint='error', url='/error')
