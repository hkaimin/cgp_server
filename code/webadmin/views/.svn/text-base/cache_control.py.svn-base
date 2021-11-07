#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redis import StrictRedis
from flask import request, redirect, flash, url_for, current_app as app
from flask.ext.admin import expose, BaseView


class CacheControlView(BaseView):
    html = 'dev/cache_control.html'

    def is_visible(self):
        return False

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        db_url = app.config.get('CACHE_DB')
        cache_db = StrictRedis.from_url(db_url)

        if request.method == 'POST':
            cache_db.flushall()
            flash(u'所有数据已清空', 'success')
            return redirect(url_for(request.endpoint))


        try:
            cache_db.ping()
        except Exception as error:
            return self.render(self.html,
                                db_url=db_url, error=error)

        entries = cache_db.keys('*')
        info = cache_db.info().items()
        info.sort()

        return self.render('cache_control.html',
                           db_url=db_url, error=None,
                           entries=entries, info=info)
