#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import time

from gevent import sleep
from grpc import DictExport, DictItemProxy, get_proxy_by_addr
import gevent
import uuid

from gevent import sleep
from gevent.lock import RLock
from gevent.event import Event
from grpc import DictExport, DictItemProxy, get_proxy_by_addr
from game import Game

from corelib import spawn, spawns, log
from corelib.cache import TimeMemCache
from corelib.gtime import current_time
from corelib.frame import MSG_FRAME_APP_ADD, MSG_FRAME_APP_DEL, MSG_ALL_LOGIC_START
from corelib.common import uuid
from game import Game
from game.define import errcode
from game.define.msg_define import MSG_LOGOUT
from game.define.store_define import *
from game.core.player import ModelPlayer, Player
from game.common import utility
from game.gm import report
import config


def get_rpc_player(pid, offline=True):
    app_name, addr = Game.rpc_player_mgr.get_sub_mgr_addr(pid, offline=offline)
    if not app_name:
        return
    proxy = SubPlayerMgr.cls_get_player_proxy(pid, addr=addr, local=0)
    return proxy


class GPlayerMgr(object):
    """ 联合进程使用的总角色管理类 """
    _rpc_name_ = 'rpc_player_mgr'
    TIME_OUT = 0.1

    def __init__(self):
        self._players = {}  # {pid:sub_mgr_id} 玩家对应子进程
        self.app_pids = {}
        self.pid_login_waiter = {}
        self.lock = RLock()

        #缓存优化
        self._logouts = {}  # {pid:sub_mgr_id} 退出玩家对应子进程缓存优化\
        self._acc2pid = {}  # {account:pid} 登录信息对应pid
        self.logons = TimeMemCache(size=1000, default_timeout=3, name='rpc_player_mgr.logons')
        #重登令牌
        self.relogin_cache = TimeMemCache(size=2000, default_timeout=3600, name='rpc_player_mgr.relogin_cache')
        self.notoken_cache = TimeMemCache(size=10, default_timeout=300, name='rpc_player_mgr.notoken_cache')

        #名称相关
        self._ready_names = set()  # 预备名列表
        self.name2pids = {}
        self.pid2names = {}
        self.paused = False  # 暂停服务

        self.overload_time = 0

        Game.sub(MSG_FRAME_APP_ADD, self._msg_app_add)
        Game.sub(MSG_FRAME_APP_DEL, self._msg_app_del)

    def SetNoTokenLogin(self, pid):
        self.notoken_cache.set(pid, 1)

    def getGPlayerMgrInfo(self):
        resp = {}
        resp["_players"] = len(self._players)
        resp["app_pids"] = len(self.app_pids)
        resp["pid_login_waiter"] = len(self.pid_login_waiter)
        resp["_logouts"] = len(self._logouts)
        resp["name2pids"] = len(self.name2pids)
        resp["pid2names"] = len(self.pid2names)
        resp["logons"] = (len(self.logons._caches), len(self.logons._times), self.logons.size)
        return resp

    def start(self):
        pass

    def after_all_start(self):
        print "after_all_start in GPlayerMgr------------------------->>"
        pass

    def after_start(self):
        # print "after_start in GPlayerMgr------------------------->>"
        pass

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def gw_open(self, processor):
        """ 连接建立 """
        hd = PlayerMgrrpcHandler()
        hd.set_rpc(processor)
        if not self.paused:
            sleep(30)
        hd.stop()

    def _msg_app_add(self, app_name, addr, names):
        if SubPlayerMgr._rpc_name_ not in names:
            return
        log.info('[player_mgr]reg sub_player_mgr:%s', app_name)
        self.app_pids[app_name] = set()
        if len(self.app_pids) == config.logic_pool:
            Game.safe_pub(MSG_ALL_LOGIC_START)

    def _msg_app_del(self, app_name, addr, names):
        """ 子进程退出,清理数据 """
        if SubPlayerMgr._rpc_name_ not in names:
            return
        log.info('[player_mgr]unreg sub_player_mgr:%s', app_name)
        self.app_pids.pop(app_name, None)

        #缓存清理，玩家退出
        def _unreg():
            pids = [pid for pid, _app_name in self._logouts.iteritems() if _app_name == app_name]
            for pid in pids:
                self._logouts.pop(pid, None)
            for pid, _app_name in self._players.items():
                if _app_name != app_name:
                    continue
                self.del_player(_app_name, pid, str(uuid.uuid1()))
        spawn(_unreg)

    def choice_sub_mgr(self):
        """ 选择一个逻辑进程,
        @result: sub_name, sub_mgr """
        keys = self.app_pids.keys()
        nofull_keys = [app_name for app_name in keys if len(self.app_pids[app_name]) < config.logic_players]
        if nofull_keys:
            app_name = random.choice(nofull_keys)
        else:
            #随机选择
            app_name = random.choice(keys)
        return app_name, Game.get_service(app_name, SubPlayerMgr._rpc_name_)

    def get_sub_mgr(self, pid, offline=False, forced=True):
        """ 获取玩家所在进程的player_mgr对象
        @param:
            pid: 玩家id
            offline: 是否离线也选择一个子进程
            forced: 是否离线也强制选一个
        @return:
            app_name, rpc_sub_mgr
        """
        self.lock.acquire()
        try:
            app_name = self._players.get(pid)
            ensure = False
            if not app_name and offline:
                ensure = True
                app_name = self._logouts.get(pid)
            if not app_name and forced:
                app_name, _ = self.choice_sub_mgr()
            if not app_name:
                self.lock.release()
                return '', None
            sub_mgr = Game.get_service(app_name, SubPlayerMgr._rpc_name_)
            if ensure:
                rs = sub_mgr.load_player(pid)
                if not rs:
                    self.lock.release()
                    return '', None
                else:
                    self._logouts[pid] = app_name
            self.lock.release()
            return app_name, sub_mgr
        except:
            self.lock.release()
            log.log_except()
            return '', None

    def get_sub_mgr_addr(self, pid, offline=False, forced=True):
        try:
            app_name, sub_mgr = self.get_sub_mgr(pid, offline=offline, forced=forced)
            addr = sub_mgr.get_addr()
            return app_name, addr
        except:
            return '', None


    def add_player(self, app_name, pid, name):
        """ 玩家登陆,防止在短时间内重复登录 """
        self._add_name_id(pid, name)
        self._players[pid] = app_name
        self.app_pids[app_name].add(pid)
        self.relogin_cache.delete(pid)
        return True

    def del_player(self, app_name, pid, token):
        """ sub_mgr调用,通知玩家退出 """
        self._logouts[pid] = app_name
        self._players.pop(pid, None)
        if app_name in self.app_pids:
            pids = self.app_pids[app_name]
            if pid in pids:
                pids.remove(pid)
        self.relogin_cache.set(pid, token)
        Game.safe_pub(MSG_LOGOUT, pid)

    def remove_pids(self, pids):
        """ 清理sub_mgr的pid缓存 """
        for pid in pids:
            self._logouts.pop(pid, None)

    @property
    def count(self):
        return len(self._players)

    def get_count(self):
        return self.count

    def _add_name_id(self, pid, name):
        if pid in self.pid2names or not name:
            return
        self.name2pids[name] = pid
        self.pid2names[pid] = name
        if name in self._ready_names:
            self._ready_names.pop(name)

    def get_id_by_name(self, name):
        """ 根据名称获取对应玩家id """
        try:
            return self.name2pids[name]
        except KeyError:
            pid = ModelPlayer.name_to_id(name)
            if pid is None:
                return
            self._add_name_id(pid, name)
            return pid

    def get_name_by_id(self, pid):
        """ 查询pid """
        try:
            return self.pid2names[pid]
        except KeyError:
            name = ModelPlayer.id_to_name(pid)
            if name is None:
                return
            self._add_name_id(pid, name)
            return name

    def get_names_by_id(self, ids):
        """ 获取玩家名列表 """
        rs = {}
        for i in ids:
            n = self.get_name_by_id(i)
            if n is None:
                continue
            rs[i] = n
        return rs

    def get_online_ids(self, pids=None, random_num=None):
        """ 返回在线的玩家id列表,
        pids: 查询的玩家列表,返回在线的ids
        random:整形, 随机选择random个pid返回
        """
        if random_num is not None:
            if len(self._players) <= random_num:
                return self._players.keys()
            return random.sample(self._players, random_num)
        if not pids:
            return self._players.keys()
        return [pid for pid in pids if pid in self._players]

    def is_online(self, pid):
        return pid in self._players

    def _login_check_player(self, pid):
        """ 检查登陆情况，防止重复登陆,短时登陆 """
        if not pid:
            return True
        if self.logons.get(pid):
            log.info(u'禁止玩家(%s)短时登录', pid)
            return False
        self.logons.set(pid, 1)
        return True

    def _login(self, processor, pid, fRoomID=0):
        """ 玩家登陆请求
        返回: isOk, error or sid
        """
        if self.count >= config.max_players:
            return 0, errcode.EC_USER_MAX
        elif not self._login_check_player(pid):
            return 0, errcode.EC_LOGIN_ERR

        # (app_name, sub_mgr) = self.get_sub_mgr(pid)
        # #选取逻辑进程, 进入逻辑进程
        # if not app_name and pid:
        app_name, sub_mgr = self.get_sub_mgr(pid, offline=True)
        #登陆
        rs = sub_mgr.player_login(processor.pid, pid, fRoomID)
        #网关连接子进程
        addr = sub_mgr.get_addr()
        #等待连接成功后才返回,要不前端在得到返回后马上发送的数据可能会丢失
        print "-------->>>>>>> <<<<<<<----------", addr
        processor.connect(*addr)

        log.debug(u'loginSNS finish:%s', rs)
        return 1, rs

    def _relogin(self, processor, pid, fRoomID=0):
        """ 玩家登陆请求
        返回: isOk, error or sid
        """
        if self.count >= config.max_players:
            return 0, errcode.EC_USER_MAX
        elif not self._login_check_player(pid):
            return 0, errcode.EC_LOGIN_ERR

        # (app_name, sub_mgr) = self.get_sub_mgr(pid)
        # #选取逻辑进程, 进入逻辑进程
        # if not app_name and pid:
        app_name, sub_mgr = self.get_sub_mgr(pid, offline=True)
        #登陆
        rs = sub_mgr.player_relogin(processor.pid, pid)
        # rs = dict(rid=pid, have=1)
        #网关连接子进程
        addr = sub_mgr.get_addr()
        #等待连接成功后才返回,要不前端在得到返回后马上发送的数据可能会丢失
        print "-------->>>>>>> _relogin <<<<<<<----------", addr
        processor.connect(*addr)

        log.debug(u'loginSNS finish:%s', rs)
        return 1, rs


    def sub_login_finish(self, pid):
        if pid in self.pid_login_waiter:
            waiter = self.pid_login_waiter.pop(pid)
            waiter.set()

    def broadcast(self, proto, data, exclude=[]):
        for app in self.app_pids:
            sub_mgr = Game.get_service(app, SubPlayerMgr._rpc_name_)
            sub_mgr.broadcast(proto, data, exclude)

#--------------------  业务流程 -------------------------------
    # isAgent 是否代理，代理和推广号是不一样的
    def rc_register(self, account, password, pcode='', verified_code='',isAgent=0):
        """ 注册账号 """
        # pcode = '185a2db51L'
        # isHascode = Game.rpc_membtree_svr.rc_IsHasCode(pcode)
        # print "------------ishascode", isHascode
        # if not isHascode:
        #     pcode = config.root_player_code # 临时先用这个，先写死
        # print "------------pcode", pcode
        log.debug(u'注册账号请求:account(%s)', account)
        if not account:
            return 0, errcode.EC_FORBID_STRING
        d = Game.store.query_loads(Player.DATA_CLS.TABLE_NAME, dict(account=account))
        if d:
            return 0, errcode.EC_NAME_REPEAT
        newTime = current_time()
        data = dict(account=account, password=password, base={"pcode":pcode, "isAgent":isAgent}, newTime=newTime)
        #try:
        rid = Game.store.insert(Player.DATA_CLS.TABLE_NAME, data)
        # if rid:
        #     # 生成个人邀请码
        #     Code = utility.activation_code(rid)
        #     print "注册生成个人邀请码:%s"%(Code)
        #     fakecode = Game.rpc_membtree_svr.rc_creatTreebyAdd(Code, rid, pcode)
        #     _base = {"pcode":pcode, "code":Code, "isAgent":isAgent, "fakecode":fakecode}
        #     Game.store.update(Player.DATA_CLS.TABLE_NAME, rid, dict(base=_base))
        #     # 修改关系链，如果 pcode 为空，默认挂在根节点上
        #     # print "resgin",Code, rid, pcode
        #     if pcode == '':
        #         print 'pcode is none'
        #     report.log_CreateRole_sql(rid, account, password, pcode, Code, newTime, isAgent)
        #except:
            #return 0, errcode.EC_NAME_REPEAT
        return 1, rid

    def rc_login(self, processor, account, password, fRoomID=0):
        """ 玩家登陆请求
        返回: isOk, error or sid
        """
        log.debug(u'用户登录请求:account(%s)', account)
        d = Game.store.query_loads(Player.DATA_CLS.TABLE_NAME, dict(account=account, password=password))
        # print "player login d:", d
        if not d:
            return 0, errcode.EC_LOGIN_ERR

        pid = d[0]['id'] # 玩家id
        rs, d = self._login(processor, pid, fRoomID)
        # print d

        if not rs:
            return rs, d
        self._acc2pid[account] = pid
        print "--------->>>>>rc_login:",rs, d
        return rs, d

    # 微信登陆
    def rc_wxlogin(self, processor, openID, sHead, sName, iGender, password=1):
        account = openID
        print ">>>>>account:", openID
        if not account:
            return 0, errcode.EC_FORBID_STRING
        d = Game.store.query_loads(Player.DATA_CLS.TABLE_NAME, dict(account=account))
        if d: # 已经有账号，直接登陆
            rs, data = self.rc_login(processor, account, password)
            return rs, data
        else: # 注册并登陆
            isSuccess, rid = self.rc_registerbyWX(account, password, sHead, sName, iGender)
            if isSuccess:
                rs, data = self.rc_login(processor, account, password)
                return rs, data
            else:
                return 0, errcode.EC_LOGIN_ERR

    # """点击微信分享链接"""
    def rc_loginWXbyLink(self, processor, openID, sHead, sName, iGender, fightRoom, pid, token, password=1):
        account = openID
        if not account:
            return 0, errcode.EC_FORBID_STRING
        if not fightRoom and pid and token:
            rs, d = self.rc_relogin(processor,pid,token) # 走重连
            return rs, d
        if fightRoom and pid and token: # 走重连 + 拉入房间
            rs, d = self.rc_relogin(processor,pid,token,fightRoom) # 走重连
            return rs, d
        # 如果都没有，或则有房间邀请号，走微信登陆
        d = Game.store.query_loads(Player.DATA_CLS.TABLE_NAME, dict(account=account))
        if d: # 已经有账号，直接登陆
            rs, data = self.rc_login(processor, account, password, fightRoom)
            return rs, data
        else: # 注册并登陆
            isSuccess, rid = self.rc_registerbyWX(account, password, sHead, sName, iGender)
            if isSuccess:
                rs, data = self.rc_login(processor, account, password, fightRoom)
                return rs, data
            else:
                return 0, errcode.EC_LOGIN_ERR


    def rc_registerbyWX(self, account, password, sHead='', sName='',iGender=0):
        """ 微信注册账号 """
        log.debug(u'注册账号请求:account(%s)', account)
        if not account:
            return 0, errcode.EC_FORBID_STRING
        d = Game.store.query_loads(Player.DATA_CLS.TABLE_NAME, dict(account=account))
        if d:
            return 0, errcode.EC_NAME_REPEAT
        newTime = current_time()
        data = dict(account=account, password=password, base={"wxID":account, "name":sName, "headPic":sHead, "gender":iGender}, newTime=newTime)
        #try:
        rid = Game.store.insert(Player.DATA_CLS.TABLE_NAME, data)
        return 1, rid


    def rc_relogin(self, processor, pid, token, fRoomID=0):
        """玩家重连"""
        notoken = self.notoken_cache.get(pid, 0)
        print "---rc_relogin----", processor, pid, token, notoken

        if not notoken:
            cache_token = self.relogin_cache.get(pid)
            if not cache_token:
                return 0, errcode.EC_LOGIN_ERR
            if cache_token != token:
                return 0, errcode.EC_LOGIN_ERR

        rs, d = self._relogin(processor, pid, fRoomID)
        if not rs:
            return rs, d
        if pid not in self.pid_login_waiter:
            waiter = Event()
            self.pid_login_waiter[pid] = waiter
            waiter.wait(200)
        return rs, d







    def rc_tokenLogin(self, processor, account, token):
        """玩家令牌登陆"""
        #先校验令牌有效性

        chn = 0

        if config.serverNo=="039999": #启用免登录验证，用于压力测试
            chn = 3
        else:
            request = utility.post(config.login_url, json=dict(uid=account, token=token, server_id=config.serverNo))
            task = spawn(request.send)
            gevent.joinall([task], timeout=3)

            try:
                respData = json.loads(request.response.content)
                request.response.close()
                request.session.close()
            except:
                return 0, errcode.EC_LOGIN_ERR

            rs = respData.get("success", 0)
            chn = respData.get("channel_id", 0)
            err = respData.get("err_msg", "")
            if not rs:
                Game.glog.log2File("rc_tokenLoginError", "%s|%s|%s|%s|%s" % (config.login_url, config.serverNo, account, token, err))
                return 0, errcode.EC_TOKEN_ERR

        # chn = 3

        d = Game.store.query_loads(Player.DATA_CLS.TABLE_NAME, dict(account=account))

        if not d:
            #白名单账号
            if account in ("exingame2", "surery123987"):
                data = dict(account=account, channel=chn, newTime=current_time(), gm=1)
            else:
                data = dict(account=account, channel=chn, newTime=current_time())
            try:
                _id = Game.store.insert(Player.DATA_CLS.TABLE_NAME, data)
                # d = Game.store.query_loads(Player.DATA_CLS.TABLE_NAME, dict(account=account))
                data['id'] = _id
                d = [data]
            except:
                return 0, errcode.EC_SAME_ACCOUNT
        if not d:
            return 0, errcode.EC_LOGIN_ERR
        # log.debug("%s", d)
        pid = d[0]['id']
        rs, d = self._login(processor, pid)
        if not rs:
            return rs, d
        if pid not in self.pid_login_waiter:
            waiter = Event()
            self.pid_login_waiter[pid] = waiter
            waiter.wait(200)
        return rs, d

#--------------------  业务流程end -------------------------------


class SubPlayerMgr(DictExport):
    """ 逻辑进程使用的角色管理类 """
    _rpc_name_ = 'rpc_sub_player_mgr'
    #定时保存时间 5分钟
    _SAVE_TIME_ = 60 #60 * 5
    _STAY_PROP_ = '_mgr_stay_time_'  # 玩家对象清理用

    max_logouts = config.logic_players
    max_logouts_times = 3600

    def __init__(self):
        self._keys = TimeMemCache(size=200, default_timeout=5*60, name='SubPlayerMgr._keys')
        self.others = TimeMemCache(size=100, default_timeout=(self._SAVE_TIME_-1), name='SubPlayerMgr.others')
        self.players = {}  # {pid: player}
        self.alls = {}  # {pid: player} (在线,离线) 所有玩家缓存,性能优化
        self.teamid2pid = {} #玩家组队id对应pid
        self._loop_task = None

    def setTeamid2pid(self,tid,pid):
        self.teamid2pid[tid]=pid

    def getTeamid2pid(self,tid):
        return self.teamid2pid.get(tid,0)

    def getSubPlayerMgrInfo(self):
        resp = {}
        resp["players"] = len(self.players)
        resp["alls"] = len(self.alls)
        resp["_keys"] = (len(self._keys._caches), len(self._keys._times), self._keys.size)
        return resp

    @property
    def count(self):
        return len(self.players)

    @property
    def len_offline(self):
        return len(self.alls) - len(self.players)

    @classmethod
    def cls_get_player_proxy(cls, pid, addr=None, local=1):
        if addr is None:
            addr = Game.app.get_addr()
        if local:
            proxy = DictItemProxy(cls._rpc_name_, dict_name='alls',
                key=pid, addr=addr)
        else:
            proxy = get_proxy_by_addr(addr, cls._rpc_name_, DictItemProxy)
            proxy.dict_name = 'alls'
            proxy.key = pid
        return proxy

    def start(self):
        self._loop_task = spawn(self._loop)

    def stop(self):
        if self._loop_task:
            self._loop_task.kill(block=False)
            self._loop_task = None
        #调用所有logout,并等待完成
        spawns(lambda u: u.logout(),
               [(u,) for u in self.players.itervalues()])

    def _loop(self):
        """ 定时保存等处理 """
        stime = 30
        logout_check_time = current_time()
        while 1:
            sleep(stime)
            try:
                p = None
                #定时保存
                for pid in self.players.keys():
                    p = self.players.get(pid)
                    if p is None or not p.logined:
                        log.error('[player_mgr]player(%s) in mgr.players, is None or not logined', pid)
                        self.players.pop(pid, None)
                        continue
                    try:
                        if p.save_time + self._SAVE_TIME_ <= time.time():
                            p.save()
                            p.save_task()
                            sleep(0.01)
                    except:
                        log.log_except()
                        self.players.pop(pid, None)
                del p
            except:
                log.log_except()

            #定时清理离线玩家缓存
            min_time_out, max_time_out = 2 * 60, 5 * 60  # 10分钟检查一次,
            ctime = current_time()
            if (self.len_offline > self.max_logouts and (ctime - logout_check_time >= min_time_out)) or \
                    (ctime - logout_check_time >= max_time_out):
                logout_check_time = ctime
                try:
                    self.logouts_clean()
                except:
                    log.log_except()

    def gw_open(self, processor):
        """ 新连接 """
        process_id = processor.pid
        p = self._keys.delete(process_id)
        if not p:
            processor.close_client()
            return
        # print "---------------2222---->>>> gw_open 0:",p
        # print "---------------2222---->>>> gw_open 1:",processor, processor.pid, processor.gwid
        # print "---------------2222---->>>> processor.pid 1:", processor.pid
        # print "---------------2222---->>>> gw_open 1:",processor, processor.pid, processor.gwid
        # if p.logined:  # 重连,下面假设一定成功
        #     p.reconnect(processor)
        #     return
        #登陆
        hd = PlayerRpcHandler()
        p.set_handler(hd, processor)
        wait_for_login_tag = p.wait_for_login()
        if wait_for_login_tag == 1:
            print "--------gw_open------1"
            self.load_player(p.id, p=p)
            self.add_player(p)
            p.login()
            Game.rpc_player_mgr.sub_login_finish(p.id, _no_result=1)
        elif wait_for_login_tag == 2:
            print "-----RELOGIN--->>"
            self.load_player(p.id, p=p)
            self.add_player(p)
            p.relogin()
            Game.rpc_player_mgr.sub_login_finish(p.id, _no_result=1)
        else:
            "--------gw_open------2"
            p.set_handler(None)
        import traceback
        traceback.print_stack()



    def player_login(self, process_id, pid, fRoomID=0):
        """ 玩家登陆,判断是否重连 """
        print "------------- Player_login --------------"
        if pid in self.players: # 顶号登陆
            print 111111111111111
            logout_player = self.players[pid]
            # if not logout_player.disconnected:
            #     print "logout_player.disconnected"
            #     log.warn(u'玩家(%s)重连异常,断开之前的连接', logout_player.id)
            #     logout_player.set_process(None)
        else: # 第一次登陆,或离线再次登陆
            print 2222222222222222
            logout_player = self.alls.get(pid, None)
            # print '-------------login 2',self.alls,logout_player
        p = Player.login_player(logout_player, pid)
        if fRoomID:
            p.setFriendRoomNo(fRoomID)
        self._keys.set(process_id, p)
        return dict(rid=p.id, have=1 if p.name else 0)

    def player_relogin(self, process_id, pid, fRoomID=0):
        """ 玩家登陆,判断是否重连 """
        print "------------- Player_login --------------"
        if pid in self.players: # 顶号登陆
            print 111111111111111
            logout_player = self.players[pid]
            # if not logout_player.disconnected:
            #     print "logout_player.disconnected"
            #     log.warn(u'玩家(%s)重连异常,断开之前的连接', logout_player.id)
            #     logout_player.set_process(None)
        else: # 第一次登陆,或离线再次登陆
            print 2222222222222222
            logout_player = self.alls.get(pid, None)
            # print '-------------login 2',self.alls,logout_player
        p =logout_player
        if not p:
            return {}
        p.setIsRelogin()
        if fRoomID:
            p.setFriendRoomNo(fRoomID)
        self._keys.set(process_id, p)
        return dict(rid=p.id, have=1 if p.name else 0)

    def load_player(self, pid, p=None):
        """ 加载玩家对象到alls
        @result:
            bool: 是否成功
        """
        # print "--------------","load player",pid
        if pid is None:
            # print '------------1'
            raise ValueError('pid is None')
        if pid in self.alls:
            # print '------load_player------2'
            if p is not None and self.alls[pid] != p:
                log.error('*******load_player: pid(%s) alls[pid](%s)<>player(%s)',
                        pid, id(self.alls[pid]), id(p))
            setattr(self.alls[pid], self._STAY_PROP_, current_time())
            # print '-----------load player------2 self.alls',self.alls
            return True
        if p is None:
            # print '------------3'
            p = Player.load_player(pid)
        if p is None:
            # print '------------4'
            return False
        self.alls[pid] = p
        setattr(self.alls[pid], self._STAY_PROP_, current_time())
        return True

    def add_player(self, player):
        """ 玩家进入游戏 """
        pid = player.id
        if pid is None:
            return
        rs = Game.rpc_player_mgr.add_player(Game.app.name, pid, player.name)
        if not rs:
            return False
        self.players[pid] = player
        log.debug('sub_player_mgr.add_player:%s', pid)
        return True

    def del_player(self, player):
        """ 玩家退出 """
        pid = player.data.id
        if pid not in self.players:
            return
        log.debug('sub_player_mgr.del_player:%s', pid)
        assert self.players[pid] == player, 'player != p'
        self.players.pop(pid)
        Game.rpc_player_mgr.del_player(Game.app.name, pid, player.relogin_token)
        Game.safe_pub(MSG_LOGOUT, player)

    def del_player_by_id(self, pid):
        """ 玩家退出,由全局管理器调用 """
        player = self.players.get(pid)
        if player is None:
            return
        player.logout()

    def clean_cache(self, pid):
        log.debug('alls.pop player(%s)', pid)
        p = self.alls.pop(pid, None)
        if p is None:
            return
        if not p.logout():
            # 清理出内存时,再确保保存一次,如月卡奖励,会延迟发送,在延迟后执行时玩家已经下线,attr的数据会修改了未保存
            p.save()
        p.uninit()
        return True

    def logouts_clean(self):
        """ 检查并清理离线缓存 """
        self.max_logouts = 500
        self.max_logouts_times = 10 * 60  # todo 测试用,减小player缓存时间,方便检查内存泄漏

        #对象缓存时长根据缓存量来确定
        n = self.len_offline / float(self.max_logouts)  # 缓存率
        times = int(max(self.max_logouts_times / n if n > 1 else self.max_logouts_times, 60))

        #过滤、排序离线玩家列表
        sorts = [(max(p.data.logoutTime, getattr(p, self._STAY_PROP_, 0)), p)
                for p in self.alls.itervalues() if p.id not in self.players]
        if not sorts:
            return
        sorts.sort(reverse=True)
        c = 0

        removes = []
        while sorts:
            check_time, p = sorts.pop(-1)
            if p.logined:
                continue
            pass_time = current_time() - check_time
            if pass_time >= times:  # 超时部分
                self.clean_cache(p.id)
                removes.append(p.id)
            elif len(sorts) > self.max_logouts:
                if pass_time >= 600:  # 超出部分,并且登陆退出超过n秒
                    self.clean_cache(p.id)
                    removes.append(p.id)
            else:
                break
            c += 1
            if c % 50 == 0:
                sleep(0.1)

        #通知全局管理器移除关联
        Game.rpc_player_mgr.remove_pids(removes)


    def get_player(self, pid):
        return self.players.get(pid)

    def get_player_in_all(self, pid):
        return self.alls.get(pid)

    def iter_players(self, pids=None):
        if pids is None:
            pids = self.players.keys()
        for pid in pids:
            p = self.players.get(pid)
            if p is None:
                continue
            yield pid, p

    # def broadcast(self, proto, data, exclude):
    #     for player in self.players.itervalues():
    #         if not exclude:
    #             spawn(player.call, proto, data, noresult=True)
    #         elif player.id not in exclude:
    #             spawn(player.call, proto, data, noresult=True)

    def broadcast(self, proto, data, exclude=[], keys=[]):
        Game.glog.log2File("testDebug", "keys 1|%s" % (keys))
        if not keys:
            Game.glog.log2File("testDebug", "keys 2|%s" % (keys))
            keys = self.players.keys()
        if not keys:
            Game.glog.log2File("testDebug", "keys 3|%s" % (keys))
            return
        for pid in exclude:
            keys.remove(pid)
        sendInfo = {}
        for pid in keys:
            Game.glog.log2File("testDebug", "keys 4|%s" % (pid))
            player = self.players.get(pid)
            if player:
                Game.glog.log2File("testDebug", "keys 5|%s" % (pid))
                processerInfo = player.getProcesserInfo()
                if processerInfo:
                    Game.glog.log2File("testDebug", "keys 6|%s" % (pid))
                    gwid, processerid, route_id, mid = processerInfo
                    group = sendInfo.setdefault(gwid, [])
                    group.append([processerid, route_id, mid])

        Game.gateway.broadcast(proto, data, sendInfo)



#---------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
from game.protocal.player import PlayerMgrrpcHandler, PlayerRpcHandler
