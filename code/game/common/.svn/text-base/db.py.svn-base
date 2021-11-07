#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gevent.lock import RLock

from corelib import log
from store.store import Store
from game.define.store_define import *
import config

class BaseGameStore(Store):
    def init(self, url, **dbkw):
        self.pool_get_size = dbkw.pop('pool_get_size', 10)
        self.pool_set_size = dbkw.pop('pool_set_size', 10)
        super(BaseGameStore, self).init(url, **dbkw)

class GameStore(BaseGameStore):
    STORE_INFOS = GAME_CLS_INFOS

class ResStore(BaseGameStore):
    STORE_INFOS = RES_CLS_INFOS
    KEY_DB_VER = '_db_ver_'

    def __init__(self):
        # setattr(Game, self._rpc_name_, self)
        BaseGameStore.__init__(self)
        self.lock = RLock()

class PayStore(BaseGameStore):
    STORE_INFOS = RES_CLS_INFOS


def new_game_store():
    # #资源库
    # res_store = ResStore()
    # res_store.init(config.db_engine_res, **config.db_params_res)
    # res_store.start()
    # #支付库
    # pay_store = PayStore()
    # if getattr(config, 'db_engine_pay', None) is not None:
    #     pay_store.init(config.db_engine_pay, **config.db_params_pay)
    # else:
    #     pay_store.init(config.db_engine_res, **config.db_params_res)
    # pay_store.start()
    #游戏库
    store = GameStore()
    store.init(config.db_engine, **config.db_params)
    store.start()
    return store



#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
