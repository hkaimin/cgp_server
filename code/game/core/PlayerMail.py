#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from game.common import utility
from game import Game

#所有邮件基类
class MailBase(utility.DirtyFlag):
    def __init__(self):
        utility.DirtyFlag.__init__(self)
        self.mailTranceNo = ''  # 邮件唯一id （添加给角色才生成， 否则为一个系统设定值）角色id + 自增
        self.iOwner = 0 #拥有者id
        self.sTitle = '' # 邮件标题
        self.sContent = '' # 邮件内容
        self.iCreattime  = int(time.time()) #生成时间

        self.save_cache = {}  # 存储缓存

    def set_owner(self, owner):
        if not self.itemTranceNo:
            self.iOwner = owner.id
            self.mailTranceNo = "%s-%s"%(self.iOwner, owner.data.GenerateMailTranceNo())
            self.markDirty()

    def markDirty(self):
        utility.DirtyFlag.markDirty(self)

    # 存库数据
    def to_save_dict(self, forced=False):
        if self.isDirty() or forced:
            self.save_cache = {}
            self.save_cache["mailTranceNo"] = self.mailTranceNo
            self.save_cache["iOwner"] = self.iOwner
            self.save_cache["sTitle"] = self.sTitle
            self.save_cache["sContent"] = self.sContent
            self.save_cache["iCreattime"] = self.iCreattime
        return self.save_cache

    # 读库数据初始化
    def load_from_dict(self, data):
        self.mailTranceNo = data.get("mailTranceNo", '')  # 邮件唯一id （添加给角色才生成， 否则为一个系统设定值）角色id + 自增
        self.iOwner = data.get("iOwner", 0)  # 拥有者id
        self.sTitle = data.get("sTitle", 0)  # 邮件标题
        self.sContent = data.get("sContent", 0)  # 邮件内容
        self.iCreattime = data.get("iCreattime", 0)  # 生成时间

    def to_big_data(self):
        pack_data = {}
        pack_data["iMail"] = self.mailTranceNo
        pack_data["sMailTitle"] = self.sTitle
        pack_data["sMailContent"] = self.sContent
        pack_data["iMailData"] = self.iCreattime
        return pack_data

    def to_little_data(self):
        pack_data = {}
        pack_data["iMail"] = self.mailTranceNo
        pack_data["sMailTitle"] = self.sTitle
        pack_data["iMailData"] = self.iCreattime
        return pack_data


class PlayerMail(utility.DirtyFlag):
    def __init__(self, who):
        utility.DirtyFlag.__init__(self)
        self.owner = who
        # self.parentMailDict = {}  # 上级发的邮件
        self.mailRead = []  # 已读的邮件id列表
        self.unRead = 0
        self.save_cache = {}  # 存储缓存
        pass


    def markDirty(self):
        utility.DirtyFlag.markDirty(self)

    def to_save_dict(self, forced=False):
        if self.isDirty() or forced:
            self.save_cache = {}
            self.save_cache['mailRead'] = self.mailRead  # 已读邮件列表
        return self.save_cache

    def load_from_dict(self, data):
        self.mailRead = data.get('mailRead', [])
        # self.getParentMail()
        pass


    # ==================== 对外接口 =========================

    # 获取邮件详细信息
    def readDetail(self, mid):
        data = Game.rpc_mail_svr.rc_readDetail(mid)
        return data
    #
    # # 获取邮件列表
    def getAllMail(self):
        mails_list = Game.rpc_mail_svr.rc_getParentMail(self.owner.base.code)
        return mails_list

    # 登录检测红点, 这里有问题
    def checkLoginReadPoint(self):
        print "checkLoginReadPoint self.owner.base----------", self.owner.base, self.owner, self.owner.base.code
        maillist = []
        if not self.owner.base.code:
            self.owner.base.code = Game.rpc_membtree_svr.rc_getCode(self.owner.data.id)
        if self.owner.base.code:
            maillist = Game.rpc_mail_svr.rc_getMailMidList(self.owner.base.code)
        print "----maillist", maillist, type(maillist)
        readcount = 0
        for mid in self.mailRead:
            if mid in maillist:
                readcount = readcount + 1
        unread = len(maillist) - readcount
        self.unRead = unread
        return unread

    # 添加已读
    def addReadMail(self, mid):
        if mid in self.mailRead: return
        self.mailRead.append(mid)
        self.markDirty()
        pass


    # # 序列化打包邮件信息的时候要用到(有权限发邮件的上家)
    # def to_mails_list_parent(self):
    #     mails_list = []
    #     for mid, mobj in self.parentMailDict.iteritems():
    #         mails_list.append(mobj.to_little_data())
    #     return mails_list

    # # 初始化获取上家邮件信息
    # def getParentMail(self):
    #     code = self.owner.base.code
    #     puid = Game.rpc_membtree_svr.rc_check_mail_uid(code)
    #     d = Game.rpc_mail_svr.rc_getMailByRid(puid) # rpc 从缓存里面取邮件
    #     data = d
    #     for mailTranceNo, mData in data.iteritems():
    #         mailObj = MailBase()
    #         mailObj.load_from_dict(mData)
    #         self.parentMailDict[mailTranceNo] = mailObj
    #     pass


# class MailMgr(object):
#     def __init__(self):
#         pass
