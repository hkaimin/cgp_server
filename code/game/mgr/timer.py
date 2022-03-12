#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from corelib import log, spawn
from game.define import constant, msg_define, store_define
from corelib.gtime import cur_day_hour_time, current_time, custom_today_ts
from gevent import sleep, Timeout
from game import Game


class Timer(object):
    def __init__(self):
        pass

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

    def one_minute_task(self):
        """1分钟定时器"""

        next_time = 60 - int(time.time()) % 60
        sleep(next_time)

        while 1:
            Game.safe_pub(msg_define.MSG_ONE_MINUTE)
            sleep(60)

    def half_hour_task(self):
        """半小时定时器"""

        next_time = 1800 - int(time.time()) % 1800
        sleep(next_time)

        while 1:
            Game.safe_pub(msg_define.MSG_HALF_HOURS)
            sleep(1800)

    def tow_hours_task(self):
        """两小时定时器"""

        next_time = 7200 - int(time.time()) % 7200
        sleep(next_time)

        while 1:
            Game.safe_pub(msg_define.MSG_TWO_HOURS)
            sleep(7200)

    def eight_fifty_five_pm_task(self):
        todayTs = custom_today_ts(20, 55, 0)
        interval = todayTs - int(time.time())
        if int(time.time()) > todayTs:
            interval += 24 * 60 * 60

        sleep(interval)

        while 1:
            Game.safe_pub(msg_define.MSG_EIGHT_FIFTY_FIVE_PM)
            sleep(24 * 60 * 60)

    def nine_pm_task(self):
        todayTs = custom_today_ts(21, 0, 0)
        interval = todayTs - int(time.time())
        if int(time.time()) > todayTs:
            interval += 24*60*60

        sleep(interval)

        while 1:
            Game.safe_pub(msg_define.MSG_NINE_PM)
            sleep(24*60*60)

    def start(self):
        spawn(self.one_minute_task)
        spawn(self.wee_hours_task)
        spawn(self.half_hour_task)
        spawn(self.tow_hours_task)
        spawn(self.eight_fifty_five_pm_task)
        spawn(self.nine_pm_task)
