#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app
from flask.ext.admin import expose, BaseView

class SystemSummaryView(BaseView):

    def is_visible(self):
        return False

    @expose('/')
    def index_view(self):
        return self.render('system_summary.html', config=app.config)
