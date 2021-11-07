#!/usr/bin/env python
# -*- coding:utf-8 -*-

import gc
import sys
import os
import locale
from os.path import dirname, abspath

class SysSetting(object):
    """系统环境"""
    def __init__(self):
        self.app_argv = None #启动参数
        self.language_code = None #语言
        self.sys_encoding = None #系统编码
        self.py_path = None #python目录
        self.executable = None #执行命令
        self.root_path = None #项目根目录
        self.lib_path = None #项目库目录
        self.version = None #代码版本

        self.init()

    def init(self):
        #wingIDE调试加载 必须在gevent path替换系统socket之前调用，否则会失效
        from package import wingdbg
        wingdbg()

        #减少周期性检查
        sys.setcheckinterval(1000)
        #启动参数
        self.app_argv = ' '.join(sys.argv[2:])
        #编码
        self.init_encoding()
        #路径
        self.init_path()
        #代码版本
        self.read_svn_version()
        #启动gc
        gc.enable()

        from linux.block_fileon import BlockFileon
        BlockFileon()

    def init_encoding(self):
        """编码"""
        #改变系统默认转换编码格式
        import sys
        stderr, stdin, stdout = sys.stderr, sys.stdin, sys.stdout
        reload(sys); sys.setdefaultencoding('utf-8')
        sys.stderr, sys.stdin, sys.stdout = stderr, stdin, stdout

        language_code, sys_encoding = locale.getdefaultlocale()
        if sys_encoding is None:
            sys_encoding = 'UTF-8'
        self.language_code = language_code #语言
        self.sys_encoding = sys_encoding #系统编码

    def init_path(self):
        """初始化路径"""
        # if sys.platform in ['win32', 'cygwin']:
        #     executable = abspath(sys.argv[0]).replace("\\code", "")
        # else:
        #     executable = abspath(sys.argv[0]).replace("/code", "")
        executable = abspath(sys.argv[0])
        self.py_path = dirname(executable) #python目录
        self.root_path = os.path.abspath(os.path.dirname(__file__)).decode(self.sys_encoding)  #根目录

        if os.path.exists('main.py'):
            main_py = ' main.py'
        else:
            main_py = ' main.pyc'

        self.executable = executable + main_py
        self.lib_path = os.path.join(self.root_path, 'lib') #库目录
        sys.path.insert(0, self.lib_path) #加入库目录
        self.root_path.encode('utf-8')

    def read_svn_version(self):
        """代码版本"""
        file_path = os.path.join(self.root_path, 'svn_version')
        try:
            with open(file_path, 'r') as fh:
                version = fh.readline().strip()
                self.version = version
                print('svn_version:', version)
        except IOError:
            pass

message = u"""
启动方式:
.运行程序:
    python main.py <app> <start|stop|status|run>

.运行测试:
    python main.py test

.log 信息显示
    python main.py log <app>

.远程shell:
    python main.py tools shell ip port

.用meliae分析内存文件:
    python main.py tools meliae file_path
"""


def main():
    print sys.path
    sys_setting = SysSetting()
    if len(sys.argv) < 3:
        print(message.encode(sys_setting.sys_encoding))
        sys.exit(0)
    sys.modules['SysSetting'] = sys_setting
    from launch import Launcher
    launcher = Launcher()
    app = launcher.load_config()
    launcher.execute(app)

if __name__ == '__main__':
    main()
