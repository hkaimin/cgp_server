#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, os

###########  库加载  ##########

def install_psyco():
    """ 使用psyco包，提高速度，但在linux下，很耗内存 """
    try:
        import psyco
        psyco.full()
        print('***psyco installed.')
    except ImportError:
        pass

def install_cpp_protobuf():
    """ 使用protobuf 2.4中开始引入的c扩展模块，提高速度 """
    #protobuf use cpp
    os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'cpp'
    try:
        from google.protobuf.internal import cpp_message
        print('use cpp protobuf')
    except ImportError:
        os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

def install_pypy():
#    return
    #判断是否存在pypy
    #python同目录下有pypy
    sys_setting = sys.modules['SysSetting']

    is_source = os.path.exists(os.path.join(sys_setting.root_path, 'main.py'))
    pub_path = os.path.dirname(sys_setting.root_path)
    pypy_root_path = sys_setting.root_path
    if os.path.exists(os.path.join(sys_setting.py_path, 'pypy')):
        pypy = os.path.join(sys_setting.py_path, 'pypy')
    elif os.path.exists(os.path.join(pub_path, 'env', 'pypy', 'bin', 'pypy')):
        pypy = os.path.join(pub_path, 'env', 'pypy', 'bin', 'pypy')
    else:
        pypy = None
    if pypy:
        if is_source:
            os.environ['pypy'] = '%s main.py' % pypy
        else:
            pypy_root_path = os.path.join(pub_path, 'svr_pypy')
            if not os.path.exists(pypy_root_path):
                pypy = None
            else:
                os.environ['pypy'] = '%s main.pyc' % pypy
                os.environ['pypy_cwd'] = pypy_root_path

        if pypy:
            print('install pypy:', os.environ['pypy'])

    #pypy运行时: 安装pypycore
    if 'PyPy' not in sys.version:
        return
    sys_setting.root_path = pypy_root_path
    sys_setting.lib_path = os.path.join(sys_setting.root_path, 'lib')
    sys_setting.root_path.encode('utf-8')
    print('update pypy root:', sys_setting.root_path, sys_setting.lib_path)

    os.environ['GEVENT_LOOP'] = 'pypycore.loop'
    from gevent.hub import Hub
    Hub.loop_class = 'pypycore.loop'
    print('install GEVENT_LOOP=pypycore.loop', Hub.loop_class)


def wingdbg():
    #wingIDE调试加载 必须在gevent path替换系统socket之前调用，否则会失效
    if sys.argv[-1] == 'subgame_debug':
        sys.argv.pop()
        try:
            print(u'启动wingide调试')
            import wingdbstub
        except ImportError:
            print(u'启动wingide调试失败')
