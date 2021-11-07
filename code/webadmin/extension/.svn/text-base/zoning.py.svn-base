#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from flask import current_app as app
from time import time
from collections import OrderedDict
from pymongo import MongoClient
from flask import session


def safe_dburl(url):
    matches = re.findall('//.+@', url)
    if not matches:
        return url
    return url.replace(matches[0], '//', 1)


class Zoning(object):
    """ 游戏服务器组控制器 """

    @classmethod
    def share(cls):
        zoning = app.extensions['zoning']
        if 0:
            zoning = Zoning()
        return zoning

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.extensions['zoning'] = self
        self.init()

    def init(self):
        self.db_models = {}  # {db:{model:objects}}
        self.dbcache = {}  # {url: db}
        self.zones = OrderedDict()
        self.gamesvrs = OrderedDict()
        self.loaded_timestramp = 0
        self.reload()

    def system_db(self):
        connection = self.app.extensions['mongoengine'].connection
        db_name = self.app.config['MONGODB_SETTINGS']['db']
        return connection[db_name]

    def reload(self, force=False):
        db = self.system_db()

        # 初始化服务器组及其属性
        self.zones = OrderedDict()
        for zone in db['zone'].find():
            zone_id = int(zone['_id'])
            zone['_id'] = zone_id
            zone.setdefault('name','unnamed_%d' % zone_id)
            zone.setdefault('desc', '')

            zone['url'] = zone['resource_db']
            zone['title'] = '#%(_id)d %(name)s %(desc)s' % zone
            self.zones[zone_id] = zone

        # 初始化服务器及其属性
        self.gamesvrs = OrderedDict()
        for gamesvr in db['gamesvr'].find():
            gamesvr_id = int(gamesvr['_id'])
            gamesvr['_id'] = gamesvr_id
            gamesvr.setdefault('name', 'unnamed_%d' % gamesvr_id)
            gamesvr.setdefault('desc', '')
            gamesvr['zone'] = int(gamesvr['zone'])

            gamesvr['title'] = '#%(_id)d %(name)s %(desc)s' % gamesvr
            gamesvr['address'] = '%(host)s:%(port)s' % gamesvr
            gamesvr['safe_resource_db'] = safe_dburl(gamesvr['resource_db'])
            gamesvr['safe_user_db'] = safe_dburl(gamesvr['user_db'])
            gamesvr['safe_logging_db'] = safe_dburl(gamesvr['logging_db'])
            self.gamesvrs[gamesvr_id] = gamesvr

    def make_force_reselect(self):
        # 修改读取时间截，强制用户重新选择服务器

        self.loaded_timestramp = int(time())

    def auto_create_gamesvrs_from_running_server(self):
        # TODO 用线程获取

        ext = self.app.extensions['gamesvr']

        def fetch_servers(zone):
            try:
                client = MongoClient(zone['url'])
                default_db = client.get_default_database()
                servers = list(default_db['server'].find())
            except StandardError as error:
                print 'WARNNING: fetch servers in zone %s(%s) fail: %s' % (
                       zone['title'], zone['url'], error)
                return []
            finally:
                client.disconnect()

            for server in servers:
                server['resource_db'] = zone['resource_db']
                server['user_db'] = zone['user_db']
                server['logging_db'] = zone['logging_db']
                server['zone'] = zone['_id']
            return servers

        def fetch_server_config(server):
            try:
                config = ext.get_config(server['host'], server['port'])
            except StandardError as error:
                print 'WARNNING: fetch cofnig in server %s(%s:%s) fail: %s' % (
                       server['name'], server['host'], server['port'], error)
                return None
            return config

        def create_doc(i, server):
            return dict(
                _id=i,
                name=server['name'],
                desc='', # 有吗？
                host=server['host'],
                port=server['port'],
                resource_db=server['resource_db'],
                user_db=server['user_db'],
                logging_db=server['logging_db'],
                zone=server['zone']
            )
        # 从每个组的资源数据库读取服务器列表
        servers = []
        for zone in self.zones.itervalues():
            servers.extend(fetch_servers(zone))

        # 给每个 server 读取配置
        for server in servers:
            config = fetch_server_config(server)
            if config is not None:
                server['resource_db'] = config['db_engine_res']
                server['user_db'] = config['db_engine']
                server['logging_db'] = config['db_engine_log']

        # 创建 gamesvr 的 doc 并存到数据库
        collection = self.system_db()['gamesvr']
        for i, server in enumerate(servers, 1):
            doc = create_doc(i, server)
            collection.save(doc)

    # 数据库选择相关 { #

    def get_db_by_url(self, url):
        try:
            return self.dbcache[url]
        except KeyError:
            client = MongoClient(url)
            db = client.get_default_database()
            self.dbcache[url] = db
            db.db_url = url
            return db

    def get_resource_db(self, id):
        return self.get_db_by_url(self.gamesvrs[id]['resource_db'])

    def get_user_db(self, id):
        return self.get_db_by_url(self.gamesvrs[id]['user_db'])

    def get_logging_db(self, id):
        return self.get_db_by_url(self.gamesvrs[id]['logging_db'])

    def get_admin_db(self):
        connection = self.app.extensions['mongoengine'].connection
        db_cfg = self.app.config['MONGODB_SETTINGS']
        db_name = db_cfg['db']
        db = connection[db_name]
        if db_cfg.get('username'):
            db.authenticate(db_cfg['username'], db_cfg['password'])
        return db

    def switch_my_gamesvr(self, id):
        if id not in self.gamesvrs:
            raise StandardError('此服务器不存在')
        session['gamesvr'] = '%d:%d' % (self.loaded_timestramp, id)
        return self.gamesvrs[id]

    def my_gamesvr_id(self):
        try:
            value = session['gamesvr']
        except KeyError:
            return None

        try:
            timestramp, id = map(int, value.split(':', 1))
        except ValueError:
            return None

        if id not in self.gamesvrs \
                or timestramp != self.loaded_timestramp:
            del session['gamesvr']
            return None

        return id

    def my_gamesvr_status(self):
        try:
            value = session['gamesvr']
        except KeyError:
            return 1 # 没选择过

        try:
            timestramp, id = map(int, value.split(':', 1))
        except ValueError:
            return 1 # 数据结构不一致，当没选择过

        if id not in self.gamesvrs:
            del session['gamesvr']
            return 2 # 服务器不存在

        if timestramp != self.loaded_timestramp:
            del session['gamesvr']
            return 3 # 已经过期

        return 0

    def my_gamesvr(self):
        id = self.my_gamesvr_id()
        if id is None:
            return None
        return self.gamesvrs[id]

    def my_zone(self):
        gamesvr = self.my_gamesvr()
        if gamesvr is None:
            return None
        return self.zones[gamesvr['zone']]

    def my_resource_db(self):
        id = self.my_gamesvr_id()
        return self.get_resource_db(id)

    def my_user_db(self):
        id = self.my_gamesvr_id()
        return self.get_user_db(id)

    def my_logging_db(self):
        id = self.my_gamesvr_id()
        return self.get_logging_db(id)

    # 数据库选择相关 } #

    # 其它通用结构信息 { #

    def current_and_candidate(self):
        """ 返回当前选择的和候选的 """
        group_by_zone = {}
        for gamesvr in self.gamesvrs.itervalues():
            zone_id = gamesvr['zone']
            if zone_id not in group_by_zone:
                group_by_zone[zone_id] = []
            group_by_zone[zone_id].append(gamesvr)

        candidates = []
        for zone_id, gamesvrs in group_by_zone.iteritems():
            candidate = dict(
                zone=self.zones[zone_id],
                gamesvrs=sorted(gamesvrs, key=lambda g: g['_id'])
            )
            candidates.append(candidate)

        my_gamesvr = self.my_gamesvr()
        if my_gamesvr is not None:
            current = dict(
                zone=self.my_zone(),
                gamesvr=my_gamesvr
            )
        else:
            current = None
        return current, candidates

    def get_zone_by_svid(self, svid):
        return self.gamesvrs[svid]['zone']

    def get_curren_zone(self):
        svrid = self.my_gamesvr_id()
        return self.gamesvrs[svrid]['zone']

    def get_server_list_by_zone(self, zone):
        rs = []
        for k, v in self.gamesvrs.iteritems():
            if v['zone'] == zone:
                v['id'] = k
                rs.append(v)
        return rs

    def get_curren_server_list(self):
        zone = self.get_curren_zone()
        return self.get_server_list_by_zone(zone)

    def get_model_objects(self, model):
        """ 获取当前用户选择的库的model.objects """
        db = model._get_db()
        if db in self.db_models and model in self.db_models[db]:
            return self.db_models[db][model]
        models = self.db_models.setdefault(db, {})
        from mongoengine.queryset import QuerySetManager
        model._collection = None  # hack:清理缓存
        model.objects = QuerySetManager()
        # models[model] = model.objects  # 不能缓存,否则插入、更新不能及时反映到页面
        return model.objects

    def clean_model_cache(self, model):
        """ 清理 """
        db = model._get_db()
        if db in self.db_models and model in self.db_models[db]:
            return self.db_models[db].pop(model)


#------------------------
#------------------------
#------------------------
