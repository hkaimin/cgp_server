#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import random
from gevent import sleep
from corelib import spawn, log, spawn_later
from game.define import errcode,msg_define
from game import Game
from game.common import utility
import config
from corelib.frame import Game
import weakref
from game.define.constant import *


PAOPAO_EXIST_TIME = 0

PAOPAO_MAX_TOUCHTIME = 8 # 泡泡最大碰撞次数


STATE_MATCH = 0     #匹配
STATE_READY = 1     #准备
STATE_START = 2     #开始
STATE_FIGHTING = 3  #比赛中

MINIGAME_SWITCH          = 0    # 小游戏开关
MINIGAME_STATE_UNSTART   = 0    # 小游戏未开始
MINIGAME_STATE_START     = 1    # 小游戏开始
MINIGAME_STATE_END       = 2    # 小游戏结束

class PaopaoInst(object):
    """ 房间类 """
    def __init__(self, mgr, rid, mode=1, max=2, isNoLoopCheck=False):
        self.id = rid #房间id
        # self.roomType = mode #房间类型（1:PVP,）
        # self.mgr = mgr
        self.mgr = weakref.proxy(mgr)
        self.name = "" #名称
        self.fight_mode = mode
        self.map_mode = 2
        self.max = max #最大人数
        self.state = 0 # 0:匹配，1，准备, 2:已开始
        # self.isGoReady = False
        self._st = 0 #当前局开始时间
        self.players = {} #房间玩家列表 id：roomPlayer
        self.lplayers= [] # 匹配队列
        self.readys = {} #EC_VALUE
        self.Map = Game.res_mgr.dPvpMapData
        self.isOver = False
        self.task_timmer = None # 任务计时器
        self.canJoin = True
        self.mapObj = None # 地图对象
        self.dPaoPao = {}
        self.iPaopaoTranceNo = 0
        self._loop_task = None
        self._loop_check = None
        self.paopaoMiniGame = None
        self.paopaoMiniGameState = 0
        self.isFinish = False
        self.isFriend1V1 = False
        self.waitForReconnect = []
        self.putBoom = {} # 投放炸弹数量
        self.fightBrick = {} # 炸掉砖块数量
        self.is1V1 = 0
        self.roomerID = 0
        self.lastPosTime = 0
        self.dProcessor = {}
        self.isTrain = 0
        self.startTime = 0
        # if not isNoLoopCheck:
        # self._loop_check = spawn(self.check)
        # Game.sub(msg_define.MSG_ROLE_LEVEL_UPGRADE, self.event_lv_uprade)

    def getIsTrain(self):
        return self.isTrain

    def setProcessor(self, playerID, processor):
        # print dir(processor)
        print "------------!!!!!!!!!!!---->><><><><><> ",playerID, processor
        processor = weakref.proxy(processor)
        self.dProcessor[playerID] = processor



    def setloopCheck(self):
        self._loop_check = spawn(self.check)

    def kill_loop_check(self):
        if self._loop_check:
            self._loop_check.kill(block=False)
        pass

    def check(self):
        if self.fight_mode == APP_MODE_PVE:
            return
        while 1:
            sleep(60)
            if len(self.players) == 0:
                self.end()

    def Test(self):
        print "Test ========================== 1:"
        return 1, {}

    # 广播
    def broadcast(self, fname, data, exclude=()):
        for playerID, processor in self.dProcessor.iteritems():
            # print playerID, processor
            # print fname, data
            if playerID in exclude:
                continue
            try:
                if not processor:
                    continue
                spawn(processor.call, fname, data, noresult=True)
            except:
                pass

    def broadcast2(self, fname, data, exclude=()):
        """ 广播 """
        from game.mgr.player import get_rpc_player
        lplayer = self.players.keys()
        # if fname in ["syncPosBroadcase"]:
        #     Game.rpc_player_mgr.broadcast(fname, data, [] ,lplayer, _no_result=True)
        #     return
        for pid in lplayer:
            if pid in exclude:
                continue
            if not self.players.get(pid):
                continue
            # data1 = self.packRoomPlayer(player)
            # data["roleInfo"] = data1
            rpc_player = get_rpc_player(pid)
            rpc_player.broadcast(fname, data, _no_result=True)

    def G2CSendPacket(self, fname, data, rid):
        print "G2CSendPacket>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>???", fname, data, rid
        from game.mgr.player import get_rpc_player
        if not self.players.get(rid):
            return
        rpc_player = get_rpc_player(rid)
        if rpc_player:
            rpc_player.broadcast(fname, data, _no_result=True)

    def getPaopaoTranceNo(self):
        self.iPaopaoTranceNo += 1
        return self.iPaopaoTranceNo


    # 房间是否满员
    def IsFull(self):
        if len(self.players) >= self.max and self.canJoin:
            return True
        if self.state > 0:
            return True
        return False
    # 是否空房间
    def InEmpty(self):
        if len(self.players) == 0:
            return True
        return False

    def setIs1V1(self):
        self.isFriend1V1 = True

    def getIs1V1(self):
        return self.isFriend1V1

    def canJoin(self):
        if self.fight_mode == APP_MODE_PVE:
            if len(self.players) >= 1:
                return False
        return True

    # 获取房间详细信息
    # def get_info(self):
    #     return dict(rid=self.id, name=self.name, money=self.money, count=len(self.players),
    #                 max=self.max, isEncrypted=self.isEncrypted)


    #=========================匹配等待=======================

    def  enter_wait(self, pid, name, icon, dAttr, dEffect={}, is1V1=0):
        # self.players[pid]
        print "-----------pid",pid,self.id
        self.is1V1 = is1V1
        if not self.roomerID:
            self.roomerID = pid
        if not self.players.has_key(pid):
            player = game.core.PaoPaoPVP.paopaoPlayer.PaopaoRoomPlayer(self, pid, name, icon, dAttr, dEffect)
            self.players[pid] = player
            player.setPlayerSide(len(self.players))

        # if len(self.players) == 1:
        #     self.check_pve()
        if len(self.players) >=2:
            print "match success!!!", self.players.keys()
            self.state = 1
            self.MatchSuccessPVP()
            self.syncWaitingInfo()
            return 1, {}
        else:
            self.syncWaitingInfo()
            return 1, {}

    def check_pve(self):
        if len(self.players) > 1:
            return
        if self.task_timmer:
            self.task_timmer.kill(block=False)
            self.task_timmer = None
        self.task_timmer = spawn_later(10, self.MatchSuccessPVE)

    def MatchSuccessPVE(self):
        if self.state > 0:
            return
        self.state = 1
        self.fight_mode = APP_MODE_PVE
        print "match success PVE!!!"
        pass

    def MatchSuccessPVP(self):
        self.start()
        pass


    # 同步匹配情况/刷新游戏状态
    def syncWaitingInfo(self):
        data = {}
        data['lenPlayer'] = len(self.players)
        data["player"]={}
        for pid, player in self.players.iteritems():
            data["player"][pid] = player.packRoleBase()
        data["state"] = self.state # 0：正在等待， 1：匹配成功，2：开始比赛，3：比赛中
        data["paopaoMiniGameState"] = self.paopaoMiniGameState # 0:小游戏未开始, 1:小游戏开始, 2:小游戏结束
        spawn(self.broadcast, 'WaitingInfo', data)


    #========================================业务================================
    def start(self):
        # 下发地图信息，比赛信息等
        if self.is1V1:
            self.set1V1PlayerMap(self.roomerID)
        else:
            self.randomMap() # 随机地图
        self.syncMapData()
        self.state = 2
        # self.dPaoPao[]
        if MINIGAME_SWITCH:
            self.startMiniGame()

        self.syncWaitingInfo()
        for pid, player in self.players.iteritems():
            self.dPaoPao[pid] = {}
            # self.set1V1PlayerMap(pid)
        self.state = 3 # 切换成比赛中状态
        pass


    # 一开始，设置不能移动
    def setStopMove(self):
        data = {}
        spawn(self.broadcast, 'stopMove', data)
        pass

    # 可以移动
    def setStartMove(self):
        date = {}
        spawn(self.broadcast, 'startMove', date)


    # 播放MiniReadyGo
    def showMiniReadyGo(self):
        date = {}
        spawn(self.broadcast, 'showMini321', date)

    # 播放ReadyGo
    def showReadyGo(self):
        date = {}
        spawn(self.broadcast, 'show321', date)

    # 开始抢地图小游戏
    def startMiniGame(self):
        if not self.paopaoMiniGame:
            self.paopaoMiniGame = game.core.PaoPaoPVP.paopaoMiniGame.MiniGame()
            self.paopaoMiniGame.setInst(self)
            self.paopaoMiniGameState = MINIGAME_STATE_START


    # 普通点击
    def normalClick(self, uid):
        if self.paopaoMiniGame:
            self.paopaoMiniGame.normalClick(uid)

    # 特殊点击
    def spClick(self, uid):
        if self.paopaoMiniGame:
            self.paopaoMiniGame.spClick(uid)

    # 小游戏弃权，认输，直接用对手的地图
    def miniGameGiveup(self, uid):
        if self.paopaoMiniGame:
            self.paopaoMiniGame.miniGameGiveup(uid)

    # 小游戏胜利，重新初始化地图，初始化新加成
    def minigameWin(self, uid):
        self.paopaoMiniGameState = MINIGAME_STATE_END
        playerObj = self.players.get(uid)
        bgConf = playerObj.getMyMapBgconf()
        layerConf = playerObj.getMyMapLayerConf()
        if bgConf and layerConf:
            self.mapObj = PaopaoMap(0, bgConf, layerConf)
            self.syncMapData()
            self.showReadyGo()
        pass

    #
    def set1V1PlayerMap(self, uid):
        playerObj = self.players.get(uid)
        bgConf = playerObj.getMyMapBgconf()
        layerConf = playerObj.getMyMapLayerConf()
        if bgConf and layerConf:
            self.mapObj = PaopaoMap(0, bgConf, layerConf)
            # self.syncMapData()
        else:
            self.randomMap()
            # self.showReadyGo()
        pass
    # def startPVE(self):
    #     # 下发地图信息，比赛信息等
    #     self.randomMap()
    #     self.syncMapData()
    #     self.state = 2
    #     self.syncWaitingInfo()
    #     pass

    def randomMap(self):
        mapKeys = self.Map.keys()
        # key = random.choice(mapKeys)
        # 这里可以随机地图Key列表
        key = random.choice(mapKeys)
        print "----------start", self
        self.mapObj = PaopaoMap(key)

    def syncMapData(self):
        data = {}
        data["bgConf"] = self.mapObj.getBGConf() # 地板地图
        data["layerConf"] = self.mapObj.getlayerconf() # 障碍物地图
        data["p1Idx"] = self.mapObj.get_p1_idx() # 玩家1 idx
        data["p2Idx"] = self.mapObj.get_p2_idx() # 玩家2 idx
        data["fight_mode"] = self.fight_mode # 游戏模式
        data["map_mode"] = 2
        # data["mapType"] = self.mapObj.mapType
        data["player"] = {}
        for pid, player in self.players.iteritems():
            data["player"][pid] = {}
            data["player"][pid] = player.packRoleBase()
        # self.broadcast("syncMapData", data)
        spawn(self.broadcast, 'syncMapData', data)

    # 同步位置 speed  速率
    def syncPos(self, rid, x, y, direction, speed=1, idx=0, playerID=0):
        if playerID != 0 and playerID != rid and playerID in self.players.keys():
            rid = playerID
        data = {}
        data["rid"] = int(rid)
        data["x"] = int(x)
        data["y"] = int(y)
        data["direction"] = int(direction)
        data["speed"] = int(speed)
        data["idx"] = int(idx)
        # player = self.players.get(rid)z
        # if int(speed) != player.speed:
        #     return 0, {}  # 使用外挂
        spawn(self.broadcast, 'syncPosBroadcase', data)
        return 1, {}

    # 同步谁放了炸弹，坐标要发当前格子的坐标，这样XY就不会有误差
    def syncPut(self, rid, x, y, idx, playerID=0):
        # 先判断是否有可释放的泡泡数量
        # print "======syncPut==playerID=>>> 1", playerID
        if playerID != 0 and playerID != rid and playerID in self.players.keys():
            rid = playerID
        # print "======syncPut==playerID=>>> 2", playerID
        # if playerID == 0:
        #     rid = playerID
        player = self.players.get(rid)
        if not player.canPutPaoPao():
            return 1, {"err":errcode.EC_NOT_PAOPAO_CAN_PUT, "rid":rid}
        player.putPaoPao()
        paopaoID = self.getPaopaoTranceNo()
        dPaopao = self.dPaoPao.get(rid, {})
        data = {}
        if not dPaopao.has_key(paopaoID):
            st = int(time.time())
            data = {
                "x" : x,
                "y" : y,
                "start":st,
                "end":st+PAOPAO_EXIST_TIME,
                "rid":rid,
                "paopaoID":paopaoID,
                "idx":idx,
                "touchTimes":0 # 触碰到的次数
            }
            dPaopao[paopaoID] = data
            spawn(self.broadcast, 'syncPut', data)
            self.dPaoPao[rid] = dPaopao

            self.add_putBoom(rid)
            return 1, {}
        return 1, {"err":errcode.EC_NOT_PAOPAO_CAN_PUT, "rid":rid}

    # 同步炸弹爆炸, 坐标要发当前格子的坐标，
    # status = -1 # 非法泡泡
    # status = 0 # 时间还没到
    # status = 1 # 泡泡有效 没有打到人
    # status = 2 # 泡泡有效 有打到人
    # , killplayerX = -1, killplayerY = -1
    def syncBoomPlayer(self, rid, paopaoID, x, y, idx, killrid=0, killidx=-1, playerID=0):
        # print "==================syncBoomPlayer",rid, paopaoID, x, y, idx, killrid
        # 发送x, y是为了验证炸弹的有效性
        if playerID != 0 and playerID != rid and playerID in self.players.keys():
            rid = playerID
        dPaopao = self.dPaoPao.get(rid,{})
        if dPaopao.has_key(paopaoID):
            dPaopao = dPaopao.get(paopaoID)
            if dPaopao['touchTimes'] >= PAOPAO_MAX_TOUCHTIME:
                del self.dPaoPao[rid]
                return
            paopaoX = dPaopao["x"]
            paopaoY = dPaopao["y"]
            paopaoOwner = dPaopao["rid"]
            if dPaopao["end"] > int(time.time()):
                # 时间还没到
                data = {}
                data["status"] = 0 #
                data['sytime'] = dPaopao["end"] - int(time.time())
                spawn(self.broadcast, 'syncBoom', data)
                return
            # if paopaoY != y or paopaoX != x or paopaoOwner != rid or (killrid and not self.players.has_key(killrid)):
            if not self.isInValueRange(x, paopaoX) and not self.isInValueRange(y, paopaoY) or paopaoOwner != rid or (killrid and not self.players.has_key(killrid))\
                    and not playerID:
                # del self.dPaoPao[rid] # 清除泡泡
                dPaopao['touchTimes'] += 1
                data = {}
                data["status"] = -1 #
                spawn(self.broadcast, 'syncBoom', data)
                return
            # if killrid > 0:
            #     if self.mapObj.MapInfo.get(killidx):
            #         killidxInfo = self.mapObj.MapInfo.get(killidx)
            #         killplayerX = killidxInfo['x']
            #         killplayerY = killidxInfo['y']
            #         zoom = 50 # 误差范围
            #         # if (killplayerX >0 and killplayerY>0) and ((killplayerX - zoom) <= paopaoX <= (killplayerX + zoom)) and \
            #         #         ((killplayerY - zoom) <= paopaoY <= (killplayerY + zoom)):
            #         if (killplayerX > 0 and killplayerY > 0) and not self.isInValueRange(killplayerX, paopaoX, 50) and \
            #                 not self.isInValueRange(killplayerY, paopaoY, 50):
            #             # 被击杀者的X,Y killplayerX, killplayerY, 也是为了验证炸弹的有效性，被击杀玩家必须X或者Y，任意一个轴与炸弹相等，才能被杀死
            #             # del self.dPaoPao[rid] # 清除泡泡
            #             dPaopao['touchTimes'] += 1
            #             data = {}
            #             data["status"] = -1  #
            #             spawn(self.broadcast, 'syncBoom', data)
            #             return
                # else:
                #     dPaopao['touchTimes'] += 1
                #     data = {}
                #     data["status"] = -1  #
                #     spawn(self.broadcast, 'syncBoom', data)
                #     return
            if int(time.time()) >= dPaopao["end"]: # 有效
                # del self.dPaoPao[rid]  # 清除泡泡
                dPaopao['touchTimes'] += 1
                if self.players.get(killrid):
                    data = {}
                    data["status"] = 2  #
                    data["killrid"] = killrid
                    spawn(self.broadcast, 'syncBoom', data)
                    if rid != killrid:
                        player = self.players.get(rid)
                        player.addKill()
                    self.kill_player(killrid)
                else:
                    data = {}
                    data["status"] = 1  #
                    spawn(self.broadcast, 'syncBoom', data)
                pass

    # 同步炸弹爆炸, 坐标要发当前格子的坐标，
    # status = -1 # 非法泡泡
    # status = 0 # 时间还没到
    # status = 1 # 泡泡有效 没有打到人
    # status = 2 # 泡泡有效 有打到人
    def syncBoomZhuan(self, rid, paopaoID, x, y, idx,  breakidx=-1, playerID=0):
        print "syncBoomZhuan：",rid, paopaoID, x, y, idx, breakidx
        # 发送x, y是为了验证炸弹的有效性
        if playerID != 0 and playerID != rid and playerID in self.players.keys():
            rid = playerID
        dPaopao = self.dPaoPao.get(rid, {})
        if dPaopao.has_key(paopaoID):
            # print "dPaopao:",dPaopao, "paopaoID:",paopaoID
            dPaopao = dPaopao.get(paopaoID)
            if dPaopao['touchTimes'] >= PAOPAO_MAX_TOUCHTIME:
                del self.dPaoPao[rid]
                return
            # paopaoX = dPaopao["x"]
            # paopaoY = dPaopao["y"]
            # paopaoOwner = dPaopao["rid"]
            # if dPaopao["end"] > int(time.time()):
            #     print 11111111111111111111
            #     # 时间还没到
            #     data = {}
            #     data["status"] = 0  #
            #     data['sytime'] = dPaopao["end"] - int(time.time())
            #     spawn(self.broadcast, 'syncBoom', data)
            #     return
            #
            # # if paopaoY != y or paopaoX != x or paopaoOwner != rid or (
            # #     killrid and not self.players.has_key(killrid)):
            # #     print 11111111111111111112, "====y:", paopaoY, y, "====x:",paopaoX,x, "====paopaoOwner", paopaoOwner, rid
            # #     # del self.dPaoPao[rid]  # 清除泡泡
            # #     dPaopao['touchTimes'] += 1
            # #     data = {}
            # #     data["status"] = -1  #
            # #     spawn(self.broadcast, 'syncBoom', data)
            # #     return
            # # if not (paopaoX - 10) < x < (paopaoX + 10) and not (paopaoY - 10) < y < (paopaoY + 10)
            # if not self.isInValueRange(x, paopaoX) and not self.isInValueRange(y, paopaoY) and not playerID:
            #     print 11111111111111111112, "====y:", paopaoY, y, "====x:", paopaoX, x, "====paopaoOwner", paopaoOwner, rid
            #     # del self.dPaoPao[rid]  # 清除泡泡
            #     dPaopao['touchTimes'] += 1
            #     data = {}
            #     data["status"] = -1  #
            #     spawn(self.broadcast, 'syncBoom', data)
            #     return

            # if int(time.time()) >= dPaopao["end"]:  # 有效
                # del self.dPaoPao[rid]  # 清除泡泡
                # print 11111111111111111113
            dPaopao['touchTimes'] += 1
            if breakidx >= 0 and self.mapObj.hasMapidx(breakidx):
                dEffect = self.mapObj.breakMap(breakidx)  # 砖块 有几率爆道具
                # print "----------------lllll dEffect", dEffect, breakidx
                if dEffect:
                    if dEffect['err'] == errcode.EC_OK:
                        data = {}
                        data["layerConf"] = self.mapObj.getlayerconf()  # 障碍物地图
                        data['idx'] = idx # 泡泡idx
                        data['breakidx'] = breakidx # 被消除砖块IDX
                        data['effect'] = dEffect
                        spawn(self.broadcast, 'syncBoomZhuan', data)
                        self.add_FightBrick(rid)
                        return
                pass

    # 是否在取值范围内
    def isInValueRange(self, value, RangeValue, i=50):
        if (RangeValue-i) <= value <= (RangeValue+i):
            return True
        else:
            return False

    def guangkaFinish(self, rid, idx):
        pass

    # 捡到道具
    # 速度 Type : 1
    # 泡泡数量道具 Type : 2
    # 泡泡威力道具 Type : 3
    # 生命 Type : 4
    # 问号红包 Type : 5
    # 屎 : 6
    def pickItem(self, rid, itype, idx, playerID=0):
        print "-----pickItem---", rid, itype, idx, playerID
        dEffectItem = self.mapObj.dEffectItem  # 当前可捡取的{道具类型：num}
        if playerID != 0 and playerID != rid and playerID in self.players.keys():
            rid = playerID
        player = self.players.get(rid)
        if not player: return
        if dEffectItem.get(itype):
            res = self.mapObj.eatEffectItem(idx, itype) # 吃道具
            if not res:
                self.syncMapData()
                return
            # 成功吃掉道具
            if itype == CFightToolType.SPEED:
                player.addSpeed()
            elif itype == CFightToolType.NUM:
                player.addPaopaocount()
            elif itype == CFightToolType.POWER:
                player.addPower()
            elif itype == CFightToolType.LIFE:
                player.addLife()
            elif itype == CFightToolType.REDBAO:
                ltype = [1,2,3,4]
            elif itype == CFightToolType.DOOR:
                if self.fight_mode == APP_MODE_PVE_GUANKA:
                    self.guangkaFinish(rid, idx)
            # self.syncMapData()

            data = {}
            data['type']= itype # 需要消除的类型
            data['effectType']= itype # 生效的类型
            data['idx']= idx # 原路返回idx
            data['pickRid'] = rid # 谁捡到了
            data["player"] = {}
            for pid, player in self.players.iteritems():
                data["player"][pid] = {}
                data["player"][pid] = player.packRoleBase()
            spawn(self.broadcast, 'syncpickItem', data)

    # 刷新战斗属性
    def reflashProperty(self):
        print 11111111111111111111,"reflashProperty"
        data = {}
        data["player"] = {}
        for pid, player in self.players.iteritems():
            data["player"][pid] = {}
            data["player"][pid] = player.packRoleBase()
        print data
        spawn(self.broadcast, 'syncpickItem', data)


    # 杀人
    def kill_player(self, pid):
        BeAttacker = self.players.get(pid)
        life = BeAttacker.beHurt()
        if life <= 0:
            self.game_over()
        else:
            self.reflashProperty()
        pass


    # 使用技能
    def useSkill(self, pid, skillID):
        skillID = str(skillID)
        targetPlayer = None
        for ppid, player in self.players.iteritems():
            if ppid != pid:
                targetPlayer = player
        if targetPlayer==None:
            return {}
        attacker = self.players.get(pid)
        if not attacker:
            return {}
        if not attacker.getSkillCanUse(skillID):
            spawn(self.broadcast, 'notify', {"tips":"技能CD回复中"}, [targetPlayer.pid])
            return {}
        res = paopaoSkill.dealSkllAttack(attacker, targetPlayer, skillID)
        if not res:
            spawn(self.broadcast, 'notify', {"tips":"请先学习技能"}, [targetPlayer.pid])
            return {}
        dData = {}
        dData["effectPlayer"] = targetPlayer.pid # 生效的角色ID，用在谁身上
        dData["skillID"] = int(skillID) # 技能ID
        spawn(self.broadcast, 'useSkillOK', dData)
        self.reflashProperty()
        return {}


    # 结算
    def game_over(self):
        if self.isFinish:
            return
        from game.mgr.player import get_rpc_player
        for pid, player in self.players.iteritems():
            if not player.isDie(): # 赢了
                player.setWin()
                rpc_player = get_rpc_player(pid)
                print ">>>>>>>>>>game_over>>>>>>>", self.putBoom, self.fightBrick
                print "===========pid", pid
                if rpc_player:
                    rpc_player.updatePvpRank(_no_result=True)
                # data = player.packRoleBase()
                # data['win'] = player.win
                # data['addexp'] = 100
            else: # 输了
                # data = player.packRoleBase()
                # data['win'] = player.win
                # data['addexp'] = 0
                pass
            isWin = player.isWin()
            player.afterResult(isWin=isWin)
        data = {}
        data["player"]={}
        for pid, player in self.players.iteritems():
            data["player"][pid] = player.packRoleResult()
        spawn(self.broadcast, 'gameResult', data)
        self.isFinish = True
        pass

    # 记录投放炸弹数量
    def add_putBoom(self, playerID):
        playerPutBoomNum = self.putBoom.get(playerID, 0)
        playerPutBoomNum += 1
        self.putBoom[playerID] = playerPutBoomNum

    # 记录炸掉砖块数量
    def add_FightBrick(self, playerID):
        playerFightBrick = self.fightBrick.get(playerID, 0)
        playerFightBrick += 1
        self.fightBrick[playerID] = playerFightBrick



    # 重连回到游戏
    def reconnect_to_Fight(self, pid):
        print "------fight_reconnect"
        print "------fight_reconnect"
        print "------fight_reconnect"
        print "------fight_reconnect"
        print "------fight_reconnect"
        self.syncMapData()
        if pid in self.waitForReconnect:
            self.waitForReconnect.remove(pid)
        pass

    # 重连超时
    def exitByTimmer(self, pid):
        spawn_later(120, self.exit, pid = pid, isCallReconnectTimmer = True)
        if pid not in self.waitForReconnect:
            self.waitForReconnect.append(pid) # n 秒内重连，则移除
        pass

    def exit(self, pid, isCallReconnectTimmer=False):
        print "exit", pid, isCallReconnectTimmer
        import traceback
        traceback.print_stack()
        if isCallReconnectTimmer and pid not in self.waitForReconnect:
            return 1, {}
        if isCallReconnectTimmer and pid in self.waitForReconnect:
            spawn(self.broadcast, 'notify', {"tips":"对方已掉线！"})

        """ 玩家退出 """
        # import traceback
        # traceback.print_stack()
        print "player ========================== 1:",pid,self.id,self
        if not self.players.has_key(pid):
            return 0, errcode.EC_NO_ROOM
        # for rid, player in self.players.iteritems():
        #     player.ExitRoom()

        from game.mgr.player import get_rpc_player
        rplayer = self.players.get(pid)
        rpc_player = get_rpc_player(pid)
        if rpc_player:
            rpc_player.ppGameOver(rplayer.dPlayerEffect, rplayer.packBackToMain(), self.fight_mode,_no_result=True)

        rplayer.ExitRoom()
        print "player ========================== :2", pid,rplayer

        # try:
        if rplayer:
            self.kill_player(pid)
            del self.players[pid]
            # del self.dProcessor[pid]
        data = dict(pid=pid, name=rplayer.name, mode=self.fight_mode)
        spawn(self.broadcast, 'exitMsg', data)
        # except:
        #     if rplayer:
        #         self.kill_player(pid)
        #         del self.players[pid]
        #     data = dict(pid=pid, name=rplayer.name, mode=self.fight_mode)
        #     spawn(self.broadcast, 'exitMsg', data)
        endPeopleCount = 0
        if self.fight_mode == APP_MODE_PVE:
            endPeopleCount = 1
        if len(self.players) <= endPeopleCount:
            self.end()
        return 1, {}

    def end(self):
        if self._loop_check:
            self._loop_check.kill(block=False)
            self._loop_check = None

        if self._loop_task:
            self._loop_task.kill(block=False)
            self._loop_task = None

        if self.task_timmer:
            self.task_timmer.kill(block=False)
            self.task_timmer = None
        self.isOver = True
        self.mgr.del_room(self)

    # ================== Alg =====================
    # 算法相关的逻辑调整

    def kill_player_by_monster(self, attacker_pid, beattacker_pid):
        pass



import random
import types
from datetime import datetime
from game.core.PaoPaoPVP.paopaoMap import *
import game.core.PaoPaoPVP.paopaoPlayer
import game.core.PaoPaoPVP.paopaoMiniGame
from game.define.constant import *
import paopaoSkill