#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from gevent import sleep

from corelib import log
from game.define import errcode, msg_define, constant, store_define
from game import Game

from game.gm import gmFunc
import time
from game.common.gateway import AbsExport
from game.protocal.xiyouProtocal import xiyouProtocal
from game.protocal.paopaoProtocal import paopaoProtocal
from game.protocal.mapProtocal import mapProtocal
from game.protocal.BasePlayerRpcHander import BasePlayerRpcHander


def _wrap_nolock(func):
    func._nolock_ = 1
    return func


class PlayerMgrrpcHandler(AbsExport):
    """ 管理器的rpc处理类 """
    def __init__(self):
        self.logined = False

    def set_rpc(self, process):
        self.rpc = process
        if process:
            self.rpc.set_export(self)

    def on_close(self, process):
        """ 断线处理 """
        self.set_rpc(None)

    def stop(self):
        if self.rpc is not None:
            self.rpc.close()
            self.set_rpc(None)

    def rc_register(self, account, password, pcode='', verified_code=''):
        """注册账号"""
        ok,data = Game.rpc_player_mgr.rc_register(account, password, pcode, verified_code)
        if not ok:
            return 0, data
        return 1, data

    def rc_login(self, account, password):
        """ 登录接口 """
        import traceback
        ok, data = Game.rpc_player_mgr.rc_login(self.rpc, account, password)
        if not ok:
            return 0, data
        self.logined = True
        return 1, data

    def rc_loginWX(self, openID, sHead, sName, iGender):
        """ 微信登录 """
        ok, data = Game.rpc_player_mgr.rc_wxlogin(self.rpc, openID, sHead, sName, iGender, password=1)
        if not ok:
            return 0, data
        self.logined = True
        return 1, data

    def rc_loginWXbyLink(self,openID, sHead, sName, iGender, fightRoom, pid, token):
        """点击微信分享链接"""
        ok, data = Game.rpc_player_mgr.rc_loginWXbyLink(self.rpc, openID, sHead, sName, iGender, fightRoom, pid, token, password=1)
        if not ok:
            return 0, data
        self.logined = True
        return 1, data



    def rc_relogin(self, pid, token):
        """ 玩家重连 """
        print "----------------"
        ok, data = Game.rpc_player_mgr.rc_relogin(self.rpc, pid, token)
        if not ok:
            return 0, data
        self.logined = True
        return 1, data

    def rc_tokenLogin(self, account, token):
        """令牌登陆"""
        ok, data = Game.rpc_player_mgr.rc_tokenLogin(self.rpc, account, token)
        if not ok:
            return 0, data
        self.logined = True
        return 1, data



class PlayerRpcHandler(BasePlayerRpcHander, xiyouProtocal, paopaoProtocal, mapProtocal):
    """ 玩家rpc处理类 """
    DEBUG = 1

    def __init__(self):
        BasePlayerRpcHander.__init__(self)
        self.active = True

    def rc_heartbeat(self):
        return 1, None

    def rc_gmFunc(self, gmCmd):
        """ 执行gm命令 """
        cmd = gmCmd
        print "============gmCmd", gmCmd
        # return 1, None
        isGM = self.player.data.IsGm()
        if not isGM:
            return 0, errcode.EC_NOT_GM
        lcmd = cmd.split("|")
        for oneCmd in lcmd:
            oneCmd = oneCmd.strip() #去掉两端的空格
            loneCmd = oneCmd.split(" ") #指令以空格分开
            fname, args = loneCmd[0], loneCmd[1:]
            func = getattr(gmFunc, fname)
            func(self.player, *args)
            # if func:
            #     try:
            #         func(self.player, *args)
            #         Game.glog.log2File("ExecGM", "%s|%s|%s" % (self.pid, oneCmd, lcmd), flag=1)
            #         report.log_ExecGM_sql(self.player, self.pid, oneCmd, lcmd)
            #     except Exception, err:
            #         Game.glog.log2File("ExecGM_Err", "%s|%s|%s|%s"%(self.pid, err.message, oneCmd, lcmd))
            #         # log.log_except("ExecGM_Err %s|%s|%s|%s", self.pid, err.message, oneCmd, lcmd)
            #         print err.message,Exception
            #         return 0, errcode.EC_EXEC_GM_CMD
            # else:
            #     Game.glog.log2File("ExecGM_NotFind", "%s|%s|%s" % (self.pid, oneCmd, lcmd))
            #     # log.log_except("ExecGM_NotFind %s|%s|%s", self.pid, oneCmd, lcmd)
            #     return 0, errcode.EC_NOT_GM_CMD
        return 1, None

    def rc_entergame(self):
        """进入游戏"""
        # print "-0-----------------rc_entergame-",self.player,dir(self.player)
        rs = self.player.entergame(self.player)
        if not rs:
            return 0, errcode.EC_LOGIN_ERR
        return 1, rs

    def rc_setName(self, name):
        """修改昵称"""
        rs = self.player.setName(name)
        return 1, rs

    def rc_setRealName(self, realname):
        """修改真实姓名"""
        rs = self.player.setRealName(realname)
        return 1, rs

    def rc_setPassword(self, oldpassword, newpassword):
        """修改密码"""
        rs = self.player.setPassword(oldpassword, newpassword)
        if not rs:
            return 0, errcode.EC_PASSWORD_ERR
        return 1, rs

    def rc_setWeixin(self, wxId):
        """修改微信号"""
        print "---rc_setWeixin"
        rs = self.player.setWeixin(wxId)
        return 1, rs


    def rc_setIcon(self, icon):
        """修改头像"""
        rs = self.player.setIcon(icon)
        return 1, rs


    # 开始匹配
    def rc_start_match(self):
        """进入游戏"""
        rs = self.player.PaoPaoPvpNet.start_match(self.player)
        if not rs:
            return 0, errcode.EC_MATCH_ERR
        return 1, rs


    # 排行榜主界面
    def rc_openRnakUI(self):
        print "------------openRnakUI---",self.player
        rs = self.player.openRnakUI(self.player)
        return 1, rs

    # 总战绩排行榜
    def rc_getTotalPvpRank(self):
        rs = self.player.rc_getTotalPvpRank(self.player)
        return 1, rs

    # 排行榜前三
    def rc_getPvpRankThree(self):
        rs = self.player.rc_getPvpRankThree(self.player)
        return 1, rs

    # 总等级排行榜
    def rc_getTotalLvRank(self):
        rs = self.player.rc_getTotalLvRank(self.player)
        return 1, rs

    # 好友战绩排行榜
    def rc_getFriendPvpRank(self):
        rs = self.player.rc_getFriendPvpRank(self.player)
        return 1, rs

    # 好友等级排行榜
    def rc_getFriendLvRank(self):
        rs = self.player.rc_getFriendLvRank(self.player)
        return 1, rs

    # 总关卡排行榜
    def rc_getTotalGuankaRank(self):
        rs = self.player.rc_getTotalGuankaRank(self.player)
        return 1, rs

    # 战斗服测试接口
    def rc_test(self,v):
        print v
        return 1, {"v":v}


    # 打开背包UI
    def rc_openBagUI(self, iType):
        rs = self.player.rc_openBagUI(self.player, iType)
        return 1, rs

   # 打开商城UI
    def rc_openShopUI(self, iType):
        rs = self.player.rc_openShopUI(self.player, iType)
        return 1, rs

   # 购买
    def rc_Buy(self, iNo, iType, num):
        rs = self.player.rc_Buy(self.player, iNo, iType, num)
        return 1, rs

    # 使用道具
    # iNo 道具表的id
    # iItemID 道具内存ID
    # iType 打开界面类型
    def rc_useItem(self, iNo, iItemID, iType):
        rs = self.player.rc_useItem(self.player, iNo, iItemID, iType)
        return 1, rs

    def rc_playerVidio(self, iNo):
        rs = self.player.rc_playerVidio(self.player, iNo)
        return 1, rs

    # 领取每天奖励
    def rc_getOneDayReward(self):
        rs = self.player.rc_getOneDayReward()
        return 1, rs

    # 领取七天奖励
    def rc_getSeventDayReward(self):
        rs = self.player.rc_getSeventDayReward()
        return 1, rs

    # 获取关卡列表
    def rc_C2GOpenWujinUI(self, diffLevel):
        rs = self.player.rc_C2GOpenWujinUI(diffLevel)
        return 1, rs

    # 进入关卡
    def rc_C2GGotoBarrier(self, barrierNo):
        rs = self.player.rc_C2GGotoBarrier(barrierNo)
        return 1, rs

    # 获取关卡详情
    def rc_getBarrierInfo(self, barrierNo):
        rs = self.player.getBarrierInfo(barrierNo)
        return 1, rs

    # 重新挑战
    def rc_againGuanka(self):
        rs = self.player.rc_againGuanka()
        return 1, rs

    # 下一关
    def rc_nextGuanka(self):
        rs = self.player.rc_nextGuanka()
        return 1, rs


    # 进入训练关卡
    def rc_C2GEnterTrain(self):
        rs = self.player.rc_C2GEnterTrain()
        return 1, rs

    # 获取角色详情
    def rc_getRoleDetail(self):
        rs = self.player.getRoleDetail()
        return 1, rs
        pass

    def rc_showAllClassList(self):
        rs = self.player.rc_showAllClassList()
        return 1, rs

    def rc_buyClass(self, iClass):
        rs = self.player.rc_buyClass(iClass)
        return 1, rs

    def rc_useClass(self,iClass):
        rs = self.player.rc_useClass(iClass)
        return 1, rs

    # 获取下一个引导
    def rc_getNextGuild(self):
        rs = self.player.getNextGuild()
        return 1, rs

    # 获取当前引导
    def rc_getNowGuild(self):
        rs = self.player.getNowGuild()
        return 1, rs

    # 升级奖励
    def rc_showUpgradeReward(self):
        rs = self.player.showUpgradeReward()
        return 1, rs

    # 获取升级奖励
    def rc_getUpgradeReward(self, iLv):
        rs = self.player.getUpgradeReward(iLv)
        return 1, rs

    # 打开技能界面
    def rc_C2G_Open_MainUI(self):
        rs = self.player.rc_C2G_Open_MainUI()
        return 1, rs

    # 技能升级
    def rc_C2G_Upgrade(self, SkillID):
        rs = self.player.rc_C2G_Upgrade(SkillID)
        return 1, rs

    # 保存微信授权后的信息
    def rc_saveWXInfo(self, head, name, gender):
        rs = self.player.rc_saveWXInfo(head, name, gender)
        return 1, rs

    # 保存代币信息
    def rc_saveCoinInfo(self, mainCoin,subCoin):
        rs = self.player.rc_saveCoinInfo(mainCoin,subCoin)
        return 1, rs

    # 帮助界面
    def rc_getHelp(self, helpID):
        rs = self.player.rc_getHelp(helpID)
        return 1, rs

    # 离开泡泡房间,取消匹配exitPPRoom
    def rc_exitPPRoom(self):
        # err, rs = self.player.rc_enterPPRoom()
        err, rs = self.player.rc_ExitWait(self.player)
        return err, rs

    # 获取随机红包
    def rc_getHongBao(self):
        rs = self.player.getHongBao()
        return 1, rs

    # 观看视频后领取等级奖励
    def rc_getLvRewardVidio(self):
        rs = self.player.getUpgradeRewardAuto()
        return 1, rs

    # 获取公告
    def rc_getGonggao(self):
        rs = self.player.getGonggao()
        return 1, rs

    # 点击播放时上传
    def rc_playVidioBefore(self, iType, iNo, pageType):
        rs = self.player.playVidioBefore(iType, iNo, pageType)
        return 1, rs

    # 视频播放后调用
    def rc_playVidioFinish(self):
        rs = self.player.playVidioFinish()
        return 1, rs

    #主币提取
    def rc_AddMainCoin(self,iAdd,iOpType):
        rs = self.player.rc_AddMainCoin(iAdd,iOpType)
        return 1, rs

    #主币提取
    def rc_AddSubCoin(self,iAdd,iOpType):
        rs = self.player.rc_AddSubCoin(iAdd,iOpType)
        return 1, rs

    #创建nft
    def rc_createNft(self,iTickets):
        rs = self.player.rc_createNft(iTickets)
        return 1, rs

    #获取已有nft
    def rc_getOwnNft(self,lNft):
        rs = self.player.rc_getOwnNft(lNft)
        return 1, rs

    def rc_PBuyNft(self,nftIndex,sAddress):
        rs = self.player.rc_PBuyNft(nftIndex,sAddress)
        return 1, rs

    #刷新exhibition
    def rc_getTotalExhi(self):
        rs = self.player.rc_getTotalExhi()
        return 1, rs

from game.gm import report
