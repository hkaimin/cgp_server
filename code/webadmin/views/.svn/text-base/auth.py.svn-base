#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from flask import current_app as app
from flask import render_template, url_for
from flask import flash, request, redirect, session
from flask.views import MethodView

class Index(MethodView):
    ''' 首页 '''

    name = 'index'
    path = '/'

    def get(self):
        return redirect(url_for('admin.index'))

class Login(MethodView):
    ''' 登录 '''

    name = 'login'
    path = '/login'

    def get(self):
        return render_template('login.html')

    def post(self):
        form = request.form

        # 开发过程中很多人都用弱密码，而后台又可以在外部访问的
        # 如果使用弱密码，禁止从外部登录
        if app.config.get('PROTECT_REMOTE_LOGIN'):
            if self.is_remote_login() and self.is_weak_password(form['password']):
                flash(u'本用户禁止从外部登录', 'error')
                return redirect(url_for(self.name))

        user = self.auth_user(form['username'], form['password'])
        if not user:
            flash(u'用户名或密码错误', 'error')
            return redirect(url_for(self.name))

        self.login_user(user)

        session.permanent = 'remember' in request.form

        if 'login_redirect' in session:
            url = session.pop('login_redirect')
            return redirect(url)
        else:
            return redirect(url_for('index'))

    def is_remote_login(self):
        addr = request.remote_addr
        return addr != '127.0.0.1'

    def is_weak_password(self, password):
        ''' 是否弱密码 '''
        # 全数字密码
        if password.isdigit():
            return True
        # 长度少于 16
        if len(password) < 16:
            return True
        # 相同字符数超过总长度的 1/2
        if max(Counter(password).values()) > len(password) * 0.5:
            return True
        return False

    def auth_user(self, username, password):
        guard = app.extensions['guard']
        user = guard.get_user_by_auth(username, password)
        return user

    def login_user(self, user):
        session['user_id'] = user['_id']

class Logout(MethodView):
    ''' 退出 '''

    name = 'logout'
    path = '/logout'

    def get(self):
        self.logout_user()
        flash(u'你已经退出登录', 'warning')
        return redirect(url_for('login'))

    def logout_user(self):
        try:
            del session['user_id']
        except:
            pass

views = [Index, Login, Logout]
