#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app
from flask.ext.admin import expose, BaseView
from webadmin.models.user import models as user_models
from webadmin.models.logging import models as logging_models
from webadmin.modelviews.user import UserModelView
from webadmin.modelviews.logging import LoggingModelView


def multi_logging_db(model):
    """ 多日志数据库支持 """
    @classmethod
    def get_db(cls):
        zoning = app.extensions['zoning']
        return zoning.my_logging_db()
    model._get_db = get_db

    # @classmethod
    # def get_collection(cls):
    #     zoning = app.extensions['zoning']
    #     return zoning.my_logging_db()[cls._get_collection_name()]
    # model._get_collection = get_collection

    model._meta['db_alias'] = 'logging_db@noexists'
    model.cls_init()


def multi_user_db(model):
    """ 多用户数据库支持 """
    @classmethod
    def get_db(cls):
        zoning = app.extensions['zoning']
        return zoning.my_user_db()
    model._get_db = get_db

    # @classmethod
    # def get_collection(cls):
    #     zoning = app.extensions['zoning']
    #     return zoning.my_user_db()[cls._get_collection_name()]
    # model._get_collection = get_collection

    model._meta['db_alias'] = 'user_db@noexists'
    model.cls_init()


def create_user_modelviews():
    views = []
    for model in user_models:
        model._meta['db_alias'] = 'user_db'
        multi_user_db(model)

        name = model.__name__.lower()
        endpoint = 'user_model_' + name
        url = '/user/' + name

        view = UserModelView(model, endpoint=endpoint, url=url)
        view.layout_template = '/user.html'
        views.append(view)
    return views


def create_logging_modelviews():
    views = []
    for model in logging_models:
        model._meta['db_alias'] = 'logging_db'
        multi_logging_db(model)

        name = model.__name__.lower()
        endpoint = 'logging_model_' + name
        url = '/user/' + name

        view = LoggingModelView(model, endpoint=endpoint, url=url)
        view.layout_template = '/user.html'
        views.append(view)
    return views


class UserIndexView(BaseView):

    @expose('/')
    def index(self):
        return self.render('user.html')


views = [
    UserIndexView(name=u'用户数据', endpoint='user', url='/user/'),
]
views.extend(create_user_modelviews())
views.extend(create_logging_modelviews())


#------------------------

