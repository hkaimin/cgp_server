#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app
from flask.ext.admin import expose, BaseView
from webadmin.models.resource import models
from webadmin.modelviews.resource import (
        ResourceModelView, AiCodeResourceModelView, ErrorModelView)
from .mapeditor import MapEditorView


def multi_resource_db(model):
    """ 多资源库数据库支持 """

    @classmethod
    def get_db(cls):
        zoning = app.extensions['zoning']
        return zoning.my_resource_db()

    model._get_db = get_db
    # 覆盖 get_collection 函数
    # model._get_collection = get_collection

    # meta 里的 db_alias 无意义了，随便设置一个不存在的
    model._meta['db_alias'] = 'resource_db@noexists'
    model.cls_init()


def create_resource_modelviews():
    views = []
    for model in models:
        model._meta['db_alias'] = 'resource_db'
        multi_resource_db(model)

        name = model.__name__.lower()
        endpoint = 'resource_model_' + name
        url = '/res/' + name

        if name == 'aicode':
            view = AiCodeResourceModelView(model, endpoint=endpoint, url=url)
            view.upload_template = 'upload_aimm.html'
        elif name == 'error':
            view = ErrorModelView(model, endpoint=endpoint, url=url)
        else:
            view = ResourceModelView(model, endpoint=endpoint, url=url)
        view.layout_template = 'res.html'

        views.append(view)
    return views


class ResIndexView(BaseView):

    @expose('/')
    def index(self):
        return self.render('res.html')

views = [
    ResIndexView(name=u'资源管理', endpoint='res', url='/res/'),
    MapEditorView(name=u'地图编辑', endpoint='mapeditor', url='/res/mapeditor'),
]
views.extend(create_resource_modelviews())

