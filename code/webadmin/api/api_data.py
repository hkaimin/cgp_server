#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import *
from store.driver import *

pre_url = 'data'


class DataView(BaseApiView):
    """ 数据类 """
    pass


class Groups(DataView):
    """ 游戏组(运营商列表) """
    url = (pre_url, 'groups')

    @api_route(methods=('POST', 'GET'))
    def get(self):
        db = self.zoning.system_db()
        docs = list(db['zone'].find())
        return jsonify({"data": docs})


class Servers(DataView):
    """ 游戏服列表 """
    url = (pre_url, 'servers')

    @api_route(methods=('POST', 'GET'))
    def get(self):
        db = self.get_user_db(1)
        docs = list(db['player'].find(limit=10))
        return jsonify({"data": docs})


class UserData(DataView):
    """ 用户库数据同步
    测试:
    curl -d "{\"serverid\":1, \"tbname\":\"p_attr\"}" "http://192.168.0.51:5000/api/v1/data/datasync"
    """
    url = (pre_url, 'datasync')

    def _result(self, docs):
        return jsonify(dict(code=1, data=docs))

    @api_route(methods=('POST', 'GET'))
    def get(self):
        params = self.parse_params()
        svr_id = params['serverid']
        tbname = params['tbname']
        db = self.get_user_db(svr_id)
        docs = list(db[tbname].find())
        return self._result(docs)


class DataApi(DataView):
    """ 数据查询 """
    url = (pre_url, )
    WHERE2OP = {
        '=': lambda name, op, v: (name, v),
        '>': FOP_GT,
        '>=': FOP_GTE,
        '<': FOP_LT,
        '<=': FOP_LTE,
        '!=': FOP_NE,
        'in': FOP_IN,
    }

    @api_route(methods=('POST', 'GET', ))
    def get(self):
        params = self.parse_params()
        name = 'api_%s' % params['name']
        f = getattr(self, name)
        return f(params['param'])

    def api_operatorlist(self, params):
        """ 运营商列表 """
        db = self.zoning.system_db()
        docs = [dict(id=d['_id'], name=d['name']) for d in db['zone'].find()]
        return self.success(docs)

    def api_gameserverlist(self, params):
        """ 游戏服列表
        curl -d "{\"name\":\"gameserverlist\", \"param\":{\"opid\":1}}" "http://192.168.0.51:5000/api/v1/data"
        """
        opid = params['opid']
        zoning = self.zoning
        docs = [dict(id=sid, name=svr['name']) for sid, svr in zoning.gamesvrs.iteritems() if svr['zone'] == opid]
        return self.success(docs)

    def api_datasync(self, params):
        """ 数据查询
        curl -d "{\"name\":\"datasync\", \"param\":{\"svrid\":1, \"tbname\":\"player\", \"fields\":[\"name\"], \"limit\":10}}" "http://192.168.0.51:5000/api/v1/data"
        """
        svrid = params['svrid']
        tbname = params['tbname']
        where = params.get('where', {})
        limit = params.get('limit', 100)
        fields = params.get('fields', None)
        mwhere = {}
        for name, ops in where.items():
            for op, v in ops.items():
                f = self.WHERE2OP[op]
                if callable(f):
                    k, v = f(name, op, v)
                    mwhere[k] = v
                else:
                    mwhere.setdefault(name, {})
                    mwhere[name][f] = v
        db = self.get_user_db(svrid)
        docs = list(db[tbname].find(spec=mwhere, fields=fields, limit=limit))
        return self.success(docs)


def init():
    pass

#------------------------
#------------------------
#------------------------


