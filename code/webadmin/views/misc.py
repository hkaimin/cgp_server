#!/usr/bin/env python'
# -*- coding: utf-8 -*-

import urllib
from itertools import groupby
from collections import OrderedDict
from flask import (request, abort, jsonify, flash, redirect,
                   make_response, url_for, current_app as app)
from flask.ext.admin import expose, BaseView

class ImageView(BaseView):
    ''' 客户端资源的图片反向代理 '''

    def is_visible(self):
        return False

    @expose('/')
    def index_view(self):
        abort(404)

    @expose('/<path:filename>')
    def file_view(self, filename):
        if not filename.endswith('.png'):
            abort(404)

        svn_url = 'http://builder:m654n@dev.zl.efun.com/svn/richer-builder/res/images/'
        url = svn_url + filename
        urlopener = urllib.urlopen(url)

        retcode = urlopener.getcode()
        data = urlopener.read()
        headers = urlopener.headers

        if retcode != 200:
            abort(retcode)

        resp = make_response(data, urlopener.getcode())
        for name in ('accept-ranges', 'last-modified', 'date'):
            resp.headers[name] = headers[name]
        resp.headers['content-type'] = 'image/png'
        return resp

class GamesvrView(BaseView):
    ''' 服务器 '''

    def is_visible(self):
        return False

    @expose('/')
    def index_view(self):
        zoning = app.extensions['zoning']
        current, candidates = zoning.current_and_candidate()
        return self.render('gamesvr.html',
                            current=current, candidates=candidates)

    @expose('/list.json')
    def list_view(self):
        zoning = app.extensions['zoning']
        gamesvrs = zoning.gamesvrs
        return jsonify(gamesvrs)

    @expose('/switch', methods=('GET', 'POST'))
    def switch_view(self):
        if request.method == 'GET':
            id = request.args.get('id', type=int)
        else:
            id = request.form.get('id', type=int)
        zoning = app.extensions['zoning']
        try:
            gamesvr = zoning.switch_my_gamesvr(id)
            flash('切换为服务器为 「%s」 成功' % gamesvr['title'], 'success')
        except StandardError as error:
            flash('切换为服务器 %s 失败：%s' % (id, error), 'error')
        return redirect(url_for('.index_view'))

views = [
    ImageView(name=u'图片', endpoint='image', url='/image'),
    GamesvrView(name=u'服务器', endpoint='gamesvr', url='/gamesvr'),
]
