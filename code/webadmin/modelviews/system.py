#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import ModelView

class SystemModelView(ModelView):

    page_size = 100
    column_exclude_list = ('password', )

