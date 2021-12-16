#!/usr/bin/env python
# -*- coding:utf-8 -*-

from corelib import spawn

from game.define import constant
from game import Game
import game.mgr.player
import corelib.xreload as x
import corelib.hotupdate as h
import app
from game.core.testcontainer import *

# app.frame.reload_modules(["game.player.player", "game.player.bag"])


gm_patch = {
    '1': "game.core.",
    '2': "game.gm.",
    '3': "game.models.",
    '4': "game.protocal.",
    'gm': "game.gm.gmFunc"
}



# 单个进程更新特定的py文件
#     - 修改该py文件的代码内容
#     - 通过python main.py shell 接入该进程
#     - 执行如下代码更新模块，比如说要更新 game/player/player.py 文件
#         import corelib.xreload as x
#         x.re("game.player.player")

def ud(who, *mod):
    app.frame.main_proxy.reload_modules(list(mod))

# def ud(who, udcmd):
#     # print who.entergame()
#     x.re(udcmd)
#     reload_modules(who, udcmd)



# 快捷ud
def uds(who, pathkey, filename=''):
    pre_path = gm_patch.get(pathkey, None)
    if not pre_path: return None
    spath = pre_path + filename
    try:
        x.re(spath)
        reload_modules(who, spath)
        print "============ updata path ============ Success >>>", spath
    except:
        print "============ updata path ============ Fail >>>", spath
    pass

def udx(who, path):
    print "--------sss"
    h.Update(path)


# 整个服务器环境所有进程更新特定文件
#     - 修改该py文件的代码内容
#     - 通过python main.py shell 接入主节点进程  （game主进程）
#     - 执行如下代码更新模块，比如说要更新 game/player/player.py, game/player/bag.py 文件
#         import app
#         app.frame.reload_modules(["game.player.player", "game.player.bag"])
def reload_modules(who, udcmd):
    l = [udcmd]
    app.frame.reload_modules(l)


# GM 修改角色名字
# mdName 6536010001 23l2
# udx game.mgr.player
# ud game.mgr.player
# ud game.core.player
# ud corelib.hotupdate
def mdName(who, rid, name="wewe"):
    p = game.mgr.player.get_rpc_player(int(rid))
    p.setName(name)
    p.save(forced=True)


def test(who):
    who.rc_enterXYRoom()

def test1(who):
    who.getXiyouFreeRoomId()

# # 读库数据初始化
# def load_from_dict(self, data):
#     self.mailTranceNo = data.get("mailTranceNo", '')  # 邮件唯一id （添加给角色才生成， 否则为一个系统设定值）角色id + 自增
#     self.iOwner = data.get("iOwner", 0)  # 拥有者id
#     self.sTitle = data.get("sTitle", 0)  # 邮件标题
#     self.sContent = data.get("sContent", 0)  # 邮件内容
#     self.iCreattime = data.get("iCreattime", 0)  # 生成时间


# GM 发邮件
def sMail(who, mid=6488010001):
    mid = mid
    Game.rpc_mail_svr.rc_addMail(mid,{"sTitle":"系统邮件1",
                                      "sContent":"系统邮件2"})

# 获取根管理员id
def gRoot(who):
    from game.core.player import Player
    lRootPlayer = Game.store.query_loads(Player.DATA_CLS.TABLE_NAME,
                                         dict(account=config.root_player_account, password=config.root_player_password))
    print lRootPlayer
    pass

# 添加金币
def addcoin(who, iAdd):
    # print iAdd
    # if is_number(iAdd):
    try:
        iAdd = float(iAdd)
        who.base.setCoin(iAdd)
        who.save(forced=True)
    except TypeError:
        print "addcoin fail", type(iAdd), iAdd
    pass

# 添加钻石
def adddia(who, iAdd):
    # print iAdd
    # if is_number(iAdd):
    try:
        iAdd = float(iAdd)
        who.base.setDiamond(iAdd)
        who.save(forced=True)
    except TypeError:
        print "setDiamond fail", type(iAdd), iAdd
    pass

def taobj(who, iNo):
    print "---------- taobj",iNo
    obj = game.core.testcontainer.New(int(iNo), who)
    print "---------- taobj obj",obj
    who.testctn.AddItem(obj)
    print "---------- taobj obj 333"
    print who.testctn.GetAllItemList()

def saobj(who):
    print who.testctn.GetAllItemList()

# def is_number(s):
#     try:
#         float(s)
#         return True
#     except ValueError:
#         pass
#
#     try:
#         import unicodedata
#         unicodedata.numeric(s)
#         return True
#     except (TypeError, ValueError):
#         pass
#
#     return False



def testAlgorithm(who, table_id):
    addr = config.algorithm_addr
    table_id = int(table_id)

    from game.mgr.algorithm.algorithmroom import get_table_proxy, get_table_mgr_proxy
    rpc_table_mgr = get_table_mgr_proxy(addr, table_id)
    rs = rpc_table_mgr.has_table(table_id)
    if not rs:
        coin_rate, diff, totalPlayerNum, rejustDiff_Level, tableId = 1, 1, 16, 1, table_id
        data = coin_rate, diff, totalPlayerNum, rejustDiff_Level, tableId
        rpc_table_mgr.new_table(table_id, data)

    rpc_table = get_table_proxy(addr, table_id)
    tableId = table_id
    perPlayerPerItemBet = [[10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    itemTotalBet = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    maxBet = 10
    minBet = 1
    gTotalBenifit = 100
    giMultiIndex = 1
    multiComb = 1
    resp =  rpc_table.QsOceanSharkAlgIn(tableId, perPlayerPerItemBet, itemTotalBet, maxBet, minBet, gTotalBenifit, giMultiIndex, multiComb)
    print '========test111111111111111111111111111111111=============', re


def mPiclib(who, count, idx=1):
    t2.makePic(who, int(count), int(idx))
    pass

def mShowMail(who):
    who.getAllMail()
    pass

# reloadpy game.gm.gmFunc
# Test 6537010001
# 查找某账号的所有下家，以及登录账号，密码
def Test(who, rid=6537010001):
    rid = int(rid)
    from game.common.db import new_game_store
    from game.core.player import Player

    store = new_game_store()
    lChildren = Game.rpc_membtree_svr.rc_getAllChildren(who.base.code)
    who.notify(str(lChildren))
    print "---lChildren:", lChildren
    for iCode in lChildren:
        iRid = Game.rpc_membtree_svr.getRidByCode(iCode)
        lRootPlayer = store.query_loads(Player.DATA_CLS.TABLE_NAME,
                                             dict(id=iRid))
        # print "lRootPlayer:", lRootPlayer
        dplayer = lRootPlayer[0]
        print "-->",iRid,dplayer.get("password"),dplayer.get("account"),dplayer.get("name", "")

    # --> 6551010001 1 q1
    # --> 6552010001 1 q2
    # --> 6553010001 1 q3
    # --> 6554010001 1 q4
    # --> 6555010001 1 q5
    # --> 655600010001 1 wwwq
    # --> 655700010001 1 wwq
    # --> 655800010001 1 www
    # --> 655900010001 1 er
    # --> 656000010001 1 er1
    # --> 656100010001 1 er2
    # --> 656200010001 1 er3
    # --> 656300010001 1 er4
    # --> 656400010001 1 wwwcc
    # --> 656600010001 2 hkm20


# reloadpy game.gm.gmFunc
# Test 6537010001
# 查找某账号的所有下家信息
def getChildrenInfo(who):
    from game.common.db import new_game_store
    from game.core.player import Player

    store = new_game_store()
    lChildren = Game.rpc_membtree_svr.rc_getAllChildren(who.base.code)
    who.notify(str(lChildren))
    # print "---lChildren:", lChildren
    l = []
    for iCode in lChildren:
        d = {}
        iRid = Game.rpc_membtree_svr.getRidByCode(iCode)
        lRootPlayer = store.query_loads(Player.DATA_CLS.TABLE_NAME,
                                             dict(id=iRid))
        dplayer = lRootPlayer[0]
        # print "-->",iRid,dplayer.get("password"),dplayer.get("account")
        d["id"] = iRid
        d["name"] = dplayer.get("name", "")
        d["account"] = dplayer.get("account", "")
        d["coin"] = dplayer.get("coin", 0)
        l.append(d)
    print l

def getCount(who):
    user = Game.rpc_player_mgr.get_count()
    who.notify(user)

def resetPws(who, newPws=""):
    if not newPws:
        who.notify("请输入密码")
        return False
    who.setPasswordForce(newPws)

def GM_creatRole(who, account, password, isAgent=0):
    '''GM创建代理'''
    if account and password:
        ok, rs = who.GM_createAgentByWeb(account, password, isAgent)
        print "------", ok, rs
        if ok:
            who.notify("创建成功")
        else:
            who.notify("创建失败")
# from game.core.caishen.makeCaishenDict import t2
from game.define import  errcode

def test(who):
    # who.start_match()
    # player = game.mgr.player.get_rpc_player(who.id)
    # print "---------------test",player,player.rc_enterPPRoom()

    player = game.mgr.player.get_rpc_player(200010001)
    playerObj = player.rf_sendPlayer(200010001)
    Game.glog.log2File("testDebug", "-----找到BEPMain x1xxx player rid:%s"%(player.getUID()))

def saveH(who):
    player = game.mgr.player.get_rpc_player(who.id)
    player.cycleHour.Save("test", 111)
    print "------saveH",player.cycleHour.Query("test", 111)



def upgrade(who, exp):
    who.Upgrade(exp)
    pass

def clear_lv(who):
    who.base.lv = 1
    who.base.exp = 0
    who.base.curexp = 0
    who.base.markDirty()
    pass

def analyze_mem(who):
    import corelib.tools
    corelib.tools.analyze_mem()
    pass


def printMemory(who):
    import sys
    import gc
    a = {}
    b = {}
    iTotal = 0
    for obj in gc.get_objects():
        if type(obj) in a:
            a[type(obj)] += sys.getsizeof(obj)
            b[type(obj)] += 1
        else:
            a[type(obj)] = sys.getsizeof(obj)
            b[type(obj)] = 1
    rs_a = sorted(a.items(), key=lambda x: x[1], reverse=True)
    rs_b = sorted(b.items(), key=lambda x: x[1], reverse=True)
    for one in rs_a:
        Game.glog.log2File("memLogA", "%s|%s\n" % one)
    for one in rs_b:
        Game.glog.log2File("memLogB", "%s|%s\n" % one)

def printRef(who):
    import random
    from game.core.player import Player

    import objgraph
    objs = objgraph.by_type('game.core.item.itemctn.CItemContainer')
    print "---------",objs
    obj = random.choice(objs)
    print "---------",obj
    RpcHandler = objgraph.by_type('game.protocal.player.PlayerRpcHandler')
    oProcesser = objgraph.by_type('game.common.gateway.Processer')
    oGateWayMgr = objgraph.by_type('game.common.gateway.GateWayMgr')
    oSubFrame = objgraph.by_type('corelib.frame.SubFrame')
    oMultiAttr = objgraph.by_type('corelib.frame.MultiAttr')


    # extra_ignore = (id(obj.cycleHour), id(obj.cycleDay), id(obj.cycleDay_7), id(obj.cycleWeek),
    #                 id(obj.cycleMonth), id(obj.base),
    #                 )
    # from game.protocal.player import PlayerRpcHandler
    extra_ignore = [id(RpcHandler), id(oProcesser), id(oGateWayMgr), id(oSubFrame), id(oMultiAttr)]
    objgraph.show_backrefs(obj, max_depth=6, too_many=7,refcounts=True, extra_ignore=extra_ignore, filename='d:\\bag3.dot')
    # objgraph.show_chain(
    #     objgraph.find_backref_chain(
    #         obj,
    #         objgraph.is_proper_module
    #     ),
    #     filename='d:\\player.dot'
    # )
# def updatePvpRank(self, rid, sName, sPic, winCount, winRate, wechatId=""):
def updateRank(who):
    who.updatePvpRank()
    # Game.rpc_rank_info.updatePvpRank(who.data.id, who.data.account, "", 3, 52)
    who.updateLvRank()
    pass

# 微信登录
def rc_loginWX(self):
    url2 = "https://api.weixin.qq.com/sns/jscode2session?appid=wx11adc66e301668c0&secret=0a16cd00dab8deb4c42dc8fb4ad7c8a9&js_code=0239bKWf2AhBGH0YpLZf2mDFWf29bKWv&grant_type=authorization_code"
    import urllib2
    import json
    data2 = {
            "appid":"wx11adc66e301668c0",
            "secret":"0a16cd00dab8deb4c42dc8fb4ad7c8a9",
            "js_code":"0239bKWf2AhBGH0YpLZf2mDFWf29bKWv",
            "grant_type":"authorization_code"
        }
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
               "Content-Type": "application/json"}
    url = "https://api.weixin.qq.com/sns/jscode2session?"
    req = urllib2.Request(url + urllib.urlencode(data2),headers=header_dict)
    s = time.time()
    res = urllib2.urlopen(req,timeout=5)
    res = res.read()
    print "res:",res
    print time.time() - s

def TimeOut(self):
    pass

def t1(who):
    Game.rpc_rank_info.test1(who)
    pass


def saveRank(who):
    Game.rpc_rank_info.SaveRank()
    pass

#  背包 ==========================
def addItem(who, iNo, num = 1):
    game.core.item.net.AddItem(who, int(iNo), int(num))
    pass

def getItem(who, iNo):
    item = who.bag.GetItemByNo(iNo)
    print "-------getItem--------",iNo
    print item.No(), item.Num(), item.itemTranceNo
    print item

def getItemNum(who, iNo):
    iNo = int(iNo)
    num = who.bag.getItemNum(iNo)
    print "------------num", num

def cleanAllItem(who):
    who.bag.CleanAllItems()

#  商品 ==========================
def buyItem(who, iNo, num = 1):
    game.core.shop.net.BuyItem(who, int(iNo), int(num))

    item = who.shop.GetItemByNo(iNo)
    print item.No(), item.getHasBuyCount(), item.shopTranceNo
    print item
    itemId = item.itemId()
    print getItem(who, itemId)
    pass

def getbuyItem(who, iNo):
    item = who.shop.GetItemByNo(iNo)
    print "-------getbuyItem--------",iNo
    print item.No(), item.getHasBuyCount(), item.shopTranceNo
    print item

#
def getbuyItemNum(who, iNo):
    iNo = int(iNo)
    num = who.shop.getItemNum(iNo)
    print "------------num", num

def cleanAllbuyItem(who):
    who.shop.CleanAllItems()

def rc_openShopUI(who):
    print who.netCmd.shopNet.rc_openShopUI(who, 0)



def buy(who,iNo):
    iNo = int(iNo)
    res = who.netCmd.shopNet.rc_playerVidio(who, iNo)
    who.save(forced=True)
    print res

def showshop(who, iNo):
    iNo = int(iNo)
    res = who.netCmd.shopNet.rc_openShopUI(who, iNo)
    print res

def printFightAddr(who):
    sAddr = who.Query("FightRoomAddr")
    print sAddr

def addcount(who):
    who.addFightEffect("LIFE", 1, 1, 0)
    print who.Query("fightEffect", {})


def checkcount(who):
    print who.packFightEffect()

def cleanshop(who):
    who.shop.CleanAllItems()

# ud game.core.diyMap.net
def getMyMaps(who):
    who.rc_getMyMaps()

def setMyMaps(who):
    who.rc_setFightMap(1001)

def getNewRank(who):
    print who.rc_getNewRank()

def showLogin(who):
    who.show_OneDayReward()
    pass

def getbase(who):
    print who.base.to_init_dict()


def testSev(who):
    Game.rpc_server_info.cycDaySet("test", 1111,_no_result=True)

def gettestSev(who):
    print Game.rpc_server_info.cycDayGet("test")

def testPVE(who):
    import game.core.NewWaitRoom
    game.core.NewWaitRoom.gCNewWaitRoomMng.EnterPVEGuanKa(who.id)

def testleft(who):
    condition = {600:0,200:1,90:2,60:3}
    star = utility.GetLeftValue(50, condition)
    print star

# ud game.gm.gmFunc
def testgk(who):
    print who.rc_getOneDayReward()


# ccd 1 天清
# ccd 2 周清
def ccd(who, iType):
    if int(iType) == 1:
        who.cycleDay.Clear()
    elif int(iType) == 2:
        who.cycleWeek.Clear()

def getClass(who):
    print who.getRoleDetail()

# A端，创建1V1房间
def test1v1(who):
    rs, data = who.outToFight()
    if rs:
        print who.id
        game.core.NewWaitRoom.gCNewWaitRoomMng.creatFriend1v1(who.id)

def create1v1(who):
    rs, data = who.outToFight()
    if rs:
        who.open1V1Room()

# B端  key 为A端的角色ID
# enter1V1 600000002
def enter1V1(who, key):
    rs, data = who.outToFight()
    if rs:
        print who.id
        game.core.NewWaitRoom.gCNewWaitRoomMng.getIntoFriend1V1(who, key)



    # self.cycleHour = CycleHour(self)  # 小时周期数据
    # self.cycleDay = CycleDay(self)  # 天周期数据
    # self.cycleWeek = CycleWeek(self)  # 周周期数据

    # self.cycleDay_2 = CycleDay(self, keepCyc=2)  # 天周期数据 保存2天内的
    # self.cycleDay_7 = CycleDay(self, keepCyc=7)  # 天周期数据 保存7天内的
    # self.cycleWeek = CycleWeek(self)  # 周周期数据
    # self.cycleMonth = CycleMonth(self)  # 月周期数据

def ssd(who):
    who.show_sevenDayReward()


def cleanGuanKaInfo(who):
    who.Set("GuanKaInfo", {})

# 本地第一张地图发出啊邀请
def open1V1RoomByMap(who):
    who.open1V1RoomByMap(1001)
    pass

# 本地进入1v1
# EG: enter1V1Room 600000002
def enter1V1Room(who, fightRoomKey):
    who.enter1V1Room(fightRoomKey)
    pass

def showAllClassList(who):
    print who.rc_showAllClassList()


# 记录属性
def logRoleProperty(who):
    print "LV: ", who.Lv()
    print "Exp: ", who.getExp()
    print "CurExp: ", who.getCurExp()
    print "Coin: ", who.getCoin()

def getUpgradeReward(who):
    who.getUpgradeReward()

def getNextGuild(who):
    who.getNextGuild()
    pass

# 设置到某一步引导
def setGuildId(who, gid):
    GuildID = int(gid)
    who.Set("GuildID", GuildID)

# 重置引导
def resetGuild(who):
    who.Set("GuildID", 1)
    who.Set("GuildKey", 1)
    who.Set("GuildStep", 1)


def udbarrPas(who, iNo, iPasTime):
    sName = "sss"
    iPasTime = int(iPasTime)
    who.updatebarrPasTime(iNo, iPasTime, sName)

def getbarrPas(who, iNo):
    print who.getbarrPasTimeInfoByNo(iNo)

def getBarrierInfo(who):
    print who.getBarrierInfo(2)

def t4(who):
    print who.getOpenCtrlData()


def getTili(who):
    tili = who.getTiliCnt()
    TiliRecoveryTime = who.Query("TiliRecoveryTime", 0)
    print "----------", tili, TiliRecoveryTime

def useTili(who):
    who.doUseTili(10)
    pass

def addTiliCnt(who):
    who.addTiliCnt(50, game.define.constant.CTili.TOOL_ADD)

def upSkill(who):
    who.rc_C2G_Upgrade(1)
    who.rc_C2G_Upgrade(2)

def claanAll(who):
    cleanAllbuyItem(who)
    cleanAllItem(who)
    who.base.claanAll()
    who.cycleDay.Clear()
    who.cycleWeek.Clear()
    pass

# 获取用户信息
def getWX(who):
    who.G2C_getWXInfo()

# 重置获取状态
def resetWX(who):
    who.Set("bSaveWXInfo", 0)

# 进入关卡
def gotobrr(who, barrierNo):
    barrierNo = int(barrierNo)
    who.rc_C2GGotoBarrier(barrierNo, isGm=True)

def resetSkillLv(who):
    who.base.setSkill({})
    pass

def n1(who):
    sStr = "闯关模式，第6~10层即将更新，各位客官敬请期待吧！"
    who.rf_scrollNotice(sStr)

def n2(who):
    sStr = "官方客服微信号：tianyaoStudio，欢迎广大玩家沟通交流！"
    who.rf_scrollNotice(sStr)

def n3(who):
    sStr = "新版本即将更新，各位客官请密切关注吧！"
    who.rf_scrollNotice(sStr)

def n4(who):
    sStr = "关注微信公众号【天曜工作室】，获取最新更新动态吧！"
    who.rf_scrollNotice(sStr)

def n5(who):
    sStr = "尊敬的玩家，现在是临时维护，请18点之后再来玩哦"
    data = {"tips": sStr}
    Game.player_mgr.broadcast("notify", data)

def reloadcfg(who, *tname):
    Game.rpc_server_info.reloadConfig(list(tname))

    for _, logic in Game.rpc_logic_game:
        print _, logic
        # if logic:
        #     logic.reloadConfig(list(tname))


if not globals().has_key("G_ShowKey"):
    G_ShowKey = 1
def sk(who, showkey):
    global G_ShowKey
    showkey = int(showkey)
    G_ShowKey = showkey


def te(who):
    import pprint
    l = who.rc_getTotalGuankaRank(who)
    pprint.pprint(l)
    # print who.rc_getTotalGuankaRank()

def clr(who):
    who.cleanGuankaRank()

if not globals().has_key("G_is0210Ver"):
    G_is0210Ver = 0
def nv(who, newVer):
    global G_is0210Ver
    newVer = int(newVer)
    G_is0210Ver = newVer

def rsu(who):
    who.Set("UnluckFunc", {})

def uprk(who):
    # plyer
    pass

def b1(who, iType, iNo):
    print iType, iNo
    iType = int(iType)
    iNo = int(iNo)
    who.playVidioBefore(iType, iNo)
    pass

def f1(who):
    who.playVidioFinish()
    pass

import game.core.item.net
import game.core.shop.net
import weakref
from corelib import spawn, log, spawn_later
import urllib
import config
import types
import game.core.login.net
from game.common import utility
import game.core.NewWaitRoom