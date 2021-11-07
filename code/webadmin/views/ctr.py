#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.admin import expose, BaseView
from webadmin.models.system import models
from webadmin.modelviews.system import SystemModelView
from .system_summary import SystemSummaryView
from .system_permission import SystemPermissionView
from .system_guard import SystemGuardView
from .system_zoning import SystemZoningView
from .system_user import SystemUserView
from .system_group import SystemGroupView

def create_system_modelviews():
    views = []
    for model in models:
        model._meta['db_alias'] = 'default'
        name = model.__name__.lower()
        endpoint = 'system_model_' + name
        url = '/ctr/' + name
        view = SystemModelView(model, endpoint=endpoint, url=url)
        view.layout_template = 'ctr.html'
        views.append(view)
    return views

class CtrIndexView(BaseView):

    @expose('/')
    def index(self):
        return self.render('ctr.html')

views = [
    CtrIndexView(name=u'控制面板',
                 endpoint='ctr',
                 url='/ctr/'),
    SystemSummaryView(name=u'基本信息',
                      endpoint='system_summary',
                      url='/ctr/system_summary'),
    SystemPermissionView(name=u'权限信息',
                         endpoint='system_permission',
                         url='/ctr/system_permission'),
    SystemGuardView(name=u'权限设置',
                    endpoint='system_guard',
                    url='/ctr/system_guard'),
    SystemZoningView(name=u'服务器组设置',
                     endpoint='system_zoning',
                     url='/ctr/system_zoning'),
    SystemUserView(name=u'用户管理',
                   endpoint='system_user',
                   url='/ctr/system_user/'),
    SystemGroupView(name=u'用户组管理',
                   endpoint='system_group',
                   url='/ctr/system_group/'),
]
views.extend(create_system_modelviews())


