#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from flask import session


class Guard(object):
    """ 权限控制器 """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.extensions['guard'] = self
        self.init()

    def init(self):
        self.users = {}
        self.groups = {}
        self.reload()

    def system_db(self):
        connection = self.app.extensions['mongoengine'].connection
        db_cfg = self.app.config['MONGODB_SETTINGS']
        db_name = db_cfg['db']
        db = connection[db_name]
        if db_cfg.get('username'):
            db.authenticate(db_cfg['username'], db_cfg['password'])
        return db

    def reload(self):
        db = self.system_db()

        # 初始化用户组及其属性
        self.groups = {}
        for group in db['group'].find():
            group_id = int(group['_id'])
            group['_id'] = group_id
            group.setdefault('name','用户组 %d' % group_id)
            group.setdefault('note','')
            group.setdefault('permissions', [])
            self.groups[group_id] = group

        # 初始化用户及其属性
        self.users = {}
        for user in db['user'].find():
            user_id = int(user['_id'])
            user['_id'] = user_id
            user.setdefault('name','unnamed_%d' % user_id)
            user.setdefault('password','whynopassword')
            user.setdefault('groups', [])
            # 去除不存在的用户组ID
            user['groups'] = filter(lambda i: i in self.groups,
                                    map(int, user['groups']))
            self.users[user_id] = user

    def get_user_by_auth(self, username, password):
        for user in self.users.itervalues():
            if user['name'] == username and user['password'] == password:
                return user
        return None

    def get_groups_by_user_id(self, user_id):
        group_ids = self.users[user_id]['groups']
        return map(lambda i: self.groups[i], group_ids)

    def get_permission_details_by_names(self, pms_names):
        details = []
        for pms_name in pms_names:
            func_name = 'pms_' + pms_name
            if not hasattr(self, func_name):
                continue
            doc = getattr(self, func_name).__doc__
            title, desc = map(str.strip, doc.split('\n', 1))
            details.append((pms_name, title, desc))
        details.sort()
        return details

    def get_permission_details(self, user_id):
        user_id = session['user_id']
        if self.is_super_user(user_id):
            pms_names = self.defined_permissions()
        else:
            pms_names = self.get_permissions_for_user(user_id)
        return self.get_permission_details_by_names(pms_names)

    def get_all_permission_details(self):
        pms_names = self.defined_permissions()
        return self.get_permission_details_by_names(pms_names)

    def get_permission_details_by_group(self, group_id):
        group = self.groups[group_id]
        return self.get_permission_details_by_names(group['permissions'])

    def get_group_members(self, group_id):
        members = {}
        for user in self.users.itervalues():
            if group_id in user['groups']:
                members[user['_id']] = user
        return members

    def is_super_user(self, user_id):
        return user_id == 1

    def iam_super_user(self):
        return self.is_super_user(session['user_id'])

    def my_name(self):
        return self.users[session['user_id']]['name']

    def my_group_names(self):
        groups = self.get_groups_by_user_id(session['user_id'])
        return [group['name'] for group in groups]

    def my_permission_details(self):
        return self.get_permission_details(session['user_id'])

    def defined_permissions(self):
        names = []
        for key in dir(self):
            if key.startswith('pms_'):
                names.append(key[4:])
        return names

    def get_permissions_for_user(self, user_id):
        groups = self.get_groups_by_user_id(user_id)
        permissions = []
        for group in groups:
            permissions.extend(group['permissions'])
        return set(permissions)

    def change_user_password(self, user_id, new_password):
        user = self.users[user_id]
        user['password'] = new_password
        self.system_db()['user'].save(user)

    def allow(self, user_id, *pms_names):
        """ 是否允许某个权限组 """
        if user_id is None:
            return False
        if self.is_super_user(user_id):
            return True

        permissions = self.get_permissions_for_user(user_id)
        for pms_name in pms_names:
            if pms_name in permissions:
                return True
        return False

    def allow_me(self, *pms_names):
        return self.allow(session.get('user_id', None), *pms_names)

    def allow_endpoint(self, user_id, endpoints, path=None, method=None):
        """ 是否允许某个 endpoint """
        if self.is_super_user(user_id):
            return True

        permissions = self.get_permissions_for_user(user_id)
        if '*' in permissions:  # 所有权限
            return True
        # pms_null_func = lambda x: False
        for pms_name in permissions:
            if path and '/' in pms_name:
                if re.search(pms_name, path):
                    return True
            func = getattr(self, 'pms_' + pms_name, None)
            if func:
                for endpoint in endpoints:
                    if func(endpoint):
                        return True
        #检查前缀是否匹配
        for endpoint in endpoints:
            names = endpoint.split('.', 1)
            if names[0] in permissions:
                return True
        return False

    def allow_endpoint_me(self, endpoints, path=None, method=None):
        return self.allow_endpoint(session['user_id'], endpoints, path=path, method=method)

    # 这里定义权限组 #

    # TODO 待细分，暂时区别读取和写入两种操作
    model_read_views = ('index', 'index_view', 'download_view')
    model_write_views = ('create_view', 'edit_view',
                         'delete_view', 'upload_view',
                         'action_view', 'ajax_lookup', 'api_file_view')

    def pms_resource_model_read(self, endpoint):
        """ 游戏资源表 - 读取

        对游戏资源表进行查看、查找、下载操作。
        """

        if not endpoint.startswith('resource_model_'):
            return False
        view_name = endpoint.split('.')[-1]
        return view_name in self.model_read_views

    def pms_resource_model_write(self, endpoint):
        """ 游戏资源表 - 修改

        对游戏资源表进行创建、编辑、删除、上传操作。
        """

        if not endpoint.startswith('resource_model_'):
            return False
        view_name = endpoint.split('.')[-1]
        return view_name in self.model_write_views

    def pms_user_model_read(self, endpoint):
        """ 用户数据表 - 读取

        对用户数据表进行查看、查找操作。
        """

        if not endpoint.startswith('user_model_'):
            return False
        view_name = endpoint.split('.')[-1]
        return view_name in self.model_read_views

    def pms_user_model_write(self, endpoint):
        """ 用户数据表 - 修改

        对用户数据表进行创建、编辑、删除操作。
        """

        if not endpoint.startswith('user_model_'):
            return False
        view_name = endpoint.split('.')[-1]
        return view_name in self.model_write_views

    def pms_logging_model_read(self, endpoint):
        """ 日志数据表 - 读取

        对日志数据表进行查看、查找操作。
        """

        if not endpoint.startswith('logging_model_'):
            return False
        view_name = endpoint.split('.')[-1]
        return view_name in self.model_read_views

    def pms_logging_model_write(self, endpoint):
        """ 日志数据表 - 修改

        对日志数据表进行创建、编辑、删除操作。
        """

        if not endpoint.startswith('logging_model_'):
            return False
        view_name = endpoint.split('.')[-1]
        return view_name in self.model_write_views

    # def pms_mapeditor(self, endpoint):
    #     """ 地图编辑器
    #
    #     使用地图编辑器修改地图
    #     """
    #     return endpoint.startswith('mapeditor.')
    #
    # def pms_cache_control(self, endpoint):
    #     """ 缓存数据
    #
    #     查看 Redis 数据库使用情况
    #     """
    #
    #     return endpoint.startswith('cache_control')
    #
    # def pms_clone_database(self, endpoint):
    #     """ 复制数据库
    #
    #     复制游戏资源数据库
    #     """
    #
    #     return endpoint.startswith('clone_database')
    #
    # def pms_release_version(self, endpoint):
    #     """ 发布版本
    #
    #     创建游戏资源新版本
    #     """
    #     return endpoint.startswith('release_version.')
    #
    # def pms_reward_test(self, endpoint):
    #     """ 奖励测试
    #
    #     使用奖励测试页面
    #     """
    #     return endpoint.startswith('reward_test')
    #
    # def pms_ai_test(self, endpoint):
    #     """ AI 测试
    #
    #     使用 AI 测试页面
    #     """
    #
    #     return endpoint.startswith('ai_test')
    #
    # def pms_simulate_fight(self, endpoint):
    #     """ 战斗模拟
    #
    #     使用战斗模拟页面
    #     """
    #     return endpoint.startswith('simulate_fight')
    #
    # def pms_statistic(self, endpoint):
    #     """ 统计信息
    #
    #     查看各种统计信息
    #     """
    #
    #     return endpoint.startswith('statistic')

    def pms_admin_control(self, endpoint):
        """ 管理后台

        使用后台的控制面板，进行修改用户和用户组
        """
        return endpoint.startswith('ctr.') or \
               endpoint.startswith('system_summary.') or \
               endpoint.startswith('system_guard.') or \
               endpoint.startswith('system_zoning.') or \
               endpoint.startswith('system_user.') or \
               endpoint.startswith('system_group.') or \
               endpoint.startswith('system_model_')
