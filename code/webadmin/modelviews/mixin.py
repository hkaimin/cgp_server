#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, flash, redirect, url_for, make_response
from flask.ext.admin import expose
from webadmin.library.xls_handle import XlsFile, XlsCreator

format_mapping = {
    'IntField': 'int',
    'FloatField': 'float',
    'StringField': 'str',
    'DynamicField': 'json',
    'IntListField': '[int]',
    'PointField': '[int]',
}

class XlsHandleMixin(object):

    upload_template = 'admin/model/upload.html'
    download_template = 'admin/model/download.html'

    @property
    def xls_meta(self):
        meta_names = []
        meta_formats = []
        meta_keys = []
        for key in self.model._fields_ordered:
            field = self.model._fields[key]
            xls_name = field.verbose_name.split('(')[0]
            xls_format = format_mapping[field.__class__.__name__]
            xls_key = field.name
            meta_names.append(xls_name)
            meta_formats.append(xls_format)
            meta_keys.append(xls_key)
        return dict(names=meta_names, formats=meta_formats, keys=meta_keys)

    @expose('/upload/', methods=('GET', 'POST'))
    def upload_view(self):

        if request.method == 'GET':
            return self.render(self.upload_template)

        # POST method

        file = request.files['file']
        if not file.filename.endswith('.xls'):
            flash(u'请选择 xls 文件', 'error')
            return redirect(url_for('.upload_view'))

        try:
            file_contents = file.read()
            xls = XlsFile(file_contents)
        except StandardError as error:
            flash(u'似乎不是一个有效的 xls 文件：%s' % error, 'error')
            return redirect(url_for('.upload_view'))

        if set(xls.keys) != set(self.xls_meta['keys']):
            flash(u'此 xls 文件格式不符合此资源定义', 'error')
            return redirect(url_for('.upload_view'))

        collection = self.model._get_collection()
        is_update = 'update' in request.form
        if is_update and not xls.errors:
            collection.drop()
            collection.insert(xls.docs.values())
            flash(u'更新成功', 'success')
            return redirect(url_for('.index_view'))

        errors = xls.errors
        src_docs = {doc['_id']: doc for doc in collection.find()}
        diff = xls.diff(src_docs)
        return self.render(self.upload_template, diff=diff, errors=errors)

    @expose('/download/', methods=('GET', 'POST'))
    def download_view(self):

        collection = self.model._get_collection()
        docs = list(collection.find())
        if hasattr(self, 'download_filename'):
            filename = self.download_filename()
        else:
            filename = '%s.xls' % self.name

        if request.method == 'GET':
            connection = collection.database.connection
            info = {
                'host': connection.host,
                'port': connection.port,
                'database': collection.full_name,
                'filename': filename,
                'count': len(docs),
            }
            return self.render(self.download_template, info=info)

        # POST method
        docs.sort(key=lambda d: d['_id'])

        creator = XlsCreator(self.xls_meta, docs)
        resp = make_response(creator.filebytes)
        if request.user_agent.browser == 'msie':
            filename = filename.decode('UTF-8').encode('GBK')
        else:
            filename = filename.encode('UTF-8')
        filename_header = 'attachment; filename="%s";' % filename
        resp.headers['Content-Disposition'] = filename_header
        resp.mimetype = 'application/vnd.ms-excel'
        return resp

    @property
    def can_upload(self):
        return self.allow_action('upload')

    @property
    def can_download(self):
        return self.allow_action('download')
