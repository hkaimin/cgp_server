#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

from flask import jsonify, Flask, request, json, abort

from corelib import log


api_app = None
if 0:
    api_app = Flask('temp')
prefix = '/api/v1/'
ep_prefix = 'api_'

#返回状态码定义
RS_OK = 1
RS_QUERY_ERROR = -1
RS_PARAM_ERROR = -2


class ParamError(StandardError):
    pass


def api_route(**kw):
    if 'methods' not in kw:  # 默认方法
        kw['methods'] = ('POST', 'GET')

    def _func(f):
        f._routed = True
        f._kw = kw
        return f
    return _func


class ApiMeta(type):
    @staticmethod
    def init_route(cls, dct):
        names = dct.get('url')
        if not names:
            return
        obj = cls(api_app)
        obj.init_route()

    def __new__(cls, name, bases, dct):
        """ 类定义后,注册路由 """
        rs = super(ApiMeta, cls).__new__(cls, name, bases, dct)
        ApiMeta.init_route(rs, dct)
        return rs


def _wrap_f(f):
    @wraps(f)
    def _func(*args, **kw):
        try:
            return f(*args, **kw)
        except ParamError as e:
            return jsonify(dict(code=RS_PARAM_ERROR, data=e.message))
        except Exception as e:
            log.log_except()
            return jsonify(dict(code=RS_PARAM_ERROR, data=str(e)))
    return _func


class BaseApiView(object):
    __metaclass__ = ApiMeta
    url = None

    def __init__(self, app):
        self.app = app
        if 0:
            self.app = Flask()

    @property
    def gamesvr(self):
        if 0:
            from webadmin.extension.gamesvr import Gamesvr
            return Gamesvr()
        return self.app.extensions['gamesvr']

    def init_route(self):
        """ 注册url路由 """
        names = self.url
        if not names:
            return
        cls_url = '%s%s' % (prefix, '/'.join(names))
        cls_endpoint = '%s%s' % (ep_prefix, '_'.join(names))
        for k in dir(self):
            f = getattr(self, k)
            if not getattr(f, '_routed', False):
                continue
            kw = f._kw
            url, ep = kw.pop('url', None), kw.pop('endpoint', None)
            if url is None:
                url = cls_url
            if ep is None:
                ep = cls_endpoint
            self.app.add_url_rule(url, ep, _wrap_f(f), **kw)

    @property
    def zoning(self):
        return self.app.extensions['zoning']

    def get_res_db(self, svr_id):
        """ 获取资源库 """
        return self.zoning.get_resource_db(svr_id)

    def get_user_db(self, svr_id):
        """ 获取用户库 """
        return self.zoning.get_user_db(svr_id)

    def parse_params(self):
        """ 校验、分析输入的参数,返回参数字典 """
        try:
            data = request.get_data()
            params = json.loads(data)
            #检查数据合法性

            return params
        except Exception as e:
            raise ParamError(e.message)

    def success(self, result):
        return jsonify(dict(code=RS_OK, data=result))


def init_api(app):
    global api_app
    print("init api...")
    api_app = app
    from . import api_data, api_ctrl
    api_data.init()


#------------------------
#------------------------
#------------------------
