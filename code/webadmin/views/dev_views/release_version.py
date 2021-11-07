#!/usr/bin/env python'
# -*- coding: utf-8 -*-

import os
from os.path import exists
import hashlib
import shutil
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED
# from StringIO import StringIO
from cStringIO import StringIO
import json

from flask import (request, redirect, flash, abort, jsonify,
                   url_for, make_response, current_app as app)
from flask.ext.admin import expose, BaseView
from webadmin.models.resource import models as res_models
from webadmin.library.jze_handle import JzeFile, JzeCreator

readable_time = lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')


db_pre = '.db'
dbe_pre = '.dbe'  # 压缩加密数据库文件
data_pre = '.data'
dump_pre = '.dump'
deletes = [db_pre, data_pre, dump_pre, dbe_pre]


def change_id(docs):
    new_docs = []
    for doc in docs:
        doc['id'] = doc['_id']
        del doc['_id']
        new_docs.append(doc)
    return docs


def wrap_with_id(docs):
    entries = {}
    for doc in docs:
        key = doc['id']
        entries[key] = doc
    return entries


class ReleaseVersionView(BaseView):
    html = 'dev/release_version.html'

    def is_visible(self):
        return False

    def resource_db(self):
        zoning = app.extensions['zoning']
        return zoning.my_resource_db()

    @classmethod
    def res_path(cls):
        zoning = app.extensions['zoning']
        subdir = zoning.my_zone()['name']
        rootdir = os.path.abspath(app.config['RES_VERSION_PATH'])
        finaldir = os.path.join(rootdir, subdir)
        return finaldir

    @property
    def parent_path(self):
        finaldir = os.path.join(self.res_path(), 'ver')
        return finaldir

    @property
    def http_path(self):
        db = self.resource_db()
        path = db['gconfig'].find_one(dict(key='dbPath'))
        if not path:
            return ''

        value = path['value']
        if value.endswith('/'):
            value = value[:-1]
        return value

    def get_filename(self, _id, pre):
        return os.path.join(self.parent_path, str(_id)) + pre

    def generate_id(self):
        db = self.resource_db()
        doc = db['gconfig'].find_one(dict(key='dbVer'))
        if doc:
            return int(doc['value']) + 1
        else:
            return 1

    def db_update_id(self, id):
        id = int(id)
        db = self.resource_db()
        collection = db['gconfig']
        doc = collection.find_one(dict(key='dbVer'))
        if doc:
            collection.save({'_id': doc['_id'], 'key': 'dbVer', 'value': id})

    def db_update_hash(self, hash):
        db = self.resource_db()
        collection = db['gconfig']
        doc = collection.find_one(dict(key='dbHash'))
        if doc:
            collection.save({'_id': doc['_id'], 'key': 'dbHash', 'value': hash})

    def archive_as_zip(self, zip_entries):
        stream = StringIO()
        with ZipFile(stream, 'w', compression=ZIP_DEFLATED) as zip_file:
            for filename, filebytes in zip_entries:
                zip_file.writestr(filename, filebytes)
        return stream.getvalue()

    def get_jze_data(self, filename):
        with open(filename) as file:
            zipdata = file.read()
        return zipdata

    def get_json_data(self, filename):
        zip_entries = []
        with ZipFile(filename) as zip_file:
            for filename in zip_file.namelist():
                filebytes = zip_file.read(filename)
                data = JzeFile(filebytes).json_string
                data = data.decode('unicode_escape')
                zip_entries.append((filename, data))
        return self.archive_as_zip(zip_entries)

    def filter_saved_ids(self, folder):
        ids = []
        for filename in os.listdir(folder):
            if not filename.endswith(db_pre):
                continue
            ids.append(filename[:-len(db_pre)]) # id.data -> id
        ids.sort()
        ids.reverse()
        return ids

    def _get_collections(self, is_dict=False, excludes=None):
        from webadmin.views.clone_database import SKIP_COLLECTIONS
        if excludes is None:
            excludes = []
        excludes.extend(SKIP_COLLECTIONS)
        if not is_dict:
            names = map(lambda x: x._meta['collection'], res_models)
            map(names.remove, [e for e in excludes if e in names])
        else:
            names = dict((x._meta['collection'], x) for x in res_models)
            map(names.pop, [e for e in excludes if e in names])
        return names

    def make_version(self, _id):

        db = self.resource_db()

        def general_entries(names):
            entries = []
            for name in names:
                docs = list(db[name].find())
                docs = wrap_with_id(change_id(docs))
                creator = JzeCreator(docs)
                entry = (name, creator.filebytes)
                entries.append(entry)
            return entries

        def tile_entries():
            """ 地格特殊处理，按地图ID 分组 """
            docs = list(db['tile'].find())
            docs = change_id(docs)
            tiles = {}
            for doc in docs:
                mid = doc['mid']
                if mid not in tiles:
                    tiles[mid] = []
                tiles[mid].append(doc)
            creator = JzeCreator(tiles)
            entry = ('tile', creator.filebytes)
            return entry

        general_collection_names = self._get_collections(excludes=['tile'])
        zip_entries = []
        zip_entries.extend(general_entries(general_collection_names))
        zip_entries.append(tile_entries())

        filename = self.get_filename(_id, data_pre)
        zipdata = self.archive_as_zip(zip_entries)
        with open(filename, 'wb') as file:
            file.write(zipdata)
        hash = hashlib.md5(zipdata).hexdigest()
        return hash

    def make_sqlite3(self, _id):
        """ 创建sqlite3数据库 """
        from webadmin.library.sqlite3_handle import Sqlite3Creator
        db = self.resource_db()
        tables = self._get_collections(is_dict=1)
        filename = self.get_filename(_id, db_pre)
        sqlite3 = Sqlite3Creator(filename)
        try:
            for tname, define in tables.iteritems():
                docs = list(db[tname].find())
                docs = wrap_with_id(change_id(docs))
                docs = docs.values()
                sqlite3.add_table(tname, define, docs)
        finally:
            sqlite3.close()
        data, old = sqlite3.encrypt()
        #md5:使用原始文件的md5,注意恢复数据库也会生成md5，需要一致
        hash = hashlib.md5(old).hexdigest()
        f = self.get_filename(_id, dbe_pre)
        with open(f, 'wb') as f:
            f.write(data)

        return hash

    def make_dump(self, _id):
        """ 备份数据库 """
        from store.driver import get_driver
        db = self.resource_db()
        filename = self.get_filename(_id, dump_pre)
        store = get_driver(db.db_url)
        store.dump(filename)

    def restore(self, _id):
        """ 恢复数据库 """
        from store.driver import get_driver
        db = self.resource_db()
        filename = self.get_filename(_id, dump_pre)
        store = get_driver(db.db_url)
        store.restore(filename)
        #更新数据库版本号, 原始文件的md5值,注意和上面版本生成时的一致
        with open(self.get_filename(_id, db_pre), 'rb') as f:
            data = f.read()
        hash = hashlib.md5(data).hexdigest()
        self.db_update_id(_id)
        self.db_update_hash(hash)
        # flash(u'版本 %s 已恢复' % _id, 'success')

    def database_info(self):
        db = self.resource_db()
        connection = db.connection
        info = {
            'host': connection.host,
            'port': connection.port,
            'database': db.name,
        }
        return info

    def new_backup(self):
        """ 创建新版本 """
        self.update_cfg()
        _id = self.generate_id()
        hash = self.make_version(_id)
        hash = self.make_sqlite3(_id)
        self.make_dump(_id)
        self.db_update_id(_id)
        self.db_update_hash(hash)
        flash(u'新的版本 %s 已创建' % _id, 'success')
        return redirect(url_for(request.endpoint))

    def update_cfg(self):
        """ 更新配置文件 """
        print('****update_cfg:server.list, apk_channel.list**************')
        db = self.resource_db()
        gconfig_tb = db.gconfig
        server_tb = db.server

        def _get_config(key):
            rs = gconfig_tb.find({'key': key})
            if rs.count():
                return rs[0]['value']

        minVer = _get_config('minVer')
        apk_channel_url = _get_config('apk_channel_url')
        app_strore_url = _get_config('app_strore_url')
        default_apk_channel = _get_config('default_apk_channel')
        default_apk_url = _get_config('default_apk_url')
        servers = list(server_tb.find())
        servers.sort(key=lambda s: s['_id'])
        lt = []
        for svr in servers:
            gws = json.loads(svr['gw'])
            for gw in gws:
                lt.append('%s %s %s:%s %s:%s %s %s %s %s\n' % (
                    svr["_id"],
                    svr["name"],
                    gw[0], gw[1],
                    svr["host"],
                    svr["port"],
                    svr["package_version"],
                    minVer, apk_channel_url, app_strore_url
                ))

        parent_path = os.path.dirname(self.parent_path)
        path = os.path.join(parent_path, "server.list")
        with open(path, 'wb') as f:
            f.write(''.join(lt))
        path = os.path.join(parent_path, "apk_channel.list")
        with open(path, 'wb') as f:
            f.write("%s %s" % (default_apk_channel, default_apk_url))

        return redirect(url_for(request.endpoint))

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        if request.method == 'POST':
            action = request.form['action']
            func = getattr(self, action)
            return func()

        parent_path = self.parent_path
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)

        ids = self.filter_saved_ids(parent_path)
        files = []
        for id in ids:
            filename = self.get_filename(id, db_pre)
            zip_fn = self.get_filename(id, dbe_pre)
            if not exists(zip_fn):
                continue
            with open(zip_fn) as file:
                zipdata = file.read()
                hash = hashlib.md5(zipdata).hexdigest()
            create_time = os.path.getctime(filename)
            files.append([id, hash, create_time])
        files.sort(key=lambda f: int(f[0]), reverse=True)
        for file in files:
            file[2] = readable_time(file[2])

        info = self.database_info()
        return self.render(self.html,
                           info=info,
                           files=files,
                           http_path=self.http_path,
                           parent_path=self.parent_path)

    @expose('/download/', methods=('GET', ))
    def download_view(self):
        id = request.args['id']
        type = request.args['type']


        if type == 'jze':
            filename = self.get_filename(id, db_pre)
            if not os.path.isfile(filename):
                abort(404)
            resp_body = self.get_jze_data(filename)
        else:  # json
            filename = self.get_filename(id, data_pre)
            if not os.path.isfile(filename):
                abort(404)
            resp_body = self.get_json_data(filename)

        #hash = hashlib.md5(resp_body).hexdigest()

        resp = make_response(resp_body)
        filename = 'v%s.%s.zip' % (id, type)
        if request.user_agent.browser == 'msie':
            filename_header = 'attachment; filename="%s";' % filename
        else:
            filename_header = "attachment; filename*=GBK''%s;" % filename
        resp.headers['Content-Disposition'] = filename_header
        resp.mimetype = 'application/zip'
        return resp

    @expose('/delete/', methods=('POST', ))
    def delete_api(self):
        id = request.form['id']
        success = True

        def _del(filename):
            try:
                if os.path.isdir(filename):
                    shutil.rmtree(filename)
                else:
                    os.remove(filename)
                return True
            except (IOError, OSError):
                pass
            return False
        for d in deletes:
            _del(self.get_filename(id, d))
        return jsonify(success=success)

    @expose('/restore/', methods=('POST', ))
    def restore_api(self):
        """ 恢复特定版本资源数据库 """
        id = request.form['id']
        success = True
        self.restore(id)
        return jsonify(success=success)


