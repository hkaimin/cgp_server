#!/usr/bin/env python
# -*- coding:utf-8 -*-

import weakref
import time
import uuid
import copy
import random
import json

import time
import weakref

from corelib import log, spawn
from corelib.gtime import current_time
from corelib.message import observable
from gevent import sleep
from gevent.lock import RLock

from corelib.message import observable
from corelib import spawn_later, log, spawn
from corelib.gtime import current_time, current_hour, get_days

from game import Game
from game.core.playerBase import PlayerBase
from game.define import errcode, msg_define, constant, protocol_define
from game.models.player import ModelPlayer
from cycleData import CycleDay, CycleWeek, CycleMonth, CycleHour, CycleCustom
from playerBase import PlayerBase
from game.models.player import ModelPlayer
import netcmd
from game.define.constant import *
import os


def _wrap_lock(func):
    def _func(self, *args, **kw):
        with self._lock:
            return func(self, *args, **kw)
    return _func

class BasePlayer(object):
    def __init__(self):
        self._handler = None
        #玩家锁,串行玩家操作
        self._lock = RLock()
        self.reconnected = False
        # self.netCmd = netcmd.netCmd()


    def __enter__(self):
        self._lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()

    @property
    def process_id(self):
        return self._handler.rpc.pid if not self.disconnected else 0

    @property
    def disconnected(self):
        """ 是否断线状态 """
        return not self._handler or self._handler.rpc is None

    def call(self, fname, data, noresult=False):
        """ 发送消息
        不能将player.send=self._handler.send,因为player对象使用grpc暴漏给其它进程,grpc有缓存,
        并且player对象也缓存长期存在;当断线重连,player会从新设置新的handler,新的send,
        但是通过grpc调用rpc_player.send一样会调用旧的方法
        """
        if self._handler:
            self._handler.call(fname, data, noresult=noresult)

    def getProcesserInfo(self):
        if self._handler:
            return self._handler.getProcesserInfo()

    def set_process(self, process):
        """ 设置processer """
        self._handler.set_rpc(process)
        if process:
            process.set_lock(self._lock)

    def set_handler(self, hd, process=None):
        """ 添加player handler """
        log.debug('player(%s)(%s) set_handler(%s, %s)', self.id, id(self), id(hd) if hd else hd,
                                                        id(process) if process else process)
        if self._handler is not None:
            self._handler.uninit()
        self._handler = hd
        if hd is not None:
            hd.player = self
            self.set_process(process)
        if 0:
            from game.protocal.player import PlayerRpcHandler
            self._handler = PlayerRpcHandler()

    def getHandler(self):
        return self._handler

    def on_close(self):
        """ 网络关闭的处理,需要实现断线保护 """
        print 'player(%s)on_close'%self.id
        log.debug('player(%s)on_close', self.id)
        sleep(0.05)  # 等待其它接口完成
        # self._close_task = spawn_later(self.SAFE_CLOSE_TIMES,
        #                 lambda: self.disconnected and self.logout())
        self.logout()

    def _clear_reconnect(self):
        if self._close_task:
            self._close_task.kill()
            self._close_task = None

    def reconnect(self, process):
        """ 重连 """
        log.debug(u'[player]玩家(%s)重连', self.id)
        if not self._handler:  # 已经释放不能重连
            sleep(0.5)  # 等待本对象释放
            return False
        self._clear_reconnect()
        self.reconnected = True
        self.set_process(process)
        return True

    # 广播
    def broadcast(self, fname, data):
        spawn(self.call, fname, data, noresult=True)

    # 系统提示
    def notify(self, tips=""):
        if not tips: return
        data = {"tips":tips}
        self.broadcast("notify",data)


@observable
class Player(BasePlayer, netcmd.netCmd):
    _wrefs = weakref.WeakKeyDictionary()
    SAFE_CLOSE_TIMES = 60 * 30  # 25分钟
    DATA_CLS = ModelPlayer


    def __init__(self):
        Player._wrefs[self] = None
        BasePlayer.__init__(self)
        netcmd.netCmd.__init__(self) # 玩家上行协议处理入口
        self.UID = 0
        self.logined = False
        self.uninited = False
        self.loaded = False
        self.save_time = current_time()
        self.relogin_token = ""  # 重连令牌
        self._close_task = None

        self.data = None #玩家数据模型

        self.rpc_room = None #玩家远程服代理】
        self.rpc_room_id = 0
        self.cycleHour = CycleHour(self)  # 小时周期数据
        self.cycleDay = CycleDay(self)  # 天周期数据
        self.cycleDay_2 = CycleDay(self, keepCyc=2)  # 天周期数据 保存2天内的
        self.cycleDay_7 = CycleDay(self, keepCyc=7)  # 天周期数据 保存7天内的
        self.cycleWeek = CycleWeek(self)  # 周周期数据
        self.cycleMonth = CycleMonth(self)  # 月周期数据

        self.base = PlayerBase(self)  # 角色基础信息
        # self.mail = PlayerMail(self)  # 邮件
        self.WaitingRoomid = 0
        #ctn
        # self.testctn = None
        self.afterLogin_timmer = None
        self.isRelogin = 0
        self.FriendRoomID = 0
        self.sub(msg_define.MSG_ROLE_LEVEL_UPGRADE, self.event_lv_uprade)
        pass


    def init_res(self):
        pass

    @property
    def id(self):
        return self.data.id

    @property
    def name(self):
        return self.data.name

    def markDirty(self):
        self.data.modify()

    def getUID(self):
        return self.id



    @_wrap_lock
    def save(self, forced=False):
        log.debug('player(%s) save', self.id)
        self.save_time = current_time()
        self.data.save(Game.store, forced=forced)

    def load(self):
        if self.loaded:
            return
        self.loaded = True
        log.debug('player(%s) load', self.id)
        # print "----- player self.data", self.data, self.data.base
        # self.cycleHour.load_from_dict(self.data.cycleHourDict)  # 小时周期数据
        # self.cycleDay.load_from_dict(self.data.clcleDayDict)  # 天周期数据
        # self.cycleDay_7.load_from_dict(self.data.clcleDay7Dict)  # 天周期数据 保存7天内的
        # self.cycleWeek.load_from_dict(self.data.cycleWeekDict)  # 周周期数据
        # self.cycleMonth.load_from_dict(self.data.cycleMonthDict)  # 月周期数据

        self.cycleHour.load_from_dict(self.data.cycleHourBytes)  # 小时周期数据
        self.cycleDay.load_from_dict(self.data.clcleDayBytes)  # 天周期数据
        self.cycleDay_2.load_from_dict(self.data.clcleDay2Bytes)  # 天周期数据 保存2天内的
        self.cycleDay_7.load_from_dict(self.data.clcleDay7Bytes)  # 天周期数据 保存7天内的
        self.cycleWeek.load_from_dict(self.data.cycleWeekBytes)  # 周周期数据
        self.cycleMonth.load_from_dict(self.data.cycleMonthBytes)  # 月周期数据


        self.base.load_from_dict(self.data.base)  # 角色基础信息
        # 初始化背包容器
        self.bag = game.core.item.itemctn.CItemContainer(self.id, "itemCtn", self)
        self.bag.Load(self.data.bagDict)  # 角色背包
        # 初始化商城容器
        self.shop = game.core.shop.shopctn.CShopContainer(self.id, "shopCtn", self)
        self.shop.Load(self.data.shopDict)  # 角色背包
        #import objgraph
        #objgraph.show_backrefs(self.bag, max_depth=10, too_many=10, filename='d:\\bag.dot')
        self.inti_exp()
        self.init_name()
        self.initDefaultRole()
        pass

    def checkPaopaoInit(self):
        AllItem  = self.bag.getAllItem()
        hasBasePaopao = False
        for itemObj in AllItem:
            if itemObj.No() == 35:
                return
        if hasBasePaopao == False:
            itemObj = game.core.item.net.AddItem(self, 35, 1)
            itemObj.useItem(self)
        pass

    # 分配随机名
    def init_name(self):
        if self.base.name:
            self.data.name = self.base.name
            return
        namedata = Game.res_mgr.res_name
        if not self.data.name and namedata:
            max_name_key = max(namedata.keys())
            rank_key = random.randint(1, max_name_key)
            nameObj = namedata.get(rank_key, "")
            name = nameObj.name
            self.data.name = name
            self.base.setName(name)
            self.markDirty()

    def AddKey(self, key, default):
        return self.base.AddKey(key, default)

    def Set(self, key, value):
        return self.base.Set(key, value)

    def Query(self, key, default=None):
        return self.base.Query(key, default)

    def Delete(self, key):
        self.base.Delete(key)

    def save_task(self):
        pass

    @classmethod
    def load_player(cls, pid):
        """ 根据pid加载Player对象 """
        # print "----------------------->>>> load_player:", pid
        data = cls.DATA_CLS.load(Game.store, pid)
        # print "----------------------->>>> data:", data
        if data is None:
            return
        p = cls()
        p.data = data
        p.data.set_owner(p)
        p.load()
        return p

    @classmethod
    def login_player(cls, player, pid):
        """ 玩家登陆 """
        if player is None:
            # print "---------11------------login_player", player
            player = cls()
            player.data = cls.DATA_CLS.load(Game.store, pid)
            # print "login_player player.data ------>:",player.data,player.data.base
            player.data.set_owner(player)
            player.load()
        else:
            player.notify("被顶号了！") # 顶号提示，如果客户端链接还在的话就会收到
            # print "---------------------login_player",player
        return player

    # 检测登陆状态
    # 1 普通登陆
    # 2 重连
    def wait_for_login(self):
        """ 等待前端新建角色,并登陆 """
        import traceback
        traceback.print_stack()
        isRelogin = self.isRelogin
        print "-------isRelogin----",isRelogin
        if isRelogin == 2:
            self.isRelogin = 0
            return 2
        return 1

    def setIsRelogin(self):
        self.isRelogin = 2
        pass

    def login(self):
        """ 登陆 """

        if self.logined:
            return
        self.logined = True
        log.debug('plyaer(%s) login', self.id)
        iTime = current_time()
        self.data.SetLoginTime(iTime)
        self.data.AddLoginNum()
        #保存最近一周的登录情况
        lPlayerDayLoginInfo = self.cycleDay_7.Query("lPlayerDayLoginInfo", [])
        lPlayerDayLoginInfo.append((constant.FLAG_LOGIN,iTime)) #1=登录 2=退出
        #只保留最近50条
        iLen = len(lPlayerDayLoginInfo)
        if iLen > 50:
            lPlayerDayLoginInfo = lPlayerDayLoginInfo[iLen-50:iLen]
        self.cycleDay_7.Set("lPlayerDayLoginInfo", lPlayerDayLoginInfo)
        # 记录日志
        Game.glog.log2File("playerLogin", "%s|%s|%s|%s|%s" % (self.id, self.Name(), self.data.account, iTime, self.data.loginNum))
        #生成重连令牌
        self.relogin_token = str(uuid.uuid1())
        # report.log_RoleLogin_sql(self.id, self.base.code, 1, self.data.loginNum)
        self.afterLogin_timmer = spawn_later(2, self.AfterLogin)
        if self.rpc_room: #
            self.rpc_room.exit(self.getUID())
        self.checkPaopaoInit()



    def relogin(self):
        if self.logined:
            return
        self.logined = True
        self.remove1V1RoomInLogin()
        self.notify("重連成功！")
        print "--------relogin-----rpc_room---??", self.rpc_room
        iTime = current_time()
        self.data.SetLoginTime(iTime)
        if self.rpc_room: # 如何是在房间里面，则切链接
            print "----------1"
            self.reconnect_to_fightserver()
            print "----------2"
            self.rpc_room.reconnect_to_Fight(self.id)

    #
    def setFriendRoomNo(self, roomID):
        self.FriendRoomID = roomID

    def checkFriendRoomToFight(self):
        if self.FriendRoomID:
            self.enter1V1Room(self.FriendRoomID)

    def AfterLogin(self):
        # self.rpc_room = None
        if self.afterLogin_timmer:
            self.afterLogin_timmer.kill(block=False)
            self.afterLogin_timmer = None
        self.broGonggao()
        self.show_OneDayReward()
        self.show_sevenDayReward()
        self.checkFriendRoomToFight()
        self.sendGuild()
        self.send_scrollNotice()

    def broGonggao(self):
        try:
            data = self.getGonggao()
            self.broadcast("getGonggao", data)
        except:
            pass


    def logout(self):
        """ 退出 """
        print "---------------logout"
        if not self.logined:
            return False
        self.logined = False
        iTime = current_time()
        self.data.SetLogoutTime(iTime)
        lPlayerDayLogoutInfo = self.cycleDay_7.Query("lPlayerDayLogoutInfo", [])
        lPlayerDayLogoutInfo.append((constant.FLAG_LOGOUT, iTime))  # 1=登录 2=退出
        # 只保留最近50条
        iLen = len(lPlayerDayLogoutInfo)
        if iLen > 50:
            lPlayerDayLogoutInfo = lPlayerDayLogoutInfo[iLen-50:iLen]
        self.cycleDay_7.Set("lPlayerDayLogoutInfo", lPlayerDayLogoutInfo)
        log.debug('plyaer(%s) logout', self.id)
        loginTime = self.data.loginTime
        useTime = iTime - loginTime
        if not useTime or useTime <= 0:
            useTime = 0
        try:
            # Game.rpc_mail_svr.rc_playerlogout(self.id)
            self.FriendRoomID = 0

            self.loginOut_waitingroom() # 退出等待房间
            self.reflashOnline1V1Room() #刷新在线离线状态
            # self.remove1V1Room() # 如果之前有保存好友对战的房间号，清除
            if self.rpc_room:
                print "------self.rpc_room-------",self.rpc_room
                # self.rpc_room.Test()
                self.rpc_room.exitByTimmer(self.id) # 60秒内不重连回来就当输了
                print "----------rs, data"
                # self.rpc_room = None
            else:
                self.remove_router()
            if self.afterLogin_timmer:
                self.afterLogin_timmer.kill(block=False)
                self.afterLogin_timmer = None
        except:
            log.log_except()
        finally:
            self.set_handler(None)
            self.save(forced=True)
            # self.rpc_room.exit(self.getUID())
            Game.player_mgr.del_player(self)
            # 记录日志
            Game.glog.log2File("playerLogout", "%s|%s|%s|%s|%s|%s|%s|%s" % (self.id, self.Name(), self.data.account, iTime, self.getCoin(), self.Lv(), useTime, self.data.loginNum))
            # report.log_RoleLogout_sql(self.id, self.base.code, 0, self.data.loginNum)
        return True

    def Name(self):
        return self.data.name
        # return self.base.name

    def getIcon(self):
        return self.base.getIcon()

    # 经验
    def getExp(self):
        return self.base.exp

    # 当前经验
    def getCurExp(self):
        return self.base.curexp

    # 等级
    def Lv(self):
        return self.base.lv

    # 金币
    def getCoin(self):
        return self.base.coin

    # 钻石
    def getDiamond(self):
        return self.base.diamond

    def checkisOnline(self):
        return self.logined

    def uninit(self):
        """ 释放 """
        if self.uninited:
            return

        self.unsub(msg_define.MSG_ROLE_LEVEL_UPGRADE, self.event_lv_uprade)


        self.uninited = True
        self.loaded = False
        log.debug('player(%s)uninit', self.id)
        if self.rpc_room:
            self.rpc_room.exit(self.id)
            self.rpc_room = None

        if self._handler:
            self.set_handler(None)

    # 保存微信授权信息
    def rc_saveWXInfo(self, head, name, gender):
        if name:
            self.base.setName(name)
            self.data.name = name
            self.markDirty()
        if head:
            self.base.setIcon(head)
        if gender:
            self.base.setGender(gender)
        self.Set("bSaveWXInfo", 1)
        return {"head":head, "name":name, "gender":gender}

    # 保存代币信息
    def rc_saveCoinInfo(self, mainCoin,subCoin):
        if mainCoin:
            self.base.setMainCoin(mainCoin)
            self.markDirty()
        if subCoin:
            self.base.setSubCoin(subCoin)
            self.markDirty()
        return {"mainCoin":mainCoin, "subCoin":subCoin}

    # 提取主币信息
    def rc_AddMainCoin(self, iAdd):
        import subprocess
        pPro = subprocess.Popen(['sh','/root/contract/maincoin/contract.sh','%s'%self.data.account,'1','%s'%int(iAdd),'%s'%int(time.time()),'1'],stdout=subprocess.PIPE,shell=False,close_fds=True)
        #contractVal = os.system("sh /root/contract/maincoin/contract.sh %s %s %s %s %s"%(self.data.account,1,int(iAdd),int(time.time()),1))
        pPro.wait()
        self.base.setCoin(iAdd)
        self.markDirty()
        Game.glog.log2File("contract", "%s" % (pPro.stdout.readlines()))
        return {"mainCoin":self.base.getCoin()}

    # 提取子币信息
    def rc_AddSubCoin(self, iAdd):
        contractVal = os.system("sh /root/contract/subcoin/contract.sh %s %s %s %s %s"%(self.data.account,1,int(iAdd),int(time.time()),1))
        self.base.setDiamond(iAdd)
        self.markDirty()
        return {"subCoin":self.base.getDiamond()}

    # 获取微信信息
    def G2C_getWXInfo(self):
        bSaveWXInfo = self.Query("bSaveWXInfo", 0)
        if not bSaveWXInfo:
            self.broadcast("G2C_getWXInfo", {})

    # =================== 对内基础业务接口 ====================
    def get_role_base(self):
        return self.base.to_base_dict()

    def inti_exp(self):
        if self.base.exp == 0:
            nextExp = self.getNextLvExp()
            self.base.exp = nextExp
            self.base.markDirty()




    def Upgrade(self, exp):
        exp = int(exp)
        # print "exp...............:", exp
        # self.lv = 0         # 等级
        # self.exp = 0        # 经验
        # self.curexp = 0     # 当前经验
        lv = self.base.lv
        nextExp = self.getNextLvExp()
        curexp = self.base.curexp
        beforeLv = lv
        beforeExp = curexp
        if lv >=30:return
        if curexp < nextExp:
            curexp += exp
        if curexp >= nextExp :
            lv += 1
            nexExp = self.getNextLvExp(lv)
            curexp = curexp - nextExp
            self.base.lv = lv
            self.base.exp = nexExp
            self.base.curexp = curexp
            self.base.markDirty()
            self.safe_pub(msg_define.MSG_ROLE_LEVEL_UPGRADE)
            # Game.rpc_rank_info.updateLvRank(self.data.id, self.data.account, "", self.base.lv, wechatId="")
            self.updateLvRank()
            if curexp >= nexExp:
                self.Upgrade(curexp)
        else:
            self.base.curexp = curexp
            self.base.markDirty()
        # print "-------------------------------------------"
        # print "addExp:", exp
        # print "beforeLv:", beforeLv
        # print "beforeExp:", beforeExp
        # print "afterLv:", self.base.lv
        # print "afterExp:", self.base.curexp
        # print "needExp:", self.base.exp
        # print "-------------------------------------------"
        return lv


    def getNextLvExp(self, lv=0):
        if not lv:
            lv = self.base.lv
        if lv == 0:
            lv = 1
            self.base.lv = lv
            self.base.markDirty()
        curUpGradeObj = Game.res_mgr.res_upgrade.get(lv)
        nextExp = curUpGradeObj.exp
        return nextExp

    def event_lv_uprade(self):
        print "roleUpgrade----------",self.base.lv
        spawn_later(0.5, self.upgradeLater)
        self.updateLvRank()
        pass

    def upgradeLater(self):
        self.notify("恭喜升级到%s级"%self.base.lv)


    # 刷新角色信息
    def reflash_role_data(self):
        data = self.base.to_init_dict()
        self.broadcast("reflashRoleData", data)

    def isFighting(self):
        if self.rpc_room:
            return True
        return False
        pass

    def isFightingTrain(self):
        if not self.isFighting():
            return False
        return self.rpc_room.getIsTrain()

    # =================== 对内基础业务接口 ====================


    # =================== 对外基础业务接口 ====================
    # 远程rpc调用其他模块netcmd接口
    # def rpc_Opera(self, iSub, funcName, *args):
    #     netcmd.netcmd_rpc_Opera(self, iSub, funcName, *args)

    # 增加胜利场数
    def addPVPWinCnt(self):
        fightInfo = self.Query("fightInfo", {})
        winCnt = fightInfo.get("winCnt", 0)
        winCnt += 1
        fightInfo["winCnt"] = winCnt
        self.Set("fightInfo", fightInfo)
        return winCnt

    # 增加总胜场数
    def addPVPTotalCnt(self):
        fightInfo = self.Query("fightInfo", {})
        totalCnt = fightInfo.get("totalCnt", 0)
        totalCnt += 1
        fightInfo["totalCnt"] = totalCnt
        self.Set("fightInfo", fightInfo)

    # 获取pvp胜场数
    def getPVPWinCnt(self):
        fightInfo = self.Query("fightInfo", {})
        winCnt = fightInfo.get("winCnt", 0)
        return winCnt

    # 获取PVP胜率
    def getPVPWinRate(self):
        fightInfo = self.Query("fightInfo", {})
        winCnt = fightInfo.get("winCnt", 0)
        totalCnt = fightInfo.get("totalCnt", 0)
        winRate = (winCnt/(totalCnt*1.0))*100
        return winRate

    # 更新PVP胜场排行榜
    def updatePvpRank(self, isWin=1):
        self.addPVPTotalCnt()
        if isWin:
            pvpWinCount = self.addPVPWinCnt()
        else:
            pvpWinCount = self.getPVPWinCnt()
        winRate = self.getPVPWinRate()
        print "-------update!!!!!!!!!!!!PvpRank-------"
        print isWin, pvpWinCount, winRate
        print "-------update!!!!!!!!!!!!PvpRank-------"
    # pvpWinCount = self.Query("PvpWinCount", 0)
        # pvpWinCount = pvpWinCount + 1
        # self.Set("PvpWinCount", pvpWinCount)
        Game.rpc_rank_info.updatePvpRank(self.data.id, self.data.name, self.getIcon(), pvpWinCount, winRate)
        if isWin:
            sStr = "恭喜%s在PVP对战中取得胜利！"%self.Name()
            self.rf_scrollNotice(sStr)


    def updateLvRank(self):
        Game.rpc_rank_info.updateLvRank(self.data.id, self.data.name, self.getIcon(), self.base.lv)

    def updateGuankaRank(self, key_iNo):
        Game.rpc_rank_info.updateGuankaRank(self.data.id, self.data.name, self.getIcon(), key_iNo)


    # 退出时候调用，离开匹配房间
    def loginOut_waitingroom(self):
        game.core.NewWaitRoom.gCNewWaitRoomMng.playerLeaveRoom(self.id)

    # 添加战斗服链接
    def router_to_fightserver(self, addr, port):
        sAddr = "%s:%s"%(addr,port)
        self.Set("FightRoomAddr", sAddr)
        self.getHandler().add_router(1, sAddr)

    def reconnect_to_fightserver(self):
        PPRoomID = self.Query("PPRoomID",0)
        if not PPRoomID:
            return

        room_mgr = self.checkhasroom(PPRoomID)
        playerData = self.pack_to_fight_wait()
        if room_mgr:
            room_mgr.setHandlerReconnect(PPRoomID,playerData)

        FightRoomAddr = self.Query("FightRoomAddr")
        print "--reconnect_to_fightserver--", FightRoomAddr
        if FightRoomAddr:
            self.getHandler().add_router(1, FightRoomAddr)

    # 移除战斗服链接
    def remove_router(self, addr="", port=""):
        print "--------remove_router----!!!!!!!!!!!!!!!!-"
        sAddr = ""
        if not addr or not port:
            sAddr = self.Query("FightRoomAddr")
        else:
            sAddr = "%s:%s"%(addr,port)
        if sAddr:
            try:
                self.getHandler().remove_router(1)
            except:
                pass
        self.Delete("FightRoomAddr")
        self.Delete("PPRoomID")

    # 打包数据到战斗服
    def pack_to_fight_wait(self):
        data = {}
        data["playerId"] = self.id
        data["gwid"] = self.getHandler().rpc.pid
        return data

    # 强制离开房间调用
    def outToFight(self):
        self.remove_router()
        self.loginOut_waitingroom()  # 退出等待房间
        try:
            if self.rpc_room:
                # print "------self.rpc_room-------", self.rpc_room
                # self.rpc_room.Test()
                rs, data = self.rpc_room.exit(self.id)
                # print "----------rs, data", rs, data
                self.rpc_room = None
                return rs, data
        except:
            pass
        return 1,{}

    # 打包数据到战斗服
    def pack_to_fight(self):
        fightMap = self.Query("FightMap", {})
        select1V1Map = self.Query("select1V1Map", {})
        base_fight = self.base.to_base_fight()
        fight_property = self.getRoleFightProperty(APP_MODE_PVP)
        data = {}
        data["fightMap"] = fightMap
        data["select1V1Map"] = select1V1Map
        data["PPSkin"] = self.getPPSkinID()
        data["PPEffectID"] = self.getPPEffectID()
        data["fightClass"] = self.getFightClass()
        data.update(base_fight)
        data.update(fight_property)
        # print "|||||||||||||||--------->>>>>>>>>>>>>>>>>",data
        return data

    # 打包数据到战斗服
    def pack_to_fight_GuanKa(self):
        mapInfo = getattr(self, "mapInfo",{})
        isTrain = getattr(self, "isTrain",0)
        layerconf = mapInfo.get("layerconf",[])
        bgconf = mapInfo.get("bgconf",[])
        barrierNo = mapInfo.get("barrierNo", 1)
        fightMap = {
            'layerconf': layerconf,
            'bgconf': bgconf
        }
        base_fight = self.base.to_base_fight()
        fight_property = self.getRoleFightProperty(APP_MODE_PVE_GUANKA)
        data = {}
        data["fightMap"] = fightMap
        data["isTrain"] = isTrain
        data["barrierNo"] = barrierNo
        data["PPSkin"] = self.getPPSkinID()
        data["PPEffectID"] = self.getPPEffectID()
        data["fightClass"] = self.getFightClass()
        data.update(base_fight)
        data.update(fight_property)
        return data

    # 添加战斗特效
    # num 数量
    # times 次数
    # cycle 持续周期，0：无限制， 1：一日， 2： 两日， 7：七日
    # dKEYS = {1:"LIFE", 2:"SPEED", 3:"COUNT", 4:"POWER"}
    def addFightEffect(self, effectkey, num, times, cycle, fight_mode):
        info = {
            "effectkey": effectkey,
            "cycle": cycle,
            "num": num,
            "times": times,
            "fight_mode":fight_mode,
        }
        fightEffect = self.Query("fightEffect", {})
        fightEffectDay = self.cycleDay.Query("fightEffectDay", {})
        if cycle == 0: # 无限制
            key = "%s_%s_%s_%s"%(effectkey, num, cycle, fight_mode)
            oldinfo = fightEffect.get(key, {})
            if oldinfo:
                oldtimes = oldinfo.get("times",0)
                info["times"] = info["times"] + oldtimes
            fightEffect[key] = info
            self.Set("fightEffect", fightEffect)
        elif cycle == 1: # 1 日
            key = "%s_%s_%s_%s"%(effectkey, num, cycle, fight_mode)
            oldinfo = fightEffectDay.get(key, {})
            if oldinfo:
                oldtimes = oldinfo.get("times", 0)
                info["times"] = info["times"] + oldtimes
            fightEffectDay[key] = info
            self.cycleDay.Set("fightEffect", fightEffectDay)
        elif cycle == 2: # 2 日
            pass


    # 打包战斗特效到战斗服
    def packFightEffect(self):
        dEffect = {}
        fightEffect = self.Query("fightEffect", {})
        fightEffectDay = self.cycleDay.Query("fightEffectDay", {})
        for key, effectInfo in fightEffect.iteritems():
            effectkey   = effectInfo.get("effectkey", "")
            num         = effectInfo.get("num", 0)
            times       = effectInfo.get("times", 0)
            fight_mode  = effectInfo.get("fight_mode", constant.APP_MODE_PVP)
            if not effectkey:
                continue
            if not times:
                continue
            saveEffectInfo = dEffect.get(effectkey, {})
            if num > saveEffectInfo.get("num", 0):
                dEffect[effectkey] = effectInfo
        for key, effectInfoDay in fightEffectDay.iteritems():
            effectkey   = effectInfoDay.get("effectkey", "")
            num         = effectInfoDay.get("num", 0)
            times       = effectInfoDay.get("times", 0)
            if not effectkey:
                continue
            if not times:
                continue
            saveEffectInfoDay = dEffect.get(effectkey, {})
            if num > saveEffectInfoDay.get("num", 0):
                dEffect[effectkey] = effectInfoDay
        return dEffect # {key1:info1,...}


    # 使用战斗特性（扣除次数）
    def useFightEffect(self, dEffect, mode):
        # PVE其实也是PVP
        if mode == constant.APP_MODE_PVE:
            mode = constant.APP_MODE_PVP
        fightEffect = self.Query("fightEffect", {})
        fightEffectDay = self.cycleDay.Query("fightEffectDay", {})
        for skey, effectInfo in dEffect.iteritems():
            effectkey   = effectInfo.get("effectkey", "")
            num         = effectInfo.get("num", 0)
            times       = effectInfo.get("times", 0)
            cycle       = effectInfo.get("cycle", 0)
            fight_mode  = effectInfo.get("fight_mode", constant.APP_MODE_PVP)
            if mode != fight_mode: # 相同模式下才能被使用
                continue
            if not effectkey:
                continue
            key = "%s_%s_%s_%s"%(effectkey, num, cycle, fight_mode)
            times -= 1 # 扣次数
            effectInfo["times"] = times
            if cycle == 0:
                if times <= 0: # 特性没有可用次数
                    if fightEffect.has_key(key):
                        del fightEffect[key]
                    return
                fightEffect[key] = effectInfo
                self.Set("fightEffect", fightEffect)
            elif cycle == 1:
                if times <= 0:  # 特性没有可用次数
                    if fightEffectDay.has_key(key):
                        del fightEffectDay[key]
                    return
                fightEffectDay[key] = effectInfo
                self.cycleDay.Set("fightEffectDay", fightEffectDay)

    # 战斗结果
    def recoverFightResult(self, dResult):
        pass

    # 增加地图设计或修改次数
    def addDiyMapCnt(self, cnt):
        diyMapCnt = self.Query("diyMapCnt", 0)
        diyMapCnt += cnt
        self.Set("diyMapCnt", diyMapCnt)

    def getDiyMapCnt(self):
        diyMapCnt = self.Query("diyMapCnt", 0)
        return diyMapCnt

    # # 获取排行榜点赞次数
    # def addLikeCnt(self, cnt):
    #     LikeCnt = self.Query("LikeCnt", 0)
    #     LikeCnt += cnt
    #     self.Set("LikeCnt", LikeCnt)
    #
    # def getLikeCnt(self):
    #     LikeCnt = self.Query("LikeCnt", 0)
    #     return LikeCnt


    # 设置泡泡皮肤ID
    def setUseSkin(self, PPskinID):
        self.Set("PPskinID", PPskinID)

    def getPPSkinID(self):
        PPskinID = self.Query("PPskinID", 1)
        return PPskinID

    # 设置泡泡特效ID
    def setPPEffectID(self):
        PPeffectID = self.Query("PPeffectID", 1)
        return PPeffectID

    def getPPEffectID(self):
        PPeffectID = self.Query("PPeffectID", 1)
        return PPeffectID

    # 获取出战角色
    def getFightClass(self):
        fightClass = self.Query("fightClass", 1)
        return fightClass


    # ==========================点赞次数===========================
    # dayLikeCnt
    # 每天点赞次数
    def getLikeCnt(self):
        default = 3
        dayLikeCnt = self.cycleDay.Query("dayLikeCnt", default)
        return dayLikeCnt

    # 点赞
    def doAddLike(self, cnt = 1):
        dayLikeCnt = self.cycleDay.Query("dayLikeCnt", 5)
        if dayLikeCnt <= 0:
            self.notify("今天的点赞次数已用完，快去商城购买吧~")
            return False
        dayLikeCnt -= cnt
        self.cycleDay.Set("dayLikeCnt", dayLikeCnt)
        return True


    # 增加点赞次数
    def addLikeCnt(self, cnt=0):
        dayLikeCnt = self.cycleDay.Query("dayLikeCnt", 0)
        dayLikeCnt += cnt
        self.cycleDay.Set("dayLikeCnt", dayLikeCnt)


    #=============================体力===================================
    # dayLikeCnt
    # 获取体力
    def getTiliCnt(self):
        default = constant.CTili.DEFAULT_TILI
        recoverCD = constant.CTili.RECOVERY_CD
        recSpeed = constant.CTili.REC_SPEED
        now = int(time.time()) # , now+300
        TiliCnt = self.Query("TiliCnt", default)
        TiliRecoveryTime = self.Query("TiliRecoveryTime", 0)
        if TiliRecoveryTime:
            cd = now - TiliRecoveryTime
            recoveryCnt = cd/recoverCD # 恢复次数
            if recoveryCnt > 0:
                if recoveryCnt > 0:
                    leftCD = cd%recoverCD
                    addTili = recSpeed*recoveryCnt
                    TiliRecoveryTime = now+recoverCD - leftCD # 更新下一次刷新体力时间
                    self.Set("TiliRecoveryTime", TiliRecoveryTime)
                    self.addTiliCnt(addTili)
                    TiliCnt = self.Query("TiliCnt", default)
        return TiliCnt

    # 使用体力
    def doUseTili(self, cnt):
        TiliCnt = self.getTiliCnt()
        recoverCD = constant.CTili.RECOVERY_CD
        if TiliCnt < cnt:
            self.notify("亲体力不足哦，休息一下再来玩吧")
            return False
        TiliCnt -= cnt
        now = int(time.time()) # , now+300
        TiliRecoveryTime = self.Query("TiliRecoveryTime", 0)
        if not TiliRecoveryTime or now > TiliRecoveryTime:
            self.Set("TiliRecoveryTime", now+recoverCD)
        self.Set("TiliCnt", TiliCnt)
        return True

    # 增加体力值
    def addTiliCnt(self, cnt, addType=constant.CTili.NORMAL_ADD):
        maxTili = constant.CTili.DEFAULT_TILI
        if addType != constant.CTili.NORMAL_ADD:
            maxTili = constant.CTili.MAX_TILI
        if cnt <= 0:
            return False
        TiliCnt = self.getTiliCnt()
        TiliCnt += cnt
        if TiliCnt > maxTili:
            TiliCnt = maxTili
        self.Set("TiliCnt", TiliCnt)

    # 登陆下发
    # 多条推
    def send_scrollNotice(self):
        l = []
        if game.gm.gmFunc.G_ShowKey == 1:
            l.append("点击【红包】按钮，有机会获得【珍稀角色】和【泡泡皮肤】，快快来领取吧！！")
            l.append("闯关模式，第7~10层即将更新，各位客官敬请期待吧！")
            l.append("点击【红包】按钮，有机会获得【珍稀角色】和【泡泡皮肤】，快快来领取吧！！")
            l.append("购买角色 和 学习技能，可以提高实战中的能力哦！")
            l.append("点击【红包】按钮，有机会获得【珍稀角色】和【泡泡皮肤】，快快来领取吧！！")
        else:
            l.append("点击【红包】按钮，有机会获得【珍稀角色】和【泡泡皮肤】，快快来领取吧！！")
            l.append("点击【红包】按钮，有机会获得【珍稀角色】和【泡泡皮肤】，快快来领取吧！！")
            l.append("关注微信公众号【天曜工作室】，获取最新更新动态吧！")
            l.append("闯关模式，第7~10层即将更新，各位客官敬请期待吧！")
            # l.append("春节期间，每天都可以免费抢红包，快来抢福利把~")
            l.append("购买角色 和 学习技能，可以提高实战中的能力哦！")
            l.append("关注微信公众号【天曜工作室】，获取最新更新动态吧！")
            l.append("喜迎新春，新春开服，福利多多，大家快来体验吧~")
        dData = {"lInfo":l}
        self.broadcast("scrollNotice", dData)

    # 刷滚动条
    # 玩家打完关卡
    # 玩家PVP打赢
    # 系统gm
    # 单条推
    def rf_scrollNotice(self, sStr):
        # self.broadcast("rf_scrollNotice", sStr)
        dStr = {"sInfo":sStr}
        Game.player_mgr.broadcast("rf_scrollNotice", dStr)

    def rf_sendPlayer(self,rid):
        return Game.player_mgr.broadcast("contract", {"method":"transfer","to":"0xcc1d96caa5498d533bd93417202b281dec69859b","num":2},keys=[rid])







from game.mgr.xiyou.xiyouroom import SubXiYouRoomMgr, get_xiyou_room_proxy
# from game.gm import report
import config
import testcontainer
import game.core.WaitRoom
import game.mgr.player
from game.mgr.paopao.paopaoroom import SubPaopaoRoomMgr, get_paopao_room_proxy
import game.core.NewWaitRoom
import game.core.item.itemctn
import game.core.shop.shopctn
import game.gm.gmFunc


