#!/usr/bin/env python
# -*- coding:utf-8 -*-
# vim: fdm=marker

# NOTE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# Python 各类特性使用说明
#   Property
#       针对同个名字的property 新旧代码都必须要有getter 要么都有setter要么都没有setter 要么都有deleter要么都没有deleter
#   装饰器
#       请谨慎使用 被装饰的函数能正常热更新，装饰器函数本身不能热更新，例如game.room.input.random_delay_robot_input
#   闭包
#       代码应该避免使用闭包，更新时不做闭包变量检查
#   全局变量|类属性
#       除了函数或类外一律用新的同名变量替换
#       请避免使用全局变量，类属性来存放动态数据
#   __slots__
#       请谨慎使用 使用尽量自己多热更新几次 看看是不是有未知未处理的风险
#   metaclass
#       请不要使用
#
# NOTE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# TODO：
# reload失败的回滚处理
#

__all__ = ["reload_module", "re", "rm"]

# import {{{1

import gc
import imp
import sys
import types
import marshal
import inspect
import corelib.hotupdate as h


from corelib import log

RELOAD_TYPE = 1 # 1:大富翁， 2：猎人

def logger(msg):
    log.info(msg)

def print_module(module):
    print "***", id(module)
    module_name = module["__name__"]
    for name, obj in module.iteritems():
        if name != "Player": continue

        if not hasattr(obj, "__module__"): continue
        if obj.__module__ != module_name: continue

        if inspect.isclass(obj):
            print "---> class", name, id(obj)
            for attr_name in obj.__dict__.keys():
                if attr_name != "test_s": continue
                attr_obj = getattr(obj, attr_name)
                print "~~~~~~~~~~~~", attr_name, id(attr_obj),
                if isinstance(attr_obj, types.FunctionType):
                    print id(attr_obj), id(attr_obj.func_code)
                elif isinstance(attr_obj, types.MethodType):
                    print id(attr_obj.im_func), id(attr_obj.im_func.func_code)
                else:
                    print
        if inspect.isfunction(obj):
            print "___> func", name, id(obj), id(obj.func_code)

# basic types {{{1

CLASS_STATICS = frozenset(["__dict__", "__doc__", "__module__", "__weakref__"])

class C(object):

    @property
    def p(self):
        pass

property_type = type(C.p)
dict_proxy_type = type(C.__dict__)
del C

class A(object):

    __slots__ = ('a', )

member_descriptor_type = type(getattr(A, "a"))
del A

# code obj equal test {{{1

def function():
    pass
code_obj = function.func_code
code_attrs = dir(code_obj)
del code_obj
del function

code_equal_ignore_atts = set(["co_filename", "co_firstlineno"])

def code_equal(onef, anotherf):
    one = onef.func_code
    another = anotherf.func_code

    for attr in code_attrs:
        if attr.startswith("__"):
            continue
        if attr in code_equal_ignore_atts:
            continue
        o = getattr(one, attr)
        a = getattr(another, attr)
        if attr == "co_consts":
            if not co_consts_equal(onef, anotherf, o, a):
                # logger("code_equal %s %s %s" % (attr, o, a))
                return False
        elif o != a:
            if attr != "co_code":
                logger("code_equal %s %s %s" % (attr, o, a))
            return False
    return True

def co_consts_equal(onef, anotherf, otup, atup):
    if len(otup) != len(atup):
        logger("co_consts_equal len not eq %s %s" % (otup, atup))
        return False
    for index, o in enumerate(otup):
        if o == getattr(onef, "__doc__", ""):
            # logger("co_consts_equal skip o __doc__ %s %s" % (otup, atup))
            continue
        a = atup[index]
        if a == getattr(anotherf, "__doc__", ""):
            # logger("co_consts_equal skip a __doc__ %s %s" % (otup, atup))
            continue
        if o != a:
            logger("co_consts_equal not eq %s %s" % (otup, atup))
            return False
    return True

# function type  {{{1
def get_cell_value(cell):
    return type(lambda: 0)(
        (lambda x: lambda: x)(0).func_code, {}, None, None, (cell,)
    )()

def get_decorated_func(func):
    if not func.func_closure:
        return func
    for cell in func.func_closure:
        cell_value = get_cell_value(cell)
        if callable(cell_value) and hasattr(cell_value, "__name__") and cell_value.__name__ == func.__name__:
            return get_decorated_func(cell_value)
    return func

class ClosureChanged(Exception):
    pass

# reloader {{{1

class Reloader(object):
    """ Reload a module in place, updating classes, methods and functions.

    Args:
      mod: a module object

    Returns:
      The (updated) input object itself.
    """

    def __init__(self, module, filepath=None):
        self.mod = module

        self.new_class = []
        self.new_function = []

        self.old_class = {}
        self.old_function = {}
        self.filepath = filepath

    def reload(self):
        modname = self.mod.__name__
        modns = self.mod.__dict__

        filename = modns["__file__"]
        if filename.endswith(".pyc"):
            filename = filename[:-1]
        # 阿拉丁热更新机制指定的代码路径
        if self.filepath:
            logger("reload_module %s use filepath ala %s " % (modname, self.filepath))
            filename = self.filepath

        # NOTE: 旧代码使用imp寻找模块路径 game.__init__会被直接reload(game)导致Game各种服务对象名字丢失
        # 由于项目本身只有更新py文件的需求 改为自己的写的简单路径查找

        try:
            with open(filename) as stream:
                source = stream.read()
            # PeterB: if we don't strip the source code and add newline we get a SyntaxError even if `python $filename` is perfectly happy.
            source = source.strip()+'\n'
            code = compile(source, filename, "exec")
        except Exception, err:
            logger("reload_module %s compile err" % (modname, err))

        # Execute the code im a temporary namespace; if this fails, no changes
        tmpns = {'__name__': modns['__name__'],
                 '__file__': modns['__file__'],
                 '__doc__': modns['__doc__']}
        if "__package__" in modns:
            tmpns["__package__"] = modns["__package__"]
        exec(code, tmpns)

        reload_not_replace = modns.get("__reload_not_replace__", [])

        # Now we get to the hard part
        _update_scope(modns, tmpns, reason=modname)
        # Now update the rest in place
        for name in set(modns) & set(tmpns):
            if name in reload_not_replace:
                continue
            self._update(modns, name, modns[name], tmpns[name], modname)

        # tmps为新代码动态生成的函数对象func_globals的指向
        # 该global的名字一般都会执行新生成func/class对象
        # 因为func.func_globals是只读的 不能改变
        # 所以这里不要清空该空间的名字 反而要将指向新对象改为指向旧对象

        # 正常reload 过后，旧代码不应该引用新代码的类/函数
        # 这里用于将旧代码中的dict/list的容器对新类的引用转为旧的
        # 示例: 上文提到的tmps 或 game.room.room MODE_ROOMS
        def dict_find_key(d, v):
            for key, value in d.iteritems():
                if value is v:
                    return key
        lo = locals()
        for klass in self.new_class:
            for ref in gc.get_referrers(klass):
                if type(ref) is list:
                    if ref is self.new_class: continue
                    index = ref.index(klass)
                    ref[index] = self.old_class[klass.__name__]
                elif type(ref) is dict:
                    if ref is lo: continue
                    mkey = dict_find_key(ref, klass)
                    ref[mkey] = self.old_class[klass.__name__]
        for func in self.new_function:
            for ref in gc.get_referrers(func):
                if type(ref) is list:
                    if ref is self.new_function: continue
                    index = ref.index(func)
                    ref[index] = self.old_function[func.__name__]
                elif type(ref) is dict:
                    if ref is lo: continue
                    mkey = dict_find_key(ref, func)
                    ref[mkey] = self.old_function[func.__name__]

        self.new_class = []
        self.new_function = []
        self.old_class = {}
        self.old_function = {}

        return self.mod

    def _update(self, modns, name, oldobj, newobj, modname):
        """Update oldobj, if possible in place, with newobj.

        If oldobj is immutable, this simply returns newobj.

        Args:
          oldobj: the object to be updated
          newobj: the object used as the source for the update

        Returns:
          either oldobj, updated in place, or newobj.
        """
        # 不处理非本模块的变量
        new_module = getattr(newobj, '__module__', None)
        if new_module and new_module != self.mod.__name__:
            return

        # 当变量类型改变时记录 一律使用新值
        if type(oldobj) is not type(newobj):
            logger("scope change name %s %s %s %s" % (modname, name, oldobj, newobj))
            modns[name] = newobj
            return

        # 全局变量会除了类型|函数外一律用新的同名变量替换
        if inspect.isclass(newobj):
            self.new_class.append(newobj)
            self.old_class[oldobj.__name__] = oldobj
            _update_class(oldobj, newobj)
        elif inspect.isfunction(newobj):
            self.new_function.append(newobj)
            self.old_function[oldobj.__name__] = oldobj
            _update_function(oldobj, newobj, "update function %s" % newobj.__name__)
        elif oldobj != newobj:
            logger("scope change name %s %s %s %s" % (modname, name, oldobj, newobj))
            modns[name] = newobj

def _closure_changed(oldcl, newcl):
    old = oldcl is None and -1 or len(oldcl)
    new = newcl is None and -1 or len(newcl)
    #NOTE: 先不要判断具体的闭包值，在使用了装饰器的时候，闭包里面可能有新旧的函数
    # return old != new
    if old != new:
        return True
    if old > 0 and new > 0:
        for i in range(old):
            same = oldcl[i] == newcl[i]
            if not same:
                return True
    return False

def _update_scope(oldscope, newscope, reason=""):
    """ 把module级别中新定义的变量放到旧moudle中 """
    oldnames = set(oldscope)
    newnames = set(newscope)

    # 增加新的名字
    for name in newnames - oldnames:
        if reason:
            logger("scope add new name %s %s %s" % (reason, name, newscope[name]))
        oldscope[name] = newscope[name]

    for name in oldnames - newnames:
        if not name.startswith('__'):
            logger("!!! scope old name not in new %s %s %s" % (reason, name, oldscope[name]))
            # NOTE: 不做这一步，避免代码运行做成中动态产生module级别的变量被删除
            # del oldscope[name]

def _update_function(oldfunc, newfunc, reason=""):
    """Update a function object."""
    oldfunc = get_decorated_func(oldfunc)
    newfunc = get_decorated_func(newfunc)
    # NOTE: 代码应该避免使用闭包，更新时不做闭包变量检查
    # if _closure_changed(oldfunc.func_closure, newfunc.func_closure):
    #     raise ClosureChanged
    if code_equal(oldfunc, newfunc):
        return oldfunc
    if reason:
        logger(reason)
    oldfunc.func_code = newfunc.func_code
    oldfunc.func_defaults = newfunc.func_defaults
    _update_scope(oldfunc.func_globals, newfunc.func_globals)
    return oldfunc

def _update_class(oldclass, newclass):
    olddict = oldclass.__dict__
    newdict = newclass.__dict__
    oldnames = set(olddict)
    newnames = set(newdict)

    klassname = oldclass.__name__

    for name in newnames - oldnames:
        logger("scope add new name %s %s %s" % (klassname, name, newdict[name]))
        setattr(oldclass, name, newdict[name])

    for name in oldnames - newnames:
        logger("!!! scope old name not in new %s %s %s" % (klassname, name, olddict[name]))
        # NOTE: 不做这一步，避免代码运行做成中动态产生临时属性被删除
        # delattr(oldclass, name)

    if hasattr(oldclass, "__reload_not_replace__"):
        reload_not_replace = oldclass.__reload_not_replace__
    else:
        reload_not_replace = []

    for name in sorted(oldnames & newnames - CLASS_STATICS):
        if name == "__reload_not_replace__":
            continue
        if name in reload_not_replace:
            logger("reload not replace %s %s %s %s" % (klassname, name, reload_not_replace, oldclass))
            continue

        new = getattr(newclass, name)
        old = getattr(oldclass, name)

        # class method or self method
        if isinstance(new, types.MethodType):
            _update_function(old.im_func, new.im_func, "update class method %s %s" % (klassname, name))

        # staticmethod
        elif isinstance(new, types.FunctionType):
            _update_function(old, new, "update static method %s %s" % (klassname, name))

        # property
        elif type(new) is property_type and type(old) is property_type:
            # 新旧代码都应该最少要有getter
            if old.fget and new.fget:
                _update_function(old.fget, new.fget, "update property_type method %s %s" % (klassname, name))
            else:
                logger("update class property fget %s %s %s %s" % (klassname, name, old.fget, new.fget))
            # 新旧代码要么都有setter 要么都没有setter
            if old.fset and new.fset:
                _update_function(old.fset, new.fset, "update property_type method %s %s" % (klassname, name))
            elif old.fset or new.fset:
                logger("update class property fset %s %s %s %s" % (klassname, name, old.fset, new.fset))
            # 新旧代码要么都有deleter 要么都没有deleter
            if old.fdel and new.fdel:
                _update_function(old.fdel, new.fdel, "update property_type method %s %s" % (klassname, name))
            elif old.fdel or new.fdel:
                logger("update class property fdel %s %s %s %s" % (klassname, name, old.fdel, new.fdel))

        # __slots__ 跳过不更新 不然会有旧类不能调用新类的方法的异常
        # CPython implementation detail: Member descriptors are attributes defined in extension modules via PyMemberDef structures.
        elif type(new) is member_descriptor_type and type(old) is member_descriptor_type:
            logger("update class skip __slots__ %s %s" % (klassname, name))
            continue

        else:
            # NOTE: 类属性会除了函数外一律用新的同名属性替换
            if not eq(new, old):
                logger("update class attr %s %s %s %s" % (klassname, name, old, new))
                setattr(oldclass, name, new)

    return oldclass

def eq(new, old, lv=1):
    newtype = type(new)
    oldtype = type(old)
    if oldtype is not newtype:
        logger("!!! eq match type not eq %s %s %s" % (old, new, lv))
        return False
    if oldtype in (int, long, float, str, unicode, tuple, set):
        return new == old
    if oldtype is types.FunctionType:
        return code_equal(old, new)
    if oldtype is list:
        if len(old) != len(new):
            return False
        for index, oe in enumerate(old):
            ne = new[index]
            # 避免无穷递归
            newlv = lv + 1
            if newlv >= 0xff:
                return False
            if not eq(oe, ne, lv+1):
                return False
        return True
    if oldtype is dict:
        if len(old) != len(new):
            return False
        for key, oe in old.items():
            if key not in new:
                return False
            ne = new[key]
            # 避免无穷递归
            newlv = lv + 1
            if newlv >= 0xff:
                return False
            if not eq(oe, ne, newlv):
                return False
        return True
    logger("!!! eq not match type %s %s %s %s %s" % (old, new, type(old), type(new), lv))
    return old == new

def reload_module(module_name, filepath=None):
    # h.Update(module_name)
    # print "reload_module", module_name, filepath
    try:
        module = sys.modules.get(module_name)
        if not module:
            print "no module ---  %s"%(module_name)
            logger("real_reload_module no module %s" % module_name)
            return

        logger("reload_module %s %s begin" % (module_name, module))
        l = [0, 0, 0, 0]
        l[0] = len(gc.get_objects())
        gc.collect()
        l[1] = len(gc.get_objects())

        if RELOAD_TYPE == 1:
            # 大富翁的热更方式
            Reloader(module, filepath).reload()
        else:
            # 猎人的热更方式
            h.Update(module_name)

        l[2] = len(gc.get_objects())
        gc.collect()
        l[3] = len(gc.get_objects())

        logger("reload_module %s %s end %s" % (module_name, module, l))

    except Exception, err:
        logger("!!! reload_module %s %s error %s" % (module_name, module, err))
        log.log_except()

re = reload_module
rm = reload_module

def do_reload(files):

    def fname_to_module(fname):
        i = fname.find("code")
        mname = fname[i+len("code")+1:]
        m =  ".".join(mname.split("\\"))
        if m.endswith(".__init__.py"):
            return m[:-len(".__init__.py")]
        if m.endswith(".py"):
            return m[:-len(".py")]
        return m

    import app
    l = []
    for fname in files:
        if "xreload" in fname:
            continue
        l.append(fname_to_module(fname))
    if not l:
        return
    app.frame.reload_modules(l)

