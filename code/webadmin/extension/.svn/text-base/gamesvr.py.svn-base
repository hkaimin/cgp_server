#!/usr/bin/env python
# -*- coding: utf-8 -*-

from grpc import get_proxy_by_addr


class Gamesvr(object):
    """ 和游戏服务器交互的类 """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.extensions['gamesvr'] = self
        self.init()

    def init(self):
        pass

    def get_server(self, host, port):
        port = int(port) #TODO(prim) port type is float temp fix
        # 默认是游戏端口减1
        rpc_port = port - 1
        if host == '' or port < 1:
            return None
        server = get_proxy_by_addr([host, rpc_port], 'rpc_client')
        if 0:
            from game.client.client_api import ClientApi
            server = ClientApi()
        return server

    def simulate_fight(self, host, port, args):
        """ 战斗模拟 """
        server = self.get_server(host, port)
        return server.simulate_fight(**args)

    def ctrl_svr(self, host, port, **kw):
        server = self.get_server(host, port)
        return server.ctrl_svr(**kw)

    def reward_test(self, host, port, reward, params, rewardid, pid):
        """  奖励测试 """
        server = self.get_server(host, port)
        return server.reward_test(reward_text=reward, params_text=params, reward_id=rewardid, pid=pid)

    def mail_test(self, host, port, *args, **kw):
        """ 邮件测试 """
        server = self.get_server(host, port)
        return server.mail_test(*args, **kw)

    def run_code(self, host, port, pid, code):
        """ 邮件测试 """
        server = self.get_server(host, port)
        return server.run_code(pid, code)

    def ai_test(self, host, port, pid, aid, param):
        """  命运测试 """
        server = self.get_server(host, port)
        return server.ai_test(pid=pid, aid=aid, param=param)

    def get_config(self, host, port):
        """ 获取游戏服务器配置信息 """
        server = self.get_server(host, port)
        return server.get_config()

    def add_coin(self, host, port, pid, coin1=0, coin2=0):
        """ 添加金币,幸运星 """
        if not (coin1 or coin2):
            return
        svr = self.get_server(host, port)
        return svr.add_coin(coin1=coin1, coin2=coin2)

    def get_online_plist(self, host, port):
        svr = self.get_server(host, port)
        return svr.get_online_plist()

    def get_online_room_player(self, host, port, pid):
        svr = self.get_server(host, port)
        if not svr:
            return None
        return svr.get_online_room_player(pid)

    def add_online_hero_property(self, host, port, pid, key, value):
        svr = self.get_server(host, port)
        if not svr:
            return None
        return svr.add_online_hero_property(pid, key, value)

    def update_online_hero_property(self, host, port, pid, key, value):
        svr = self.get_server(host, port)
        if not svr:
            return None
        return svr.update_online_hero_property(pid, key, value)

    def set_online_hero_pos(self, host, port, pid, pos):
        svr = self.get_server(host, port)
        if not svr:
            return None
        return svr.set_online_hero_pos(pid, pos)

    def set_online_hero_dice(self, host, port, pid, dice):
        svr = self.get_server(host, port)
        if not svr:
            return None
        return svr.set_online_hero_dice(pid, dice)

    def add_online_hero_card(self, host, port, pid, card):
        svr = self.get_server(host, port)
        if not svr:
            return None
        return svr.add_online_hero_card(pid, card)

    # p1 opertion
    #=========================================================================
    def block(self, host, port, pid, time):
        svr = self.get_server(host, port)
        if svr:
            return svr.block([pid])

    def unblock(self, host, port, pid):
        svr = self.get_server(host, port)
        if svr:
            return svr.unblock([pid])

    def is_block(self, host, port, pid):
        svr = self.get_server(host, port)
        if svr:
            return svr.is_block([pid])

    def kick_player(self, host, port, pid):
        svr = self.get_server(host, port)
        if svr:
            return svr.kick_player([pid])

    def set_name(self, host, port, pid, name):
        svr = self.get_server(host, port)
        if svr:
            return svr.set_name([pid], [name])

    def limit_speak(self, host, port, pid, time):
        svr = self.get_server(host, port)
        if svr:
            return svr.limit_speak([pid], [time])

    def unlimit_speak(self, host, port, pid):
        svr = self.get_server(host, port)
        if svr:
            return svr.unlimit_speak([pid])

    def limit_speak_speed(self, host, port, pid, last_time, interval):
        svr = self.get_server(host, port)
        if svr:
            return svr.limit_speak_speed(pid, last_time, interval)

    def add_coin1(self, host, port, pid, coin1, reason):
        svr = self.get_server(host, port)
        if svr:
            return svr.add_coin1(pid, coin1, reason)

    def add_coin2(self, host, port, pid, coin2, reason):
        svr = self.get_server(host, port)
        if svr:
            return svr.add_coin2(pid, coin2, reason)

    def cost_coin1(self, host, port, pid, coin1, reason):
        svr = self.get_server(host, port)
        if svr:
            return svr.cost_coin1(pid, coin1, reason)

    def cost_coin2(self, host, port, pid, coin2, reason):
        svr = self.get_server(host, port)
        if svr:
            return svr.cost_coin2(pid, coin2, reason)

    def add_game_objs(self, host, port, pid, type, id, amount):
        svr = self.get_server(host, port)
        if svr:
            return svr.add_game_objs(pid, type, id, amount)

    def del_game_objs(self, host, port, pid, type, id, amount):
        svr = self.get_server(host, port)
        if svr:
            return svr.del_game_objs(pid, type, id, amount)

    def is_online(self, host, port, pid):
        svr = self.get_server(host, port)
        if svr:
            return svr.is_online(pid)

    def query_player_info(self, host, port, pid):
        svr = self.get_server(host, port)
        if svr:
            return svr.query_player_info(pid)

    def send_mail(self, host, port, pid, title, content):
        """ 邮件测试 """
        svr = self.get_server(host, port)
        if svr:
            return svr.send_mail(pid, title, content)

    def announcement(self, host, port, msg):
        svr = self.get_server(host, port)
        if svr:
            return svr.announcement([msg])


