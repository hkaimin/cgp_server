#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app, url_for
from flask.ext.admin import expose, BaseView


class SystemGroupView(BaseView):

    def is_visible(self):
        return False

    @expose('/')
    def index_view(self):
        guard = app.extensions['guard']
        groups = []
        for group_ in guard.groups.itervalues():
            group = group_.copy()
            group['details'] = \
                    guard.get_permission_details_by_group(group['_id'])
            group['members'] = guard.get_group_members(group['_id'])
            groups.append(group)
        return self.render('system_group/list.html', groups=groups)

    @expose('/new', methods=('GET', 'POST'))
    def new_view(self):
        pass

    @expose('edit/<int:id>', methods=('GET', 'POST'))
    def edit_view(self, id):
        return 'nonono'#self.render('system_group/list.html', groups=[])
