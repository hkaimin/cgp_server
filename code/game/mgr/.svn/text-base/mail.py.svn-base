#!/usr/bin/env python
# -*- coding:utf-8 -*-
# import os
import time
from game import Game
# from game.define import log_define
from corelib import spawn, spawns, log
from game.core.globalMail import globalMail
from corelib.gtime import current_time
from gevent import sleep
from game.common import utility
from game.core.player import Player
import config
from game.define.store_define import TN_P_MAIL
# NOTE： 进程退出的时候还需要再存一次

class MailMgr(object):
    """ 邮件管理类 """
    _rpc_name_ = 'rpc_mail_svr'
    #定时保存时间 6分钟 # 和角色数据存盘时间错开
    _SAVE_TIME_ = 60 * 6
    def __init__(self):
        self.mailMgr = None  # 全局邮件管理对象
        self._loop_task = None
        self.stoping = False

    def start(self):
        print "------------- mail start"
        self._loop_task = spawn(self._loop)
        pass

    def stop(self):
        """ 进程退出 """
        if self.stoping:
            return
        self.stoping = True
        # 退出前树进行强制保存，以防数据丢失
        self.save_mail()
        if self._loop_task:
            self._loop_task.kill(block=False)
            self._loop_task = None

    def _loop(self):
        """ 定时保存等处理 """
        stime = 60
        while 1:
            sleep(stime)
            try:
                pass
                self.save_mail(True)
            except:
                print "save mail exception2"

    def save_mail(self, isLoopTask=False):
        mail = self.mailMgr
        if mail:
            try:
                if mail.save_time + self._SAVE_TIME_ <= time.time():
                    mail.save()
                    if isLoopTask:
                        sleep(0.01)
            except:
                print "save mail exception"

    # 所有进程都启动后，再从库里初始化
    def after_all_start(self):
        # 从数据库初始化树 -
        # self.check_has_mail()
        # self.mailMgr = globalMail.load_mail(config.serverNo)  # 每个区号对应一个全局邮件表
        pass

    # def check_has_mail(self):
    #     # mongo返回的是[dict,]
    #     lMailData = Game.store.query_loads(TN_P_MAIL, dict(id=config.serverNo))
    #     if len(lMailData) == 0: # 数据库中没有树对象，则创建根节点，预留
    #         self.make_mail()
    #         pass
    #     pass

    # def make_mail(self):
    #     Game.store.insert(TN_P_MAIL, {"id": config.serverNo, "mailDict": {}})
    #     pass

    def init(self):
        # print "------------ tree init"
        pass



    # # ================== 对外接口 =================
    #
    # def rc_playerlogin(self, code):
    #     self.mailMgr.rc_playerlogin(code)
    #     pass
    #
    # # 如果上家退出，删除对应缓存
    # def rc_playerlogout(self, rid):
    #     self.mailMgr.rc_playerlogout(rid)
    #     pass
    #
    # # 根据rid获取邮件
    # def rc_getMailByRid(self, rid):
    #     dMails = self.mailMgr.rc_getMailByRid(rid)
    #     return dMails
    #
    # # 编写邮件
    # def rc_addMail(self, rid, mdata):
    #     self.mailMgr.rc_addMail(rid, mdata)
    #
    # # rpc 初始化获取上家邮件信息
    # def rc_getParentMail(self, code):
    #     mails_list = self.mailMgr.rc_getParentMail(code)
    #     return mails_list
    #
    # # rpc 初始化获取上家邮件mid列表
    # def rc_getMailMidList(self, code):
    #     mails_list = self.mailMgr.rc_getMailMidList(code)
    #     return mails_list
    #
    # # rpc 获取邮件详细信息
    # def rc_readDetail(self, mid):
    #     data = self.mailMgr.rc_readDetail(mid)
    #     return data




def new_mail_Mgr():
    mailMgr = MailMgr()
    mailMgr.init()
    return mailMgr





#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
