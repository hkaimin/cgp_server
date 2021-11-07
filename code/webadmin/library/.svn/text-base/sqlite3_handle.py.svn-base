#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sqlite3
import traceback
import json

from mongoengine import IntField, FloatField, BooleanField, StringField, DynamicField
from mongoengine.base import BaseField
from webadmin.library import mongoengine_fields as f

import zlib
from rd1sdk import aes
AES_KEY = 'xf3R0xdcmx8bxc0J'
encrypter = aes.new_aes_encrypt(AES_KEY)
decrypter = aes.new_aes_decrypt(AES_KEY)


SQL_TYPES = {
    IntField: 'INTEGER',
    FloatField: 'REAL',
    BooleanField: 'BOOLEAN',
    StringField: 'VARCHAR(255)',
    DynamicField: 'TEXT',
    f.IntListField: 'VARCHAR(255)',
    f.PointField: 'VARCHAR(255)',
}


class Sqlite3Creator(object):
    def __init__(self, db_file):
        if os.path.exists(db_file):
            os.remove(db_file)
        self.db_file = db_file
        print("Sqlite3Creator:%s" % db_file)
        self.db = sqlite3.connect(db_file)

    def add_table(self, tname, define, docs):
        """
        @params:
            define: Document class:  see models\resource.py
            docs: dict
        """
        #建表,建索引
        fields = []
        indexs = None
        for name, mf in define.__dict__.iteritems():
            if name == 'indexs':
                indexs = mf
                continue
            elif name == 'id':
                continue
            elif not isinstance(mf, BaseField):
                continue
            fields.append(dict(name=name, type=SQL_TYPES[mf.__class__]))
        self._new_table(tname, fields, indexs)

        #添加内容
        self._add_docs(tname, fields, docs)
        self.db.commit()

    def _new_table(self, name, fields, indexs):
        """ 建表、建索引 """
        sql = 'create table %s (id integer primary key,' % name
        for field in fields:
            sql += '"%(name)s" %(type)s,' % field
        sql = sql[:-1] + ');'
        sql_indexs = []
        if indexs:
            for i in indexs:
                sql_indexs.append('CREATE INDEX IF NOT EXISTS idx_%(name)s ON %(tname)s (%(name)s);' % dict(
                    name=i, tname=name,
                ))
        c = self.db.cursor()
        c.execute(sql)
        if indexs:
            c.execute('\n'.join(sql_indexs))
        self.db.commit()

    def _dump_value(self, v, encode=None):
        if isinstance(v, unicode):
            return v if encode is None else v.encode(encode)
        if isinstance(v, (int, float, str)):
            return v
        return json.dumps(v, ensure_ascii=False)

    def _add_docs(self, tname, fields, docs):
        """ 写入内容 """
        sql = 'insert into %s values(%s);' % (tname, ('?,'*(len(fields)+1))[:-1])
        c = self.db.cursor()
        for doc in docs:
            values = [doc['id']]
            try:
                for f in fields:
                    v = doc.get(f['name'], None)
                    values.append(self._dump_value(v))
                c.execute(sql, values)
            except:
                traceback.print_exc()
                raise
        self.db.commit()

    def close(self):
        self.db.close()

    def encrypt(self):
        """ 压缩加密 """
        with open(self.db_file, 'rb') as f:
            old = f.read()
        data = zlib.compress(old, 6)
        # data = encrypter(data)
        return data, old

