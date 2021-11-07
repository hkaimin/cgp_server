#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app
from datetime import datetime
from flask import request, redirect, flash, url_for, session
from flask.ext.admin import expose, BaseView

readable_time = lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')

class AccountView(BaseView):

    def is_visible(self):
        return False

    @expose('/')
    def index_view(self):
        return redirect(url_for('.permission_view'))

    @expose('/permission')
    def permission_view(self):
        guard = app.extensions['guard']
        groups = guard.my_group_names()
        permissions = guard.my_permission_details()
        return self.render('account/permission.html',
                           groups=groups, permissions=permissions)

    @expose('/password', methods=('GET', 'POST'))
    def password_view(self):
        if request.method == 'GET':
            return self.render('account/password.html')

        password = request.form['password']
        new_password = request.form['new_password']
        if (new_password == ''):
            flash('新密码不能为空', 'error')
            return redirect(url_for('.password_view'))

        guard = app.extensions['guard']
        user_id = session['user_id']
        user = guard.users.get(user_id)
        if user['password'] != password:
            flash('修改密码失败，当前密码不正确', 'error')
            return redirect(url_for('.password_view'))

        guard.change_user_password(user_id, new_password)
        flash('修改密码成功', 'success')

        return redirect(url_for('.password_view'))


views = [
    AccountView(name='我的账号', endpoint='account', url='/account'),
]
