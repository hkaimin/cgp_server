#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import *


class CtrlApi(BaseApiView):
    url = ('ctrl', )

    @api_route(methods=('POST', 'GET'))
    def get(self):
        print("Ctrl Api get")
        params = self.parse_params()
        name = 'api_%s' % params['name']
        f = getattr(self, name)
        rs = f(params['param'])
        return self.success(rs)

    def _get_svr(self, svrid):
        svr = self.zoning.gamesvrs[svrid]
        return svr['host'], svr['port']

    def _add_coin(self, params, name):
        """ 加金币,幸运星 """
        svrid, pid, count = params['svrid'], params['pid'], params['count']
        host, port = self._get_svr(svrid)
        kw = {name: count}
        coin1, coin2 = self.gamesvr.add_coin(host, port, pid, **kw)
        rs = dict(coin1=coin1, coin2=coin2)
        return dict(count=rs[name])
    
    def api_dump_dbe(self,params):
        print("apid dumpDbe")
    
    def add_addluckycoin(self, params):
        """ 加幸运星 """
        return self._add_coin(params, 'coin1')

    def api_addgoldcoin(self, params):
        """ 加金币 """
        return self._add_coin(params, 'coin2')


def init():
    pass

#------------------------
#------------------------
#------------------------
