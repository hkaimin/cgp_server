#!/usr/bin/env python
# -*- coding:utf-8 -*-

from weakref import WeakKeyDictionary

from gevent import sleep, joinall
from gevent.pool import Pool
from gevent.queue import Queue

from corelib import spawn, log
from .driver import get_driver

#排序
ASCENDING = 1
DESCENDING = -1


class StoreObj(object):
    TABLE_NAME = None
    KEY_NAME = 'id'

    @classmethod
    def new_dict(cls, **kw):
        """ 新字典 """
        new = cls()
        new.update(kw)
        return new.to_save_dict()

    @classmethod
    def new_from_list(cls, dict_list, chk_func=None):
        """ 从字典列表创建对象列表 """
        return [cls(adict=d) for d in dict_list if chk_func is None or chk_func(d)]

    def __init__(self, adict=None):
        self.init()
        if adict is not None:
            self.update(adict)
        self.modified = False

    def __getstate__(self):
        return self.to_save_dict()

    def __setstate__(self, data):
        for key, value in data.iteritems():
            setattr(self, key, value)

    def init(self):
        self.id = None

    def modify(self):
        self.modified = True

    def update(self, adict):
        """ 更新 """
        if not adict:
            return
        for k, v in adict.iteritems():
            setattr(self, k, v)
        self.modified = True

    def to_save_dict(self, copy=False, forced=False):
        raise NotImplementedError("StoreObj func to_save_dict not found")

    def copy_from(self, dataobj):
        self.update(dataobj.to_save_dict())

    @classmethod
    def load(cls, store, key, check=False):
        if check and not store.has(cls.TABLE_NAME, key):
            return
        adict = store.load(cls.TABLE_NAME, key)
        if adict:
            obj = cls(adict=adict)
            return obj

    @classmethod
    def load_ex(cls, store, querys):
        alist = store.query_loads(cls.TABLE_NAME, querys)
        if not alist:
            return
        if len(alist) > 1:
            log.error('[StoreObj]load_ex repeat error:%s- querys:%s', cls.TABLE_NAME, querys)
        obj = cls(adict=alist[0])
        return obj

    def save(self, store, forced=False, no_let=False):
        """ 保存 """
        if getattr(self, self.KEY_NAME, None) is None:
            key = store.insert(self.TABLE_NAME, self.to_save_dict())
            setattr(self, self.KEY_NAME, key)
        elif forced or self.modified:
            store.save(self.TABLE_NAME, self.to_save_dict(forced=forced), no_let=no_let)
        self.modified = False

    @classmethod
    def saves(cls, store, objs, filter=None):
        """ 批量保存 """
        news, mods = [], []
        for o in objs:
            if filter is not None and not filter(o):
                continue
            if o.id is None:
                news.append(o)
            elif o.modified:
                mods.append(o.to_save_dict())
        if news:
            map(lambda o: o.save(store), news)
        if mods:
            store.saves(cls.TABLE_NAME, mods)

    def delete(self, store):
        """ 删除 """
        if self.id is None:
            return
        store.delete(self.TABLE_NAME, self.id)


def wrap_get(func):
    """ 包装store，将数据请求转发到store;
    """
    def _func(self, *args, **kw):
        store_func = getattr(self.store, func.func_name)
        return self._get(store_func, *args, **kw)
    _func.obj_func = func
    return _func


class Store(object):
    """ 存储类 """
    STORE_INFOS = None
    INITDBS = tuple()

    def __init__(self):
        if 0:
            from .mongodb import MongoDriver
            self.store = MongoDriver()
        self.store = None
        self.stoped = False

    def init(self, url, **dbkw):
        self.db_name = url.split('/')[-1]
        self.url = url
        self.store = get_driver(url, **dbkw)
        cls_infos = self.STORE_INFOS[self.store.engine_name]
        self._set_lets = WeakKeyDictionary()
        if not self.store.init_cls_infos(cls_infos):
            raise ValueError('store have init!')
        if 0:
            from .mongodb import MongoDriver
            self.store = MongoDriver()

    def start(self):
        pass

    def stop(self):
        """ 停止,必须保证异步的任务已经全部完成 """
        self.stoped = True
        lets = self._set_lets.keys()
        joinall(lets)
        log.warn('[store](%s) stop complete!', self.db_name)
        return True

    def _get(self, store_func, *args, **kw):
        """ 包装store，将数据请求转发到store; """
        return store_func(*args, **kw)

    def _set(self, store_func, *args, **kw):
        """ 包装store，将数据请求转发到store; """
        if self.stoped:
            raise ValueError('[store](%s) has stoped!'  % self.db_name)
        let = spawn(store_func, *args, **kw)
        self._set_lets[let] = 0
        return let

    def insert(self, tname, values):
        """ 新增,返回key """
        kn = self.store.get_key(tname)
        kv = self._get(self.store.insert, tname, values)
        return kv

    def inserts(self, tname, values_list):
        """ 批量新增,返回key """
        return self._get(self.store.inserts, tname, values_list)

    def save(self, tname, values, no_let=False):
        """ 保存,values必须包含key """
        if no_let:
            self.store.save(tname, values)
        else:
            self._set(self.store.save, tname, values)

    def saves(self, tname, values_list):
        """ 批量修改 """
        self._set(self.store.saves, tname, values_list)

    def has(self, tname, key):
        return self._get(self.store.has, tname, key)

    def load(self, tname, key):
        return self._get(self.store.load, tname, key)

    def loads(self, tname, keys):
        return [self.load(tname, key) for key in keys]

    def load_all(self, tname, sort_by=None):
        return self.values(tname, None, None, sort_by=sort_by)

    def query_loads(self, tname, querys, limit=0, sort_by=None, skip=0):
        return self.loads(tname, self.store.iter_keys(tname, querys, limit=limit, sort_by=sort_by, skip=skip))

    def load_tables(self, tnames, querys):
        """加载多个表"""
        rs = []
        for tname in tnames:
            rs.append(self.query_loads(tname, querys))
        return rs

    def clear(self, tname):
        self._get(self.store.clear, tname)

    def delete(self, tname, key):
        self._set(self.store.delete, tname, key)

    def deletes(self, tname, keys=None):
        if keys is None:
            self.clear(tname)
            return
        for key in keys:
            self.delete(tname, key)

    def query_deletes(self, tname, querys):
        """ 根据条件，删除一批数据 """
        self.deletes(tname, self.store.iter_keys(tname, querys))

    def update(self, tname, key, values):
        self._set(self.store.update, tname, key, values)

    @wrap_get
    def count(self, tname, querys):
        """ 根据条件，获取结果数量 """
        pass

    def values(self, tname, columns, querys, limit=0, sort_by=None, skip=0):
        """ 根据名称列表，获取表的数据, 返回的是tuple """
        return list(self._get(self.store.iter_values,
            tname, columns, querys, limit=limit, sort_by=sort_by, skip=skip))

    @wrap_get
    def execute(self, statement, params=None):
        """ 高级模式:根据不同后台执行sql或者js(mongodb) """
        pass

    @wrap_get
    def map_reduce(self, tname, map, reduce, out=None, inline=1, full_response=False, **kwargs):
        """ mongodb的map_reduce """
        pass

    def initdb(self, tables=None):
        """ 清除数据库 """
        if tables is None:
            tables = self.INITDBS
        self.store.initdb(tables)

    def dump(self, dump_path):
        """ 备份数据库 """
        pass

    def restore(self, dump_path):
        """ 恢复数据库 """
        pass


class StorePool(object):
    INC = 5
    MAX_SIZE = 100
    def __init__(self, store):
        self.started = False
        self.store = store
        self.set_size = store.pool_set_size
        self.get_size = store.pool_get_size
        self.pool_get = Pool(size=self.get_size)
        self.pool_set = Pool(size=self.set_size)
        self.quese_set = Queue()
        self._check_task = None
        self._set_task = None


#统计数据
        self.set_count = 0
        self.set_step_count = 0
        self.get_count = 0
        self.get_step_count = 0

    def start(self):
        if self.started:
            return
        self.started = True
        self._check_task = spawn(self._check_loop)
        self._set_task = spawn(self._process_set)


    def stop(self):
        if not self.started:
            return
        self.started = False
        log.info("wait for store:%s", self.store.db_name)
        self.pool_get.join()
        self.pool_set.join()
        log.info("end wait for store")
        self._check_task.kill()
        self._set_task.kill()


    def _set(self, store_func, *args, **kw):
        self.quese_set.put((store_func, args, kw))

    def _get(self, store_func, *args, **kw):
        self.get_count += 1
        self.get_step_count += 1
        return store_func(*args, **kw)

    def _inc_pool(self, pool, num):
        """ inc pool size """
        if pool.size >= self.MAX_SIZE:
            return
        log.warn('[StorePool]pool inc:+%d / %d', num, pool.size)
        pool.size += num
        for i in xrange(num):
            pool._semaphore.release()

    def _dec_pool(self, pool, num):
        """ inc pool size """
        for i in xrange(num):
            pool._semaphore.acquire()

    def pool_counter(self, pool):
        return pool._semaphore.counter

    def _check_set(self):
        set_size = self.quese_set.qsize()
        if set_size >= self.pool_set.size and self.set_step_count == 0:
            self._inc_pool(self.pool_set, self.INC)

    def _check_loop(self):
        """ 检查 """
        pass_time = 60
        while 1:
            spawn(self._check_set)
            sleep(pass_time)
            self._log_info(pass_time)

    def _log_info(self, pass_time):
        if self.quese_set.qsize() != 0 or self.set_step_count != 0 or\
           self.get_step_count > 100: #空闲时候也会读数据
            p = self.set_step_count / float(pass_time)
            p_get = self.get_step_count / float(pass_time)
            log.info("[StorePool-%s]set:::size:%d, total:%d, %d, %.2f c/s:::, get:::size:%d, total:%d, %d, %.2f",
                self.store.db_name,
                self.pool_set.size, self.set_count, self.set_step_count, p,
                self.pool_get.size, self.get_count, self.get_step_count, p_get)
        self.set_step_count = 0
        self.get_step_count = 0

    def _process_set(self):
        """ 取出set任务,放到pool中运行 """
        from .errors import ConnectionError
        def _set_data(func, args, kw):
            self.set_count += 1
            self.set_step_count += 1
            while 1:
                try:
                    return func(*args, **kw)
                except ConnectionError as e:
                    #链接错误,尝试重新保存,保证数据安全
                    log.error('_process_set error:%s, will retry:%s', e, (func, args, kw))
                except:
                    log.log_except('_process_set:%s', (func, args, kw))
                    break
                sleep(0.1)

        while 1:
            func, args, kw = self.quese_set.get()
            self.pool_set.spawn(_set_data, func, args, kw)


class CacheStore(Store):
    """ 缓存存储类 """
    def init(self, url, **dbkw):
        self.pool_get_size = dbkw.pop('pool_get_size', 10)
        self.pool_set_size = dbkw.pop('pool_set_size', 10)
        super(CacheStore, self).init(url, **dbkw)
        self.pool = StorePool(self)
        self._set = self.pool._set
        self._get = self.pool._get
        self.cache_tnames = set()

    def init_cache(self):
        #self.cache = memory_cache.HitMemCache(size=5000)
        if 0:
            from .cache import StoreCache
            self.cache = StoreCache()
        raise NotImplementedError

    def start(self):
        super(CacheStore, self).start()
        self.pool.start()
        if self.cache_tnames:
            self.init_cache()

    def stop(self):
        self.pool.stop()

    def _cache_set(self, tname, key, value):
        if tname not in self.cache_tnames:
            return
            #if '_id' in value:
        #    log.log_stack('load _cache_set:%s', value)
        self.cache.set(tname, key, value)

    def _cache_get(self, tname, key):
        if tname not in self.cache_tnames:
            return
        return self.cache.get(tname, key)

    def insert(self, tname, values):
        """ 新增,返回key """
        kv = super(CacheStore, self).insert(tname, values)
        self._cache_set(tname, kv, values)
        return kv

    def inserts(self, tname, values_list):
        """ 批量新增,返回key """
        keys = super(CacheStore, self).inserts(tname, values_list)
        for i, k in enumerate(keys):
            self._cache_set(tname, k, values_list[i])
        return keys

    def save(self, tname, values):
        """ 保存,values必须包含key """
        kn = self.store.get_key(tname)
        self._cache_set(tname, values[kn], values)
        super(CacheStore, self).save(tname, values)

    def saves(self, tname, values_list):
        """ 批量修改 """
        kn = self.store.get_key(tname)
        for values in values_list:
            self._cache_set(tname, values[kn], values)
        super(CacheStore, self).saves(tname, values_list)

    def has(self, tname, key):
        values = self._cache_get(tname, key)
        if values is not None:
            return True
        return super(CacheStore, self).has(tname, key)

    def load(self, tname, key):
        values = self._cache_get(tname, key)
        if values is not None:
            #if '_id' in values:
            #    log.error('load _cache_get(%s):%s', self.cache, values)
            return values
        values = super(CacheStore, self).load(tname, key)
        if values:
            #if '_id' in values:
            #    log.error('load load:%s', values)
            self._cache_set(tname, key, values)
        return values

    def clear(self, tname):
        if tname in self.cache_tnames:
            self.cache.tb_clear(tname)
        super(CacheStore, self).clear(tname)

    def delete(self, tname, key):
        if tname in self.cache_tnames:
            self.cache.delete(tname, key)
        return super(CacheStore, self).delete(tname, key)

    def update(self, tname, key, values):
        if tname in self.cache_tnames:
            c = self._cache_get(tname, key)
            if c is not None:
                c.update(values)
                self._cache_set(tname, key, c)
        return super(CacheStore, self).update(tname, key, values)


