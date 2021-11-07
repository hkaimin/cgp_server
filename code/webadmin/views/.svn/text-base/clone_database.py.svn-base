#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from flask import request, jsonify, current_app as app
from flask.ext.admin import expose, BaseView

# 跳过不要复制的表名
SKIP_COLLECTIONS = (
    'system.indexes',
    'system.users',
    '_auto_inc_',
    'gconfig',
    'server',
    'pay_log',
    'pay_pre',
    'exchangecode',
)


class CloneDatabaseView(BaseView):
    html = 'dev/clone_database.html'

    def is_visible(self):
        return False

    def clone(self, source_id, target_id):
        source_db, target_db = self.prepare_clone(source_id, target_id)
        collection_names = self.get_clone_collection_names(source_db)
        self.execute_clone(source_db, target_db, collection_names)

    def prepare_clone(self, source_id, target_id):
        zoning = app.extensions['zoning']
        source_url = zoning.gamesvrs[source_id]['resource_db']
        target_url = zoning.gamesvrs[target_id]['resource_db']
        if source_url == target_url:
            raise StandardError('数据库地址相同')

        source_client = MongoClient(source_url)
        source_db = source_client.get_default_database()
        target_client = MongoClient(target_url)
        target_db = target_client.get_default_database()
        return source_db, target_db

    def get_clone_collection_names(self, source_db):
        names = []
        for name in source_db.collection_names():
            if name in SKIP_COLLECTIONS:
                continue
            names.append(name)
        return names

    def execute_clone(self, source_db, target_db, collection_names):
        for name in collection_names:
            source_collection = source_db[name]
            target_collection = target_db[name]
            target_collection.drop()
            for doc in source_collection.find():
                target_db[name].insert(doc)

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        zoning = app.extensions['zoning']
        current, candidates = zoning.current_and_candidate()
        return self.render(self.html,
                           current=current, candidates=candidates)

    @expose('/clone', methods=('POST', ))
    def clone_api(self):
        source_id = request.form.get('source', type=int)
        target_id = request.form.get('target', type=int)
        try:
            self.clone(source_id, target_id)
            success = True
            error = ''
        except StandardError as err:
            error  = str(err)
            success = False

        return jsonify(dict(success=success, error=error))
