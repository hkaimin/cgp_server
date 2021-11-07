#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, flash, redirect, url_for
from flask.ext.admin import expose
from webadmin.library.aimm_handle import AimmFile
from .base import ModelView
from .mixin import XlsHandleMixin


class ResourceModelView(ModelView, XlsHandleMixin):

    page_size = 500

    def download_filename(self):
        collection = self.model._get_collection()
        filename = '%s(%s).xls' % (self.name, collection.name)
        return filename


class AiCodeResourceModelView(ResourceModelView):

    @expose('/upload/', methods=('GET', 'POST'))
    def upload_view(self):

        if request.method == 'GET':
            return self.render(self.upload_template)

        # POST method

        file = request.files['file']
        if not file.filename.endswith('.mm'):
            flash(u'请选择 mm 文件', 'error')
            return redirect(url_for('.upload_view'))

        try:
            file_contents = file.read()
            mm = AimmFile(file_contents)
        except StandardError:
            flash(u'似乎不是一个有效的 mm 文件', 'error')
            return redirect(url_for('.upload_view'))

        collection = self.model._get_collection()
        is_update = 'update' in request.form
        if is_update:
            collection.drop()
            collection.insert(mm.docs.values())
            flash(u'更新成功', 'success')
            return redirect(url_for('.index_view'))

        src_docs = {doc['_id']: doc for doc in collection.find()}
        diff = mm.diff(src_docs)
        return self.render(self.upload_template, diff=diff)

class ErrorModelView(ResourceModelView):

    form_excluded_columns = None
