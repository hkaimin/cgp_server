#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask.ext.admin import expose, BaseView
from flask import current_app as app, request, flash, session
from flask import Markup
from werkzeug import secure_filename
import zipfile
import subprocess

from corelib.geventfix import td_start_new_thread

RESFILEPATH = 'ResFilePath'
RES_UPLOAD_LABEL = 'git-pulling....'
RES_UPLOAD_MSG = {}



class UploadLngView(BaseView):

    html = 'dev/upload_lng.html'

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        msg_key = self.get_store_git_path()
        rs_msg = RES_UPLOAD_MSG.setdefault(msg_key, '')
        if request.method == "POST":
            if not rs_msg is RES_UPLOAD_LABEL:
                ver = 0
                if 'ver' in request.form:
                    ver = request.form['ver']
                rs_msg = RES_UPLOAD_LABEL
                RES_UPLOAD_MSG[msg_key] = rs_msg
                path = self.get_store_git_path()
                t1 = td_start_new_thread(self.subpopen_shell, (path, ver))

        return self.render(self.html, rs_msg=Markup(rs_msg))

    def subpopen_shell(self, path, ver):
        if not ver:
            cmd = 'cd %s \n git pull \n git log -3' % path
        else:
            cmd = 'cd %s \n git reset --hard %s \n git log -3' % (path, ver)

        rs = subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        RES_UPLOAD_MSG[path] = rs.stdout.read().replace('\n', "<br/>")
        rs.kill()


    def get_store_path(self, sub, fname):
        """ 获取路径及创建目录 """
        db = app.extensions['zoning'].my_resource_db()
        home_path = str(db['gconfig'].find({'key': 'resHomePath'})[0]['value'])
        path = str(db['gconfig'].find({'key': 'resUrl'})[0]['value'])
        path = path.replace('http://', '')
        cc = path.find("/")
        path = "%s%s" % (home_path, path[cc:])

        fname = secure_filename(fname)
        urlfile = '%s/%s/%s' % (path, sub, fname)
        urldir = '%s/%s' % (path, sub)
        if not os.path.isdir(urldir):
            os.mkdir(urldir)
        return urldir, urlfile

    def get_store_git_path(self):
        """ 获取路径及创建目录 """
        db = app.extensions['zoning'].my_resource_db()
        home_path = str(db['gconfig'].find({'key': 'resHomePath'})[0]['value'])
        path = str(db['gconfig'].find({'key': 'resUrl'})[0]['value'])
        path = path.replace('http://', '')
        cc = path.find("/")
        path = "%s%s" % (home_path, path[cc:])
        return path

    def do_uzip(self, urldir, urlfile):
        """ 解压删除原来文件 """
        try:
            zf = zipfile.ZipFile(urlfile, 'r')
            for file in zf.namelist():
                zf.extract(file, urldir)
        except Exception:
            pass
        os.remove(urlfile)
