#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import re

from gevent import sleep

from corelib import log
from corelib import spawn, message
from corelib.process import BaseApp, daemon
from corelib.frame import AbsMainApplication, Game, MSG_APP_FSTART
import game
import config

@message.observable
class Application(BaseApp, AbsMainApplication):
    EXTRA_CMDS = []

    def __init__(self):
        BaseApp.__init__(self)
        AbsMainApplication.__init__(self, config)
        self.restarted = False
        self.started_app = set()
        self.all_started = False
        self.sub(MSG_APP_FSTART, self.msg_app_fstart)


    def start(self):
        self.init_frame()
        self.frame.start()

        self._init_web()
        self.web_svr.start()
        log.info('app started')
        # spawn_later(2, self.stop)
        while 1:
            try:
                self._waiter.wait()
                break
            except KeyboardInterrupt:
                log.info('app stoped:KeyboardInterrupt')
            except SystemExit:
                log.info('app stoped:SystemExit')
            except:
                log.log_except()
                break
            log.info('spawn app stop')
            spawn(self.stop)
            sleep(0.2)
        cmd = ' '.join(map(str, [sys.executable,] + sys.argv))
        log.info('*****app(%s) stoped', cmd)
        self.stop()


        #守护进程方式,重启服务
        if self.restarted and hasattr(self, 'daemon_runner'):
            self.daemon_runner.domain_restart()

    def msg_app_fstart(self, app_name, addr, names):
        self.started_app.add(app_name)
        if self.all_started:
            sub_proxy = self.frame.sub_proxys[tuple(addr)]
            sub_proxy.app_after_start() # 所有配置表子进程加载完后，还有新的子进程加入调用
            pass
        if len(self.started_app) == self.total_app_count():
            print "-----------------------ALL SUB PROXY START IN GAME !!!!!"
            for addr, sub_proxy in self.frame.sub_proxys.items():
                sub_proxy.after_all_sub_start() # 所有配置表的子进程加载完之后调用
            self.all_started = True
        pass

    def total_app_count(self):
        return len(config.frames)

    def _init_web(self):
        from gevent import pywsgi
        from corelib.geventfix import Http10WSGIHandler
        from game.gm import webapp

        web_addr = ('0.0.0.0', config.web_addr[1])
        self.wsgi_app = webapp.get_wsgi_app()
        self.web_svr = pywsgi.WSGIServer(web_addr,
            self.wsgi_app, log=log if config.debug else None,
            environ=os.environ,
            handler_class=Http10WSGIHandler)
        self.web_svr.reuse_addr = 1
        self.web_svr.environ['SERVER_NAME'] = 'game'
        log.info('game web:%s', web_addr)

    def _stop_game(self):
        """ 按顺序停止游戏 """

        try:
            game.Game.rpc_player_mgr.pause()
        except:
            pass

        try:
            for addr, logic in Game.rpc_logic_game:
                if logic:
                    logic.stop()
        except:
            log.log_except()
        finally:
            self.frame.before_stop()

    def stop(self):
        if self.stoped:
            return
        self.stoped = True
        log.warn(u'管理进程开始退出')
        try:
            self.web_svr.stop()
            log.warn(u'管理进程:stop_game')
            self._stop_game()
            log.warn(u'管理进程:stop_frame')
            self.frame.stop()
        except:
            log.log_except()
        finally:
            self._waiter.set()

    def restart(self, m, msg=None):
        """ 过min分钟后,自动重启, """
        spawn(self._restart, m, msg)

    def _restart(self, m, msg, restart=True):
        if restart:
            amsg = u'重启'
        else:
            amsg = u'关闭维护'
        if msg is None:
            msg = u'服务器将在%%(min)s分钟后%s, 谢谢!' % amsg

        sleep(1)
        self.restarted = restart
        self._waiter.set()


def main():
    app = Application()
    daemon(app)

if __name__ == '__main__':
    main()

