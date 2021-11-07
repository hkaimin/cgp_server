#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time

from gevent import sleep, Timeout
from gevent.lock import Semaphore

from corelib import log, spawn

from corelib.gtime import cur_day_hour_time, current_time


from game import Game
from game.define import msg_define, store_define

_logic_free_time = 0
def logic_capacity_check(cell):
    """ 根据逻辑进程容量比率, 返回:
        1=需要增加
        0=不处理
        -1=需要减少
    """
    import config

    c = cell.get_count()

    logic_pool = config.logic_pool
    if c < logic_pool:
        return 1
    elif c == logic_pool:
        return 0

    try:
        count = Game.rpc_player_mgr.get_count()
        c = Game.rpc_sub_player_mgr.count()
    except:
        log.log_except()
        return 0

    total = c * config.logic_players
    rate = float(total - count) / config.logic_players
    if count >= total or rate < 0.2:
        return 1
    global _logic_free_time
    if rate > 1.5 and time.time() - _logic_free_time >= 20*60:
        _logic_free_time = time.time()
        return -1
    return 0

class LogicGame(object):
    _rpc_name_ = 'rpc_logic_game'

    inited = False

    lock_count = 9999

    def __init__(self):
        self.stoping = False
        self.stoped = True
        self.stop_lock = Semaphore(self.lock_count)
        self.stop_mgrs = []

    def wee_hours_task(self):
        """凌晨定时任务"""
        while 1:
            next_time = cur_day_hour_time(hour=24)
            delay = next_time - current_time()
            if delay > 5 * 60:
                sleep(5 * 60)
            else:
                sleep(delay)
                Game.safe_pub(msg_define.MSG_WEE_HOURS)

    def start(self):
        if not self.stoped:
            return False
        self.stoped = False
        #凌晨定时任务
        spawn(self.wee_hours_task)

        for mgr in self.stop_mgrs:
            try:
                if not hasattr(mgr, 'start'):
                    continue
                mgr.start()
            except StandardError as e:
                log.log_except('stop mgr(%s) error:%s', mgr, e)
        return True

    def _stop(self):
        pass

    def stop(self):
        """ 进程退出 """
        if self.stoping:
            return
        self.stoping = True
        log.info(u'game模块(%s)停止', self.__class__.__name__)

        def _stop_func():
            try:
                self._stop()
            except StandardError:
                log.log_except()

            for mgr in self.stop_mgrs:
                try:
                    mgr.stop()
                except StandardError as e:
                    log.log_except('stop mgr(%s) error:%s', mgr, e)
            sleep(0.5)  # 允许其它线程切换
            #等待其它完成
            while self.stop_lock.wait() < self.lock_count:
                sleep(0.1)
        try:
            #保证在30分钟内处理完
            with Timeout.start_new(60 * 30):
                _stop_func()
        except:
            log.log_except()
        log.info('[game]stoped!')
        self.stoped = True

    def add_mgr(self, mgr):
        self.stop_mgrs.append(mgr)
