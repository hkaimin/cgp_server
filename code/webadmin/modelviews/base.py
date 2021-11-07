#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from mongoengine.fields import DynamicField
from flask import request, current_app as app
from flask.ext.admin.contrib import mongoengine as flaskadmin_mongoengine
from webadmin.library.mongoengine_fields import IntListField, PointField, TimeField
from webadmin.library.model_converter import ModelConverter


def json_formatter(view, context, model, name):
    value = model[name]
    return json.dumps(value, indent=4).decode('unicode_escape')


AUTO_INC_TABLE = '_auto_inc_'


def auto_inc(db, table_name, count=1):
    """ 获取自增值 """
    inc = db[AUTO_INC_TABLE]

    if inc.find_one({'name':table_name}) is None:  # 新增记录
        inc.save({'name':table_name, 'id':0})

    v = inc.find_and_modify(query={'name': table_name}, update={'$inc': {'id':count}}, new=True)
    return int(v['id'])


class ModelView(flaskadmin_mongoengine.ModelView):

    layout_template = 'admin/master.html'
    column_default_sort = 'id'
    # form_excluded_columns = ('id', )
    model_form_converter = ModelConverter
    object_id_converter = int

    def __init__(self, model, name=None,
                 category=None, endpoint=None, url=None):

        if name is None and hasattr(model, '__doc__'):
            name = model.__doc__.strip()

        super(ModelView, self).__init__(model, name, category, endpoint, url)

    # 重载父类函数 { #

    def get_query(self):
        """
        支持多数据库
        """
        return self.model.get_zone_objects()

    def is_visible(self):
        return False

    def on_model_change(self, form, model, is_created=None):
        """ 模型修改前处理 """
        # 如果是新建，添加自定义的 _id
        if is_created and model.id is None:
            model.id = self.get_next_id()

    def render(self, template, **kwargs):
        """ 模板渲染前处理 """
        # 添加布局模板名
        kwargs['layout_template'] = self.layout_template
        return super(ModelView, self).render(template, **kwargs)

    def get_column_name(self, field):
        """ 表格头"""
        if field == 'id':
            return 'ID'
        # 使用中文名
        name = self.model._fields[field].verbose_name
        if name is not None:
            name = name.split('(')[0]
        else:
            name = field
        return name

    @property
    def column_formatters(self):
        """ 表格内容格式化 """
        if not hasattr(self, '_column_formatters'):
            attr = {}
            for name, field in self.model._fields.iteritems():
                if isinstance(field, DynamicField):
                    attr[name] = json_formatter
            self._column_formatters = attr
        return self._column_formatters

    @property
    def column_filters(self):
        """ 过滤器条目 """
        # 自动列出所有可以过滤的字段
        if not hasattr(self, '_column_filters'):
            ingore_field_types = (IntListField, PointField, DynamicField, TimeField)
            names = self.model._fields_ordered
            fields = self.model._fields
            filterable = lambda x: not isinstance(fields[x], ingore_field_types)
            self._column_filters = filter(filterable, names)
        return self._column_filters

    # 重载父类函数 } #

    # 自定扩展函数 { #

    def is_active(self, name):
        """ 父页地址是否激活中 """
        return request.endpoint.endswith(name)

    def get_next_id_ex(self):
        """ 使用数据长度确定, 获取下一个 id 的值 """
        models = self.model.objects.order_by('+id')
        n = len(models)
        if n == 0:
            next_id = 1
        else:
            next_id = models[n - 1].id + 1
        return next_id

    def get_next_id(self):
        """ 同游戏服一个机制,用自增表确定自增id, 获取下一个 id 的值 """
        db = self.model._get_db()
        table_name = self.model._get_collection_name()
        next_id = auto_inc(db, table_name)
        return next_id

    def allow_action(self, action_name):
        """ 是否允许某动作 """
        model_type = request.endpoint.split('.')[0]
        pms_name = '%s.*.%s_view' % (model_type, action_name)
        guard = app.extensions['guard']
        return guard.allow_endpoint_me(pms_name, path=request.path)

    @property
    def can_create(self):
        return self.allow_action('create')

    @property
    def can_edit(self):
        return self.allow_action('edit')

    @property
    def can_delete(self):
        return self.allow_action('delete')

    # 自定扩展函数 } #
