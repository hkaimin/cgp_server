#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time

from corelib.message import observable
from corelib import spawn_later, log, spawn
from corelib.gtime import current_time

from game import Game
from game.models.mail import ModelMail
from game.core.PlayerMail import MailBase

# 所有对外接口全部加上rc_
@observable
class globalMail(object):
    DATA_CLS = ModelMail

    def __init__(self):

        self.loaded = False
        self.data = None #全局邮件数据字典
        self.pMailObjCache = {}  # 玩家邮件对象缓存
        self.save_time = current_time()
        pass

    def init(self):
        pass

    def markDirty(self):
        self.data.modify()

    def save(self, forced=False):
        self.save_time = current_time()
        # 此处加log
        # log.debug('tree(%s) save', self.save_time)
        # print "----- log save debug"
        # if self.data.modified: # 如果数据脏了，树对象重新导出字典
        #     self.tree_to_dict()
        self.data.save(Game.store, forced=forced)

    def load(self):
        if self.loaded:
            return
        self.loaded = True
        print "----- log load debug"
        # log.debug('tree(%s) load', self.save_time)

    @classmethod
    def load_mail(cls, serverid):
        """ 根据pid加载Player对象 """
        data = cls.DATA_CLS.load(Game.store, serverid)  # 这里用serverid做ke
        if data is None:
            return
        mail = cls()
        mail.data = data
        mail.load()
        return mail

    def clean(self):
        pass

    def test_mail(self):
        print "----test_mail"
        pass

    # 初始化获取上家邮件信息
    def getParentMail(self, puid):
        d = self.rc_getMailByRid(puid) # rpc 从缓存里面取邮件
        #print "-------d",puid,d
        data = d
        playermail  = {}
        for mailTranceNo, mData in data.iteritems():
            mailObj = MailBase()
            mailObj.load_from_dict(mData)
            playermail[mailTranceNo] = mailObj
        self.pMailObjCache[puid] = playermail

    # 序列化打包邮件信息的时候要用到(有权限发邮件的上家)
    def to_mails_list_parent(self, mailObjData):
        mails_list = []
        for mid, mobj in mailObjData.iteritems():
            mails_list.append(mobj.to_little_data())
        return mails_list



    # ===================== 对外接口 ======================
    def rc_playerlogin(self, code):
        pass

    # 如果上家退出，删除对应缓存
    def rc_playerlogout(self, rid):
        mailObjData = self.pMailObjCache.get(rid, None)
        if mailObjData:
            del self.pMailObjCache[puid]
        pass

    # 根据rid获取邮件, 数据库load出来的数据
    def rc_getMailByRid(self, rid):
        dMails = self.data.mailDict.get(rid, {})
        return dMails

    # 编写邮件
    def rc_addMail(self, rid, mdata):
        print "==========rc_addMail", rid, mdata
        if mdata == None:return
        rid = str(rid)
        if type(mdata) != types.DictType:
            print "error type %s, type must be dict"%type(mdata)
            return
        mid = "%s-%s" % (rid, self.data.GenerateMailTranceNo())
        dMails = self.data.mailDict.get(rid, {})
        #print "rc_addMail", dMails, mdata
        mdata["iOwner"] = rid  # 拥有者id
        mdata["mailTranceNo"] = mid  # 分配邮件id
        mdata["iCreattime"] = int(time.time()) # 创建时间

        newMail = MailBase()
        newMail.load_from_dict(mdata)
        data = newMail.to_save_dict(True) # 格式化输出存储字典

        dMails[mid] = data
        self.data.mailDict[rid] = dMails
        #print "---self.data.mailDict",self.data.mailDict

        self.markDirty()
        self.save(True)
        return data

    # rpc 初始化获取上家邮件信息
    def rc_getParentMail(self, code):
        mails_list = []
        if code == "":
            print "code is None"
            return mails_list
        puid = Game.rpc_membtree_svr.rc_check_mail_uid(code)  # 上家的uid
        #print "---rc_check_mail_uid", puid
        puid = str(puid)
        mailObjData = self.pMailObjCache.get(puid, None)
        if not mailObjData: # 如果缓存中没有
            self.getParentMail(puid)
            mailObjData = self.pMailObjCache.get(puid, None)
        mails_list = self.to_mails_list_parent(mailObjData)
        return mails_list

    # rpc 初始化获取上家邮件mid列表
    def rc_getMailMidList(self, code):
        mails_list = []
        if code == "":
            print "code is None"
            return mails_list
        puid = Game.rpc_membtree_svr.rc_check_mail_uid(code)  # 上家的uid
        print "puid:",puid
        puid = int(puid)
        mailObjData = self.pMailObjCache.get(puid, None)
        if not mailObjData: # 如果缓存中没有
            self.getParentMail(puid)  # 初始化加入到缓存
            mailObjData = self.pMailObjCache.get(puid, None)
        mails_list = mailObjData.keys()
        return mails_list

    # rpc 获取邮件详细信息
    def rc_readDetail(self, mid):
        mailobj = self.pMailObjCache.get(mid, None)
        mid = int(mid)
        if not mailobj:return
        data = mailobj.to_big_data()
        return data



import types
#---------------------
#---------------------
#---------------------


