#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app
from flask.ext.admin import expose, BaseView

class SystemUserView(BaseView):

    def is_visible(self):
        return False

    @expose('/')
    def index_view(self):
        guard = app.extensions['guard']
        return self.render('system_user/list.html', users=guard.users, groups=guard.groups)

    @expose('/new', methods=('GET', 'POST'))
    def new_view(self):
        pass

    @expose('/edit/<int:id>', methods=('GET', 'POST'))
    def edit_view(self, id):
        pass
