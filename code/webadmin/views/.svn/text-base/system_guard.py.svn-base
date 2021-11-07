#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import request, flash, redirect, url_for, current_app as app
from flask.ext.admin import expose, BaseView

class SystemGuardView(BaseView):

    def is_visible(self):
        return False

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        guard = app.extensions['guard']
        if request.method == 'POST':
            guard.reload()
            flash('账户信息已重载', 'success')
            return redirect(url_for('.index_view'))

        users = []
        for user_ in guard.users.itervalues():
            user = user_.copy()
            permission = guard.get_permissions_for_user(user['_id'])
            if permission is None:
                user['permissions'] = ''
            else:
                user['permissions'] = json.dumps(list(permission), indent=4)
            users.append(user)

        return self.render('system_guard.html', users=users)
