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
import game.core.PaoPaoPVP.paopaoInst
import time
from game.define.constant import *

# ============== 战斗模式
# APP_MODE_PVP = 1
# APP_MODE_PVE = 2
# APP_MODE_PVE_GUANKA = 3

PAOPAO_EXIST_TIME = 0

PAOPAO_MAX_TOUCHTIME = 8 # 泡泡最大碰撞次数

RESULT_IME_TYPE = 1

MONSTER_AI_KEY = 121

# 1，是否对方死了
# 2，通关时间
# 3，炸砖块数量达到N
# 4，放炸弹少于N
# 5，速度道具捡到N个
# 6，泡泡数量道具捡到N个
# 7，泡泡威力道具捡到N个
# 8，增加生命道具捡到N
class CStarType(object):
    IS_WIN = 1
    UES_TIME = 2
    FIGHT_BRICK_CNT = 3
    PUT_BOOM_CNT = 4
    PICK_SPEED = 5
    PICK_PAOPAO_CNT = 6
    PICK_PWOER_CNT = 7
    PICK_LIFE_CNT = 8



class PaoPaoPVEGuanKaInst(game.core.PaoPaoPVP.paopaoInst.PaopaoInst):
    """ 房间类 """
    def __init__(self, mgr, rid, mode=1, max=2):
        super(PaoPaoPVEGuanKaInst, self).__init__(mgr, rid, mode, max, True)
        self.id = rid #房间id
        # self.roomType = mode #房间类型（1:PVP,）
        # self.mgr = mgr1
        self.mgr = weakref.proxy(mgr)
        self.name = "" #名称
        self.fight_mode = APP_MODE_PVE_GUANKA # PVE模式
        self.map_mode = 2 # 9*11
        self.max = max #最大人数
        self.state = 0 # 0:匹配，1，准备, 2:已开始
        # self.isGoReady = False
        self._st = 0 #当前局开始时间
        # self.players = {} #房间玩家列表 id：roomPlayer
        self.lplayers= [] # 匹配队列
        self.readys = {} #EC_VALUE
        self.Map = Game.res_mgr.res_mapConf
        self.isOver = False
        self._loop_task = None
        self.task_timmer = None # 任务计时器
        self.canJoin = True
        self.mapObj = None # 地图对象
        self.dPaoPao = {}
        self.iPaopaoTranceNo = 0
        self.random_name_data = Game.res_mgr.res_name  # 随机名字表
        self.player = None
        self.res_wujinInstData = Game.res_mgr.res_wujinInstData
        self.barrierNo = 0
        self.barrierObj = None
        self.aiLevel = 1
        self.barrWinType = 0 # 胜利类型
        self.barrWinCondition = {} #星星条件
        self.startTime = int(time.time())
        self.barrTime = 300
        self.isTrain = 0 # 是否训练模式
        # Game.sub(msg_define.MSG_ROLE_LEVEL_UPGRADE, self.event_lv_uprade)

    def setProcessor(self, playerID, processor):
        #print dir(processor)
        print "------------!!!!!!!!!!!---->><><><><><> 1",playerID, processor
        processor = weakref.proxy(processor)
        self.dProcessor[playerID] = processor

    def No(self):
        return self.barrierNo


    # 获取AI随机名字
    def getRandAIName(self):
        namekeys = self.random_name_data.keys()
        namekey = random.choice(namekeys)
        randomNameObj = self.random_name_data.get(namekey)
        if randomNameObj:
            return randomNameObj.name
        else:
            return "随机名字"

    def InitPVE(self):
        self.NameRes = Game.res_mgr.res_name

    # def check(self):
    #     # while 1:
    #     #     sleep(60)
    #     #     if len(self.players) == 0:
    #     #         self.end()
    #     pass

    # 广播
    def broadcast2(self, fname, data, exclude=()):
        for playerID, processor in self.dProcessor.iteritems():
            if playerID in exclude:
                continue
            if playerID <= 10000 and playerID > 1:
                continue
            try:
                if not processor:
                    continue
                spawn(processor.call, fname, data, noresult=True)
            except:
                pass

    def broadcast(self, fname, data, exclude=()):
        """ 广播 """
        # print "-------------PaopaoPVEInstGuanka", fname, self.id, self.dProcessor
        if self.dProcessor:
            self.broadcast2(fname, data, exclude)
            return
        from game.mgr.player import get_rpc_player
        for pid, player in self.players.iteritems():
            if pid in exclude:
                continue
            if pid <= 10000 and pid > 1:
                continue
            # data1 = self.packRoomPlayer(player
            # data["roleInfo"] = data1
            rpc_player = get_rpc_player(pid)
            rpc_player.broadcast(fname, data, _no_result=True)

    def sendGuild(self):
        from game.mgr.player import get_rpc_player
        pid = self.player.pid
        rpc_player = get_rpc_player(pid)
        rpc_player.sendGuild()

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
    # AI进入
    def makeAI(self):
        pid = random.randint(1,10000)
        name =  self.getRandAIName()
        icon = ""
        if not self.isTrain:
            aiAttr = self.barrierObj.getAIAttr()
            ppskil = random.randint(1, 6)
            dAttr = {
                "aiLevel":self.aiLevel,
                "PPSkin": ppskil
            }
            dAttr.update(aiAttr)
            # print dAttr, "------------------------------///////////////////// AI"
        else:
            # aiAttr = self.barrierObj.getAIAttr()
            dAttr = {
                "aiLevel":0
            }
            # dAttr.update(aiAttr)
        player = game.core.PaoPaoPVEGuanKa.paopaoPlayer.PaopaoRoomPlayer(self, pid, name, icon, dAttr)
        player.setIsAI()
        player.init_player()
        return player

    def init_barrier(self, dAttr):
        self.barrierNo = dAttr.get("barrierNo", 1)
        self.isTrain = dAttr.get("isTrain", 0)
        if not self.isTrain:
            self.barrierObj = self.res_wujinInstData.get(self.barrierNo)
            self.aiLevel = self.barrierObj.aiLevel
            self.barrWinType = self.barrierObj.itype
            self.barrWinCondition = self.barrierObj.condition
            self.barrTime = self.barrierObj.barrTime
        pass


    def enter_wait(self, pid, name, icon, dAttr, dEffect={}):
        # self.players[pid]
        print "------PVE WAIT-----pid",pid,self.id
        self.init_barrier(dAttr) # 初始化关卡信息
        # 玩家 坐下
        self.randomMap()

        if not self.players.has_key(pid):
            player = game.core.PaoPaoPVEGuanKa.paopaoPlayer.PaopaoRoomPlayer(self, pid, name, icon, dAttr, dEffect)
            player.init_player()
            self.players[pid] = player
            player.setPlayerSide(len(self.players))
            self.player = player

        peopleAICount = self.mapObj.layerconf.count(120)

        monsterAICount = self.mapObj.layerconf.count(MONSTER_AI_KEY)

        for i in xrange(peopleAICount):
            # ai 坐下
            mainAiPlayer = self.makeAI()
            aiPid = mainAiPlayer.pid
            if not self.players.has_key(aiPid):
                self.players[aiPid] = mainAiPlayer
                mainAiPlayer.setPlayerSide(len(self.players))
                print "----------------1"
                print "AI PID 1: ",aiPid
                print "AI Name 1:",mainAiPlayer.name


        for i in xrange(monsterAICount):
            # 怪物机器人
            aiMonster = self.makeAI()
            aiPid = aiMonster.pid
            if not self.players.has_key(aiPid):
                self.players[aiPid] = aiMonster
                aiMonster.player_side = aiMonster.player_side
                aiMonster.setAiLevel(50)
                aiMonster.lWalkArea = self.mapObj.getWalkArea(i)
                print "---------................-------2",i, self.mapObj.mapConfObj.lMonsterArea
                print "AI PID 2: ",aiPid
                print "AI Name 2:",aiMonster.name

        if len(self.players) >=2:
            print "match success!!!", self.players.keys()
            self.state = 1
            self.statrGuanKa()
            self.syncWaitingInfo()
            return 1, {}
        else:
            self.syncWaitingInfo()
            return 1, {}


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

    def statrGuanKa(self):
        self.start()
        pass

    def start(self):
        # 下发地图信息，比赛信息等
        self.syncMapData()
        self.state = 2
        # self.dPaoPao[]
        self.syncWaitingInfo()
        for pid, player in self.players.iteritems():
            self.dPaoPao[pid] = {}
        self.state = 3 # 切换成比赛中状态
        self.startTime = int(time.time())
        if self.isTrain:
            #print "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"
            #print "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"
            self.sendGuild()
        #spawn_later(6, self.reflashTest, 111)

    def reflashTest(self, timmerid=0):
        print 11111111111111111111,"reflashTest"
        data = {}
        data["player"] = {}
        for pid, player in self.players.iteritems():
            data["player"][pid] = {}
            data["player"][pid] = player.packRoleBaseBT()
        print data
        spawn(self.broadcast, 'syncpickItem', data)
    pass


    def randomMap(self):
        self.mapObj = PaopaoMap(self.barrierNo, self.isTrain)

    def passBarrier(self):
        pass

    # # 杀人
    # def kill_player(self, pid):
    #     BeAttacker = self.players.get(pid)
    #     life = BeAttacker.beHurt()
    #     if life <= 0:
    #         self.game_over()
    #     pass


    # 结算获得多少星
    def gameStar(self, playerId, playerObj):
        iResultType = self.barrierObj.itype
        condition = self.barrierObj.getPassCondition()
        condition = {1:{1:1},2:{1:1,2:120},3:{1:1,2:60}}
        star = 0
        for star, starCondition in condition.iteritems():
            isPassStar = self.chcekCanPass(playerId, playerObj, starCondition)
            if isPassStar:
                star += 1
            pass
        # if iResultType == RESULT_IME_TYPE:
        #     star = utility.GetLeftValue(useTime, condition, 0)
        if star >3:
            star = 3
        return star

    # 通关类型：
    # 1，是否对方死了
    # 2，通关时间
    # 3，炸砖块数量达到N
    # 4，放炸弹少于N
    # 5，速度道具捡到N个
    # 6，泡泡数量道具捡到N个
    # 7，泡泡威力道具捡到N个
    # 8，增加生命道具捡到N
    # 检测是否能通过星星检测
    def chcekCanPass(self, playerId, playerObj, starCondition):
        for starType, iCondition in starCondition.iteritems():
            if starType == CStarType.IS_WIN:
                return True
            elif starType == CStarType.UES_TIME:
                now = int(time.time())
                useTime = now - self.startTime
                if useTime <= iCondition:
                    return True
            elif starType == CStarType.FIGHT_BRICK_CNT:
                pass
            elif starType == CStarType.PUT_BOOM_CNT:
                pass
            elif starType == CStarType.PICK_SPEED:
                pass
            elif starType == CStarType.PICK_PAOPAO_CNT:
                pass
            elif starType == CStarType.PICK_PWOER_CNT:
                pass
            elif starType == CStarType.PICK_LIFE_CNT:
                pass
        return False



    # 完成关卡
    def guangkaFinish(self, rid, idx):
        # 先检测index
        if self.isFinish:
            return
        player = self.players.get(rid)
        star = 0
        if player == self.player and not player.isDie():
            from game.mgr.player import get_rpc_player
            player.setWin()
            if not self.isTrain:
                rpc_player = get_rpc_player(rid)
                # print "===========pid", pid
                star = self.gameStar(rid, player)
                usetime = time.time() - self.startTime
                if rpc_player:
                    rpc_player.updateStar(self.barrierNo, star, usetime)
                player.afterResult(star)
        data = {}
        data["player"]={}
        for pid, player in self.players.iteritems():
            data["player"][pid] = player.packRoleResult()
            if player == self.player:
                if player.win == 0:
                    star = 0
                data["player"][pid]['star'] = star
                if self.isTrain:
                    data["player"][pid]['GuanKaDesc'] = ""
                else:
                    data["player"][pid]['GuanKaDesc'] = "第%s关" % (self.No())
        print "----->>>>>>>>------gameGuanKaResult", data
        spawn(self.broadcast, 'gameGuanKaResult', data)
        self.isFinish = True


    # 结算
    def game_over(self):
        if self.isFinish:
            return
        from game.mgr.player import get_rpc_player
        star = 0
        for pid, player in self.players.iteritems():
            if player == self.player and not player.isDie(): # 赢了
                player.setWin()
                if not self.isTrain:
                    rpc_player = get_rpc_player(pid)
                    # print "===========pid", pid
                    star = self.gameStar(pid, player)
                    if rpc_player:
                        usetime = time.time() - self.startTime
                        rpc_player.updateStar(self.barrierNo, star, usetime)
                # data = player.packRoleBase()
                # data['win'] = player.win
                # data['addexp'] = 100
            else: # 输了
                if not self.isTrain:
                    rpc_player = get_rpc_player(pid)
                    if rpc_player:
                        usetime = time.time() - self.startTime
                        rpc_player.updateStar(self.barrierNo, star, usetime)
                        rpc_player.updateBarrInfo(self.barrierNo)
                # data = player.packRoleBase()
                # data['win'] = player.win
                # data['addexp'] = 0
            player.afterResult(star)
        data = {}
        data["player"]={}
        for pid, player in self.players.iteritems():
            data["player"][pid] = player.packRoleResult()
            if player == self.player:
                if player.win == 0:
                    star = 0
                data["player"][pid]['star'] = star
                if self.isTrain:
                    data["player"][pid]['GuanKaDesc'] = ""
                else:
                    data["player"][pid]['GuanKaDesc'] = "第%s关" % (self.No())
        print "----->>>>>>>>------gameGuanKaResult", data
        spawn(self.broadcast, 'gameGuanKaResult', data)
        self.isFinish = True
        # self.againGuanka(self.player.pid)
        pass

    # 同步炸弹爆炸, 坐标要发当前格子的坐标，
    # status = -1 # 非法泡泡
    # status = 0 # 时间还没到
    # status = 1 # 泡泡有效 没有打到人
    # status = 2 # 泡泡有效 有打到人
    # , killplayerX = -1, killplayerY = -1
    def syncBoomPlayer(self, rid, paopaoID, x, y, idx, killrid=0, killidx=-1, playerID=0):
        # print "==================syncBoomPlayer",rid, paopaoID, x, y, idx, killrid
        #


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

    # 杀人
    def kill_player(self, pid):
        BeAttacker = self.players.get(pid)
        life = BeAttacker.beHurt()
        if BeAttacker.isAI and life <=0:
            data = {}
            data["killID"] = pid  #
            spawn(self.broadcast, 'syncKillMst', data)
            del self.players[pid]
        if life <= 0 and BeAttacker == self.player: # 自己被杀了
            self.game_over()
        elif life <= 0 and len(self.players) <= 1:
            self.game_over()
        else:
            self.reflashProperty()

        pass



    # 怪物杀人
    def kill_player_by_monster(self, attacker_pid, beattacker_pid):
        Attacker = self.players.get(attacker_pid)
        BeAttacker = self.players.get(beattacker_pid)
        if Attacker.aiLevel >=50 and BeAttacker.isAI:
            print "ERROR:BeAttacker is ai", beattacker_pid
            return
        life = BeAttacker.beHurt()
        if BeAttacker.isAI and life <=0:
            data = {}
            data["killID"] = pid  #
            spawn(self.broadcast, 'syncKillMst', data)
            del self.players[pid]
        if life <= 0 and BeAttacker == self.player: # 自己被杀了
            self.game_over()
        elif life <= 0 and len(self.players) <= 1:
            self.game_over()
        else:
            self.reflashProperty()


    #
    # # 重连回到游戏
    # def reconnect_to_Fight(self, pid):
    #     print "------fight_reconnect"
    #     print "------fight_reconnect"
    #     print "------fight_reconnect"
    #     print "------fight_reconnect"
    #     print "------fight_reconnect"
    #     self.syncMapData()
    #     if pid in self.waitForReconnect:
    #         self.waitForReconnect.remove(pid)
    #     pass

    # 再来一次
    def againGuanka(self, rid):
        from game.mgr.player import get_rpc_player
        rpc_player = get_rpc_player(rid)
        if rpc_player:
            rpc_player.rc_againGuanka()
        pass

    # 下一关
    def nextGuanka(self, rid):
        mapInfo = getattr(self, "mapInfo", {})
        barrierNo = mapInfo.get("barrierNo", 1)
        allGuanKa = self.res_wujinInstData.keys()
        maxGuanka = max(allGuanKa)
        if maxGuanka <= barrierNo:
            barrierNo = maxGuanka
        self.rc_C2GGotoBarrier(barrierNo)



import random
import types
from datetime import datetime
from game.core.PaoPaoPVEGuanKa.paopaoMap import *
import game.core.PaoPaoPVEGuanKa.paopaoPlayer
