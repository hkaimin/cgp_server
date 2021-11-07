#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, session, flash, redirect, abort, url_for

from flask.ext.admin import Admin
from flask.ext.babelex import Babel
from flask.ext.mongoengine import MongoEngine
from webadmin.views.auth import views as auth_views
from webadmin.views.basic import index_view, error_view
from webadmin.views.account import views as account_views
from webadmin.views.misc import views as misc_views
from webadmin.views.ctr import views as ctr_views
from webadmin.views.res import views as res_views
from webadmin.views.user import views as user_views
from webadmin.views.dev_views.dev import views as dev_views
from webadmin.views.ope import views as ope_views
from webadmin.library.utils import base26
from webadmin.extension.guard import Guard
from webadmin.extension.gamesvr import Gamesvr
from webadmin.extension.zoning import Zoning
from webadmin.extension.statician import Statician


def init_config(app):
    import config as app_config
    app.config.from_object(app_config)


def init_babel(app):
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return 'zh'


def init_databases(app):
    mongdo_db = MongoEngine()
    mongdo_db.init_app(app)


def init_error_handler(app):

    @app.errorhandler(403)
    def error_403(error):
        return error_view.render('error.html',
                                 code=403,
                                 desc='你无权访问这个页面'), 403

    @app.errorhandler(404)
    def error_404(error):
        return error_view.render('error.html',
                                 code=404,
                                 desc='网页不存在'), 404

    if app.debug:
        return

    @app.errorhandler(StandardError)
    def error_standard(error):
        import traceback; traceback.print_exc()
        return error_view.render('error.html', code=500, desc=error), 500


def init_extensions(app):
    guard = Guard()
    guard.init_app(app)

    gamesvr = Gamesvr()
    gamesvr.init_app(app)

    zoning = Zoning()
    zoning.init_app(app)

    statician = Statician()
    statician.init_app(app)


def init_processors(app):

    def allow_for_guest(endpoint, path, method):
        """ 是否允许访客访问 """
        if path.startswith('/api/'):
            return True
        if path.startswith('/static/vendor/'):
            return True
        
        allow_endpoints = ('admin.static', 'login', 'logout')
        if endpoint in allow_endpoints:
            return True

        allow_paths = (
            '/favicon.ico', '/robot.txt',
            '/static/images/welcome.jpg', '/static/styles/login.css',
        )
        if path in allow_paths:
            return True
        return False

    def allow_for_login(endpoint, path, method):
        """ 检查通用无权限限制页面 """
        allow_endpoints = ('static', 'index', 'admin.index')
        if endpoint in allow_endpoints:
            return True
        allows_category = ('error.', 'image.', 'account.', 'gamesvr.')
        for allow in allows_category:
            if endpoint.startswith(allow):
                return True
        return False

    def need_guard_protect(endpoint, path, method):
        not_needed = ('res.index', 'dev.index', 'ope.index')
        return endpoint not in not_needed

    def need_pick_gamesvr(endpoint, path, method):
        prefix = path.split('/')[1]
        return prefix in ('res', 'dev', 'ope')

    guard = app.extensions['guard']
    zoning = app.extensions['zoning']


    @app.context_processor
    def inject_manager():
        return dict(guard=guard, zoning=zoning)

    @app.before_request
    def access_filter():
        endpoint = request.endpoint
        path = request.path
        method = request.method

        if allow_for_guest(endpoint, path, method):
            return

        # 检查登录状态
        if 'user_id' not in session:
            if endpoint is not None and endpoint != 'logout':
                session['login_redirect'] = request.url
            flash(u'你还没有登录', 'error')
            return redirect(url_for('login'))

        # 不存在就 404
        if not endpoint:
            abort(404)

        # 属于通用的页面
        if allow_for_login(endpoint, path, method):
            return

        # 检查受控权限
        if need_guard_protect(endpoint, path, method):
            if not guard.allow_endpoint_me(endpoint, path, method):
                abort(403)

        # 是否属于要先选择服务器的页面
        if need_pick_gamesvr(endpoint, path, method):
            status = zoning.my_gamesvr_status()
            if status == 0:
                return
            if status == 1:
                flash(u'使用此页面要先选择一个服务器', 'error')
            elif status == 2:
                flash(u'之前选择的服务器已经不存在，请重新选择', 'warnning')
            elif status == 3:
                flash(u'之前选择的服务器已经过期，请重新选择', 'warnning')
            return redirect(url_for('gamesvr.index_view'))


def init_template_filter(app):

    @app.template_filter('excel_col')
    def excel_col(number):
        return base26(number)


def init_normal_views(app):
    for view in auth_views:
        app.add_url_rule(view.path, view_func=view.as_view(view.name))


def init_admin_views(app):
    admin = Admin(name=u'大富翁九', index_view=index_view, url='/')
    admin.add_view(error_view)
    all_views = (account_views + misc_views + ctr_views +
                 res_views + user_views + dev_views + ope_views)
    for view in all_views:
        admin.add_view(view)
    admin.init_app(app)


def init_api(app):
    from .api.base import init_api
    init_api(app)


def create_app():
    app = Flask(__name__)
    init_config(app)
    init_babel(app)
    init_databases(app)
    import initadmin; initadmin.init_admin(app)
    init_error_handler(app)
    init_extensions(app)
    init_processors(app)
    init_template_filter(app)
    init_normal_views(app)
    init_admin_views(app)
    init_api(app)

    try:
        from flask.ext.compress import Compress
        Compress(app)
    except ImportError:
        pass

    return app
