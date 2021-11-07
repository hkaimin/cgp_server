#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app
from flask.ext.admin import expose, BaseView

class SystemPermissionView(BaseView):

    def is_visible(self):
        return False

    @expose('/')
    def index_view(self):
        guard = app.extensions['guard']
        permissions = guard.get_all_permission_details()
        return self.render('system_permission.html', permissions=permissions)
