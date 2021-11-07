#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from collections import OrderedDict
from StringIO import StringIO
from pprint import pprint
from pymongo import MongoClient
import xlrd
import xlwt

NAME_ROW = 0
FORMAT_ROW = 1
KEY_ROW = 2
DATA_START_ROW = 3

class Formater:

    @staticmethod
    def to_int(value):
        if isinstance(value, basestring):
            value = value.strip()
        if value == '':
            return 0
        else:
            try:
                return int(value)
            except:
                pass
            try:
                return int(float(value))
            except:
                return 0


    @staticmethod
    def to_float(value):
        if isinstance(value, basestring):
            value = value.strip()
        if value == '':
            return 0.0
        else:
            return float(value)

    @staticmethod
    def to_str(value):
        if isinstance(value, basestring):
            value = value.strip()
        return str(value)

    @staticmethod
    def to_json(value):
        if not isinstance(value, basestring):
            value = str(value)
        value = value.strip()
        if value == '':
            return None
        return json.loads(value)

    @staticmethod
    def to_int_in_list(value):
        value = str(value).strip()
        if value == '':
            return []
        return map(Formater.to_int, Formater.to_json(value))

    @staticmethod
    def to_str_int_of_dict(value):
        pass

    @staticmethod
    def get_func(type):
        mapping = {
            'int': Formater.to_int,
            'float': Formater.to_float,
            'str': Formater.to_str,
            'json': Formater.to_json,
            '[int]': Formater.to_int_in_list,
            '{str:int}': Formater.to_str_int_of_dict,
        }
        if type == '':
            raise StandardError('表格头为空，可能该列存在误填写了数据')
        if type not in mapping:
            raise StandardError('表格头必须是以下之一：%s' % mapping.keys())
        return mapping[type]

class XlsFile(object):

    def __init__(self, file_contents):
        self.file_contents = file_contents
        self.init()

    def init(self):
        self.init_meta()
        self.init_docs()

    def init_meta(self):
        # 默认使用第一个 sheet
        workbook = xlrd.open_workbook(file_contents=self.file_contents)
        sheet = workbook.sheet_by_index(0)
        names = sheet.row_values(NAME_ROW)

        # 初始化格式转换函数
        formats = sheet.row_values(FORMAT_ROW)
        formaters = map(Formater.get_func, formats)

        # 初始化要构造的 mongo doc 对象的 key 名
        # 第一列总是 id，但 mongo doc 中使用 _id
        keys = sheet.row_values(KEY_ROW)

        self.sheet = sheet
        self.names = names
        self.formats = formats
        self.formaters = formaters
        self.keys = keys
        self.keys_length = len(keys)

    def init_docs(self):

        def create_doc(values):
            formated_values = []
            col_errs = []
            for i, value in enumerate(values):
                formater = self.formaters[i]

                try:
                    formated_value = formater(value)
                except (ValueError, TypeError):
                    errcol = self.get_meta(i)
                    errcol.insert(0, i)
                    errcol.append(value)
                    col_errs.append(errcol)
                    continue

                formated_values.append(formated_value)

            doc_keys = self.keys[:]
            doc_keys[0] = '_id'
            doc = dict(zip(doc_keys, formated_values))
            return doc, col_errs

        docs = OrderedDict()
        errors = OrderedDict()

        # 读取每一行数据
        for i in xrange(DATA_START_ROW, self.sheet.nrows):
            # 读取有效的数据，
            # 忽略没有定义 key 名的列（这些列可能被策划当成注释用）
            values = self.sheet.row_values(i)
            values = values[:self.keys_length]

            doc, col_errs = create_doc(values)
            if col_errs:
                # 行数显示跟 office 软件中一致，从 1 开始
                errors[i + 1] = col_errs
            else:
                docs[doc['_id']] = doc

        self.docs = docs
        self.errors = errors

    def get_meta(self, col):
        return map(lambda l: l[col], (self.names, self.keys, self.formats))

    def diff(self, src_docs):
        ''' 和已有的 docs 比较 '''
        create = []
        update = []
        for id, doc in self.docs.iteritems():
            if doc['_id'] in src_docs:
                update.append(id)
            else:
                create.append(id)

        remove = []
        for src_id, src_doc in src_docs.iteritems():
            if src_doc['_id'] not in self.docs:
                remove.append(src_id)

        return dict(create=create, update=update, remove=remove)

class XlsCreator(object):

    def __init__(self, meta, docs):
        self.meta = meta
        self.docs = docs

        self.names = self.meta['names']
        self.formats = self.meta['formats']
        self.keys = self.meta['keys']

    @property
    def filebytes(self):

        def write_row(sheet, row, values):
            row_steam = sheet.row(row)
            for i, value in enumerate(values):
                row_steam.write(i, str(value))
            sheet.flush_row_data()

        workbook = xlwt.Workbook(encoding='utf-8')
        sheet = workbook.add_sheet('Sheet1')
        write_row(sheet, NAME_ROW, self.names)
        write_row(sheet, FORMAT_ROW, self.formats)
        write_row(sheet, KEY_ROW, self.keys)

        for i, doc in enumerate(self.docs):
            row = DATA_START_ROW + i
            value = self.get_ordered_values(doc)
            value = self.convert_to_excel_format(value)
            write_row(sheet, row, value)

        sheet.panes_frozen = True
        sheet.remove_splits = True
        sheet.vert_split_pos = 1
        sheet.vert_split_first_visible = 1
        sheet.horz_split_pos = DATA_START_ROW
        sheet.horz_split_first_visible = DATA_START_ROW
        sheet.panes_are_frozen = 1

        stream = StringIO()
        workbook.save(stream)
        return stream.getvalue()

    def convert_to_excel_format(self, value):
        for i, format in enumerate(self.formats):
            if format == 'json':
                value[i] = json.dumps(value[i])
        return value

    def get_ordered_values(self, doc):
        values = []
        keys = self.keys[:]
        keys[0] = '_id'
        for key in keys:
            if key in doc:
                values.append(doc[key])
            else:
                values.append('')
        return values

def main():
    if len(sys.argv) not in (2, 3):
        print 'usage: ./xls.py file.xls [res_name]'
        exit(1)

    filename = sys.argv[1]
    file_contents = open(filename, 'rb').read()
    xls = XlsFile(file_contents)

    if len(sys.argv) == 2:
        if xls.errors:
            print('Error:')
            pprint(xls.errors.items())
        else:
            print 'Pass.'
        return

    res_name = sys.argv[2]
    db = MongoClient('localhost', 27017)['rich_res']
    collection = db[res_name]
    if not xls.errors:
        src_docs = {doc['_id']: doc for doc in collection.find()}
        print 'Diff:'
        print xls.diff(src_docs)
        collection.drop()
        collection.insert(xls.docs.values())
        print 'Updated.'
    else:
        print 'Error:'
        pprint(xls.errors.items())
        print 'Aborted.'

if __name__ == '__main__':
    reload(sys);
    sys.setdefaultencoding('utf-8')
    main()

