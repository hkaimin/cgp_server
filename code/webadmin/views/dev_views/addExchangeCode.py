#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxleung'

from gm_base_view import *
from flask import current_app as app, request, flash, session
from flask.ext.admin import expose, BaseView
from flask import (request, redirect, flash, abort, jsonify,
                   url_for, make_response, current_app as app)
from webadmin.define.constant import *
from corelib import gtime

defualt_args = {}

class AddExchangeCodeView(BaseView):
    html = 'dev/addExchangeCode.html'

    def is_visible(self):
        return False

    def resource_db(self):
        zoning = app.extensions['zoning']
        return zoning.my_resource_db()

    def get_servers(self):
        db = self.resource_db()
        return list(db['Server'].find())

    # @property
    # def res_db(self, dbname):
    #     conn = pymongo.Connection(host='192.168.0.210',port=27017)
    #     db = conn[dbname]
    #     db.authenticate("dev","dev123")   #验证
    #     return db

    @property
    def gamesvr(self):
        return app.extensions['gamesvr']

    @expose('/', methods=('GET', ))
    def index_view(self):

        servers = self.get_servers()
        default = lambda: self.render(self.html,
                                      servers=servers, args=defualt_args)

        if request.method == 'GET':
            return default()

        args = dict(request.form.items())

        try:
            server_name = args.pop('server', None)
        except ValueError as error:
            flash('无效的表单参数：' + str(error), 'error')
            return default()

    @expose('/drold/', methods=('GET', 'POST'))
    def dr_old(self):
        """
        仅本地导入兑换码文件使用
        """

        import xlwt
        import xlrd
        from ...models.resource import ExchangeCode

        folderName = 'eCode_rich9_import_2'  #文件夹名

        jingbi5 = dict(fname='jbi-5w-', p='jingbi5', rid=1, zname=u'金币5万', fcount=32)
        xyx50 = dict(fname='xyx-50-', p='xyx50', rid=2, zname=u'幸運星-50', fcount=17)
        xyx666 = dict(fname='xyx-666-', p='xyx666', rid=3, zname=u'幸運星-666', fcount=2)
        xyx888 = dict(fname='xyx-888-', p='xyx888', rid=4, zname=u'幸運星-888', fcount=1)
        sjjsrn = dict(fname='sjjsrn-', p='sjjsrn', rid=5, zname=u'隨機經典角色人物', fcount=1)

        suijisaizix1 = dict(fname='suijisaizix1-', p='suijisaizix1', rid=7006, zname=u'隨機骰子', fcount=1)
        xingyunxing100 = dict(fname='xingyunxing100-', p='xingyunxing100', rid=7007, zname=u'幸運星-100', fcount=1)
        jinbi10w = dict(fname='jinbi10w-', p='jinbi10w', rid=7008, zname=u'金幣- 10萬', fcount=1)
        xingyunxing50 = dict(fname='xingyunxing50-', p='xingyunxing50', rid=7009, zname=u'幸運星-50', fcount=1)
        jinbi1w = dict(fname='jinbi1w-', p='jinbi1w', rid=7010, zname=u'金幣-1萬', fcount=3)

        allFList = [jingbi5, xyx50, xyx666, xyx888, sjjsrn]

        allFList = [suijisaizix1, xingyunxing100, jinbi10w, xingyunxing50, jinbi1w]
        allFList = [jinbi1w]



        res_db = self.resource_db()
        exchangecodeTb = res_db['exchangecode']

        allCount = 0

        for fdict in allFList:
            fcount = fdict['fcount']
            bname = fdict['p']  #批次名
            fname = fdict['fname']  #文件名
            znname = fdict['zname']
            rid = fdict['rid']

            for n in range(fcount):

                fNamePath = r'D:\%s\%s%d.xls' % (folderName, fname, n+1)

                workbook = xlrd.open_workbook(fNamePath)
                table = workbook.sheets()[0]
                alist = table.col_values(1)

                bathData = []

                fBuildCount = 0
                for ecode in alist:

                    insert_val = dict(_id=str(ecode),
                                      batchName=bname,
                                      createTime=1448985600,
                                      endTime=1467302399,
                                      roleIsOnce=1,
                                      rewardId=rid,
                                      useCount=1)

                    fBuildCount += 1
                    allCount += 1
                    bathData.append(insert_val)

                    print u'正在导入批次: ', fNamePath
                    print u'当前计数: ', allCount

                result = exchangecodeTb.insert(bathData)
                if result:
                    print u'文件完成导入：%s.  生成条数: %d' % (fNamePath, fBuildCount)
                else:
                    print u'文件导入错误: ', fNamePath
                    return 'import error !!. fileName: %s' % (fNamePath)

        return 'import count: %d' % allCount



    @expose('/add_code/', methods=('GET', 'POST'))
    def add_code(self):
        batchName = request.args.get('batchName')
        createTime = request.args.get('createTime')
        endTime = request.args.get('endTime')
        roleIsOnce = request.args.get('roleIsOnce')
        rewardId = request.args.get('rewardId')
        length = int(request.args.get('length'))
        useCount = request.args.get('useCount')
        addCount = request.args.get('addCount')


        respCode = self.build_code(batchName, createTime, endTime, roleIsOnce, rewardId, length, useCount, addCount)

        return 'success' if (respCode==0) else respCode

    def build_notrepeat(self, count, length, **inserKw):
        """
        生成count条数唯一兑换码
        count: 查询条数
        **inserKw: insert字典值
        """
        import uuid, random

        def uuid_tmpcode(length):
            uuid_tmp = uuid.uuid1()
            uuid_tmp = str(uuid_tmp).replace('-', '')
            if length != 32:
                uuid_tmp = ''.join(random.sample(uuid_tmp, length))
            return uuid_tmp

        #e5a061ce32,e0609113c9,01e9c56e58
        #tmpEcodeList = ['e5a061ce32','e0609113c9','01e9c56e58',]  #测试重复值

        tmpEcodeList = []
        i = 0
        #while i < 2:
        while i < count:
            uuid_tmp = uuid_tmpcode(length)

            if uuid_tmp not in tmpEcodeList:
                tmpEcodeList.append(uuid_tmp)
                i += 1
            else:
                i -= 1


        #表中查询是否存在
        exchangecodeTb = self.resource_db()['exchangecode']
        cursor = exchangecodeTb.find({'_id':{'$in':tmpEcodeList}})
        existList = [existCode['_id'] for existCode in cursor]

        #选出正确数据
        alist = [ecode for ecode in tmpEcodeList if ecode not in existList]

        normalList = []
        for ecode in alist:
            adict = dict(_id=ecode)
            adict.update(inserKw)
            normalList.append(adict)

        return normalList


    def build_code(self, *args):

        batchName, createTime, endTime, roleIsOnce, rewardId, length, useCount, addCount = args
        addCount = int(addCount)

        exchangecodeTb = self.resource_db()['exchangecode']

        #转换时间戳
        start_time = '%s 00:00:00' % (createTime)
        end_time = '%s 23:59:59' % (endTime)
        start_time = gtime.str2time(start_time)
        end_time = gtime.str2time(end_time)

        i = 0
        normalCodeList = []

        while i < addCount:

            insert_val = dict(batchName=batchName,
                              createTime=int(start_time),
                              endTime=int(end_time),
                              roleIsOnce=int(roleIsOnce),
                              rewardId=int(rewardId),
                              useCount=int(useCount))

            #限制最大每次查询500条
            count = 500 if addCount>500 else addCount
            normalList = self.build_notrepeat(count, length, **insert_val)
            normalCodeList.extend(normalList)

            i = len(normalCodeList)

        #批量插入生成数据
        try:
            exchangecodeTb.insert(normalCodeList)
            return 0
        except Exception, e:
            return e