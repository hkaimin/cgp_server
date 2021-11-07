#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import copy
import cPickle as pickle
import math
import array
import base64
import bisect
import ubson

from corelib import log

try:
    import ujson as json
    is_ujson = True
except ImportError:
    import json
    is_ujson = False

pickle_dumps, pickle_loads = pickle.dumps, pickle.loads

def json_dumps(data, ensure_ascii=False):
    """
    ensure_ascii=False时,json输出unicode, ujson输出utf8str
            u'[1, 2, 3, "\u4e2d\u56fd"]'
            '[1,2,3,"\xe4\xb8\xad\xe5\x9b\xbd"]'
        =True时,如果有unicode对象,json和ujson都会输出错误的编码
            '[1, 2, 3, "\\u4e2d\\u56fd"]'
            '[1,2,3,"\\u4e2d\\u56fd"]'

    """
    try:
        if is_ujson:
            s = json.dumps(data, ensure_ascii=False)
        else:
            s = json.dumps(data, ensure_ascii=False,
                default=str,
                separators=(',', ':'))
    except:
        log.log_except("data:%s", data)
        raise
    if ensure_ascii and isinstance(s, unicode):
        return s.encode('utf-8')
    return s

json_loads = json.loads

def bson_dumps(data):
    try:
        s = ubson.dumps(data)
    except:
        log.log_except("data:%s", data)
        raise

    return s

ubson_loads = ubson.loads

def module_to_dict(md):
    """ 过滤模块内容,返回可序列化的数据对象 """
    d1 = {}
    for name in dir(md):
        if name.startswith('_'):
            continue
        value = getattr(md, name)
        if type(value) not in (bool, int, str, unicode, float, tuple, list, dict):
            continue
        d1[name] = value
    return d1

def dict_key_int_to_str(obj):
    """
    {1:1} -> {"1":1}
    """
    adict = {}
    if isinstance(obj, dict):
        for key, value in obj.iteritems():
            adict[str(key)] = dict_key_int_to_str(value)
        return adict
    else:
        return obj

def dict_key_str_to_int(obj):
    """
    {"1":1} -> {1:1}
    """
    adict = {}
    if isinstance(obj, dict):
        for key, value in obj.iteritems():
            try:
                adict[int(key)] = dict_key_str_to_int(value)
            except ValueError:
                adict[key] = dict_key_str_to_int(value)
        return adict
    else:
        return obj

def str2dict(s, ktype=str, vtype=int):
    """ k:v|k1:v|...
    返回: {k:v, k1:v, ... }
    """
    s = s.strip()
    if not s:
        return
    rs = dict(map(lambda kv: (ktype(kv[0]), vtype(kv[1])),
        map(lambda i: i.strip().split(':'), s.split('|'))))
    return rs

def str2dict1(s):
    """level:1|role:7|role:8|task:1|obj:1:3|equ:5 -->
    {level:[1,], role:[7,8], ...}"""
    if not s:
        return
    rs = {}
    for i in s.split('|'):
        v = i.split(':')
        rs[v[0]] = v[1:]
    return rs

def str2dict2(s):
    """ a:a1:a2:a3|b:b1:b2:b3|c:c1:c2:c3 -->
        {a:[a1,a2,a3], b:[b1,b2,b3], c:[c1,c2,c3]}
    """
    if not s:
        return
    rs = {}
    for i in s.split('|'):
        v = i.split(':')
        rs[v[0]] = v[1:]
    return rs

def str2dict3(s):
    """ a:a1:a2:a3|b:b1:b2:b3|c:c1:c2:c3 -->
        {a:[(a1,a2,a3)], b:[(b1,b2,b3)], c:[(c1,c2,c3)]}
    """
    if not s:
        return
    rs = {}
    for i in s.split('|'):
        v = i.split(':')
        d = rs.setdefault(v[0], [])
        d.append(v[1:])
    return rs

def str2list(s, vtype=int):
    """ 1|2|3|4|5
    返回: [1,2,3,4,5]
    """
    if not s:
        return
    rs = []
    rs = s.split('|')
    rs = map(vtype, rs)
    return rs

def make_lv_regions(regions, accept_low=1):
    """ 实现根据等级获取对应物品功能, regions=[(lv,i), ...]
    @param:
        accept_low: 小于最小值时,是否返回最小值, false=返回None
    """
    if isinstance(regions, (str, unicode)):
        #格式:0:1|10:2|30:3  [0,10)范围对应id=1, [10,30)范围对应id=2, [30,~)范围对应id=3
        regions = map(lambda i: tuple(map(int, i.strip().split(':'))), regions.split('|'))
    else:
        regions = map(lambda v: (int(v[0]), v[1]), regions)
    regions.sort()
    lvs = list(r[0] for r in regions)
    def _lv_regions(lv):
        i = bisect.bisect_right(lvs, lv) - 1
        if i < 0:
            if not accept_low:
                return None
            i = 0
        return regions[i][1]
    return _lv_regions

def make_lv_regions_list(regions, accept_low=1):
    """ 实现根据等级获取对应物品功能, regions=[(lv,i), ...] """
    if isinstance(regions, (str, unicode)):
        #格式:0:1:1|10:2:2|30:3:3  [0,10)范围对应id=1,1, [10,30)范围对应id=2,2, [30,~)范围对应id=3,3
        regions = map(lambda i: tuple(map(int, i.strip().split(':'))), regions.split('|'))
    else:
        regions = map(lambda v: (int(v[0]), v[1]), regions)
    regions.sort()
    lvs = list(r[0] for r in regions)
    def _lv_regions(lv):
        i = bisect.bisect_right(lvs, lv) - 1
        if i < 0:
            if not accept_low:
                return None
            i = 0
        return regions[i][1:]
    return _lv_regions

def decode_dict(adict, ktype=None, vtype=None):
    data = copy.deepcopy(adict)
    tmp = {}
    for k,v in data.iteritems():
        tk, tv = k, v
        if ktype is not None:
            tk = ktype(k)
        if vtype is not None:
            tv = vtype(v)
        tmp[tk] = tv
    return tmp

def decode_list(alist, type=int):
    tmp = []
    for v in alist:
        tmp.append(type(v))
    return tmp

def pack_json_pb2(pb2obj, data):
    """打包成json格式pb2数据"""
    res = pb2obj.res.add()
    for k, v in data.iteritems():
        res.keys.append(k)
        try:
            if isinstance(eval(v), dict):
                res.params.append(json.dumps(eval(v)))
            else:
                res.params.append(v)
        except:
            res.params.append(v)
    return res


def field_dumps(value, protocol=0):
    if hasattr(value, 'dumps'):
        return value.dumps()
    else:
        return pickle.dumps(value, protocol)

def field_loads(data):
    if data:
        #修复win系统,由于浮点型数据异常，引起cPickle downs,loads报错
        if sys.platform == 'win32' and '-1.#IN' in data:
            data = data.replace('-1.#IND', '0')
            data = data.replace('1.#INF', '0')
        try:
            return pickle.loads(data)
        except StandardError, e:
            #对象持续化错误，可能对象属性变了或者py版本变了？
            log.exception(e)

class Pickler:
    dumps = staticmethod(field_dumps)
    loads = staticmethod(field_loads)

#######使用zlib压缩的###############
from zlib import compress, decompress
_zlib_length = 1024
def zlib_field_dumps(value, protocol=2):
    data = field_dumps(value, protocol)
    if len(data) > _zlib_length:
        return compress(data, 1)
    return data

def zlib_field_loads(data):
    try:
        data1 = decompress(data)
    except Exception:
        data1 = data
    return field_loads(data1)

class ZlibPickler:
    dumps = staticmethod(zlib_field_dumps)
    loads = staticmethod(zlib_field_loads)


class CustomObject(object):
    def __str__(self):
        return u'%s(%s) at %s' % (self.__class__.__name__, self.__dict__, id(self))

    def __repr__(self):
        return self.__str__()

class SoltObject(object):
    """  """
    def __getstate__(self):
        d1 = {}
        for k in self.__slots__:
            d1[k] = getattr(self, k)
        return d1

    def __setstate__(self, adict):
        for k in self.__slots__:
            if not k in adict:
                continue
            setattr(self, adict[k])

INF = 1e10000
INFS = (-INF, INF)
POS_MAX = 999999
class Position(object):
    __slots__ = ('x', 'y', 'h')
    def __init__(self, x=0, y=0, h=0):
        self.x = x
        self.y = y
        self.h = h

    def __getstate__(self):
        return dict(x=self.x, y=self.y, h=self.h)

    def __setstate__(self, adict):
        self.x = adict['x']
        self.y = adict['y']
        self.h = adict['h']

    ##    def _set_h(self, v):
    ##        self._h = v
    ##    def _get_h(self):
    ##        return self._h
    ##    h = property(_get_h, _set_h)

    def __str__(self):
        return '%s(x=%f, y=%f, h=%f)' % (self.__class__.__name__, self.x, self.y, self.h)

    def __repr__(self):
        name = super(Position, self).__repr__()
        return '%s(x=%f, y=%f, h=%f)' % (name, self.x, self.y, self.h)

    def __mul__(self, other):
        """ 乘算法 """
        new = self.clone()
        if isinstance(other, (int, float)) and other not in INFS:
            new.x *= other
            new.y *= other
            new.h *= other
        return new

    def __div__(self, other):
        """ 除 """
        new = self.clone()
        if isinstance(other, (int, float)) and other != 0 and other not in INFS:
            new.x /= other
            new.y /= other
            new.h /= other
        return new

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.h

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.h
        raise IndexError, 'key out of (0, 1, 2)'

    def clear(self):
        self.x = 0
        self.y = 0
        self.h = 0

    def assign_by(self, pos):
        if -POS_MAX < pos.x < POS_MAX:
            self.x = pos.x
        if -POS_MAX < pos.y < POS_MAX:
            self.y = pos.y
        if -POS_MAX < pos.h < POS_MAX:
            self.h = pos.h

    def assign_to(self, pos):
        if -POS_MAX < self.x < POS_MAX:
            pos.x = self.x
        if -POS_MAX < self.y < POS_MAX:
            pos.y = self.y
        if -POS_MAX < self.h < POS_MAX:
            pos.h = self.h

    def clone(self):
        pos = self.__class__(self.x, self.y, self.h)
        return pos

    def add(self, pos):
        self.x += pos.x
        self.y += pos.y
        self.h += pos.h

    def dec(self, pos):
        self.x -= pos.x
        self.y -= pos.y
        self.h -= pos.h

    def distance(self):
        """ 二维：离原点距离 """
        return abs(math.sqrt(pow(self.x, 2) + pow(self.y, 2)))

    def distance_xy(self, pos):
        """ 二维：到pos的距离 """
        return abs(math.sqrt(pow(self.x-pos.x, 2) + pow(self.y-pos.y, 2)))

    def distance_xyz(self, pos):
        """ 三维：到pos的距离 """
        return abs(math.sqrt(pow(self.x-pos.x, 2) + pow(self.y-pos.y, 2) + pow(self.h - pos.h, 2)))

    def in_distance_xy(self, pos, distance):
        """ 二维：判断是否在xy范围内 """
        return not ((abs(self.x - pos.x) > distance) or (abs(self.y - pos.y) > distance))

    def get_direct(self, pos):
        """ 获取当前点到目标点的方向值, """
        dis_x = int(pos.x) - int(self.x)
        dis_y = int(pos.y) - int(self.y)
        return get_move_direction(dis_x, dis_y)

#    def end_pos(self, distance, speed):
#        """ 根据 """
#        rate = distance / speed.distance()
#        end = Position(self.x * rate, self.y * rate, self.h)
#        return end

class Speed(Position):
    __slots__ = ('x', 'y', 'h')
    def speed_for_time(self, time):
        return Speed(self.x * time, self.y * time, self.h * time)

    def speed_by_vector(self, v_speed):
        """ 根据向量速度，设置速度和移动方向，其中z轴和xy轴处理不同；
            z轴和移动方向没关系，用正负代表方向
        """
        self.x = abs(v_speed.x)
        self.y = abs(v_speed.y)
        self.h = v_speed.h

#根据系统位数,选择合适的类型
sizeof_digit = sys.long_info.sizeof_digit
if sizeof_digit == 2:#32位系统
    UNIT = 'L'
elif sizeof_digit >= 4:#64位系统, pypy是8?
    UNIT = 'I'
else:
    raise ValueError('sys.long_info.sizeof_digit error:%s' % sizeof_digit)

class IntBiteMap(object):
    """
    说明：正整数biteMap
    """
    __slots__ = ('len', 'map')
    def __init__(self):
        self._init_map()

    def _init_map(self, data=None):
        if data:
            self.len = len(data) / 4
            self.map = array.array(UNIT, str(data))
        else:
            self.len = 0
            self.map = array.array(UNIT)
            #for i in xrange(151):
            #    self.insert(i)
            #log.debug('_init_map(data=%s):%s', data, self.map)

    def __getstate__(self):
        return self.len, self.map

    def __setstate__(self, data):
        self.len, self.map = data

    def _inc_map(self, len):
        #step = 0 #每次增加时，增加多1字节
        inc = len - self.len# + step
        self.len = len# + step
        self.map.extend((0L, ) * inc)

    @property
    def max_int(self):
        return self.len * 32

    def _value(self, insert, value):
        len = (value+1) / 32 + 1
        if len >= self.len:
            self._inc_map(len)
        index_Hash = value / 32 % self.len
        index_int = value % 32
        if insert:
            self.map[index_Hash] = (self.map[index_Hash] | (1<<index_int))
        else:
            self.map[index_Hash] = (self.map[index_Hash] & ~(1<<index_int))

    def clear(self):
        self._init_map()

    def insert(self, value):
        self._value(1, value)

    def delete(self, value):
        self._value(0, value)

    def trunate(self, value):
        """ 切去大于value的数据 """
        len = (value+1) / 32 + 1
        if len >= self.len:
            return
        index_Hash = value / 32 % self.len
        index_int = value % 32
        self.map = self.map[:index_Hash+1]
        for i in xrange(index_int+1, 32):
            self.map[index_Hash] = (self.map[index_Hash] & ~(1<<i))

    def __iter__(self):
        bi = 0
        for i in xrange(self.len):
            v = self.map[i]
            if not v:
                bi += 32
                continue

            for j in xrange(32):
                bi += 1
                if v & (1<<j):
                    yield bi



    def __contains__ (self, value):
        if  value >= self.len * 32:
            return False
        try:
            index_Hash = value / 32 % self.len
            index_int = value % 32
            if (self.map[index_Hash] & (1<<index_int)):
                return True
            else :
                return False
        except:
            log.log_except('map=%s, len=%s, ih=%s, ii=%s, value=%s',
                self.map, self.len, index_Hash, index_int, value)

    def __str__(self):
        return self.to_string()

    def to_string(self):
        return str(self.map.tostring())

    def from_string(self, data):
        self._init_map(data=data)

    def to_base64(self):
        return base64.b64encode(str(self.map.tostring()))

    def from_base64(self, data):
        data = str(data)
        try:
            data = base64.b64decode(str(data))
            self.from_string(data)
        except TypeError:
            self.from_string(data)

    @classmethod
    def new(cls, data):
        m = cls()
        m.from_string(data)
        return m

    @classmethod
    def new_base64(cls, data):
        m = cls()
        m.from_base64(data)
        return m

def test_IntBiteMap():
    bm = IntBiteMap()
    #bm.from_base64('/v8PAA==')
    assert bm.len == 0
    #bm.insert(99)
    bm.insert(10)
    assert 10 in bm and bm.len == 1
    bm.insert(32)
    assert 32 in bm and bm.len == 2
    bm.insert(62)
    assert 62 in bm and bm.len == 2
    bm.insert(64)
    assert 64 in bm and bm.len == 3
    for i in xrange(330):
        bm.insert(i)
        assert i in bm
    print bm.map

    bm.trunate(100)
    for i in xrange(101, 330):
        assert i not in bm

    s = bm.to_string()
    bm1 = IntBiteMap.new(s)
    assert 64 in bm1 and 62 in bm1 and 32 in bm1 and 10 in bm1
    IntBiteMap.new('')

class IntRegionMap(object):
    """ 针对任务等级,定义的一种结构,
    解释: (1, 10): t1, (2, 15): t2, (5, 10):t3,
    {level:[t1, t2, t3]}
    """
    def __init__(self):
        self.get_func = None
        self.tmps = {}
        self.keys = None
        self.items = None

    def add(self, start, end, value):
        """ 左开右闭 """
        self.tmps[(int(start), int(end))] = value

    def init(self):
        keys = set()
        for start, end in self.tmps.iterkeys():
            keys.add(start)
            keys.add(end)
        keys = list(keys)
        keys.sort()
        self.keys = keys
        self.items = items = {}
        for (start, end), value in self.tmps.iteritems():
            for k in keys:
                values = items.setdefault(k, [])
                if not (start <= k < end):
                    continue
                values.append(value)
        self.get_func = make_lv_regions(items.items(), accept_low=0)

    def get(self, key):
        return self.get_func(key)

    def gets(self, start, end):
        """ [start, end] 获取这个范围段所有数据 """
        if not self.keys:
            return []
        rs = set()
        for k in self.keys:
            if start <= k <= end:
                rs.update(self.get_func(k))
        return rs

def test_IntRegionMap():
    m = IntRegionMap()
    m.add(2, 10, 1)
    m.add(5, 11, 2)
    m.add(5, 15, 3)
    m.init()
    l = m.get(5)
    l1 = m.get(10)
    l0 = m.get(1)


class TrieNode:
    def __init__(self, pnode):
        self.pnode = pnode
        self.value = None
        # children is of type {char, Node}
        self.children = {}
        self.end = 0 #是否叶子节点

    def get_value(self):
        if self.value is None:
            return ''
        return '%s%s' % (self.pnode.get_value(), self.value)

class Trie:
    def __init__(self):
        self.root = TrieNode(None)

    def insert(self, key):      # key is of type string
        # key should be a low-case string, this must be checked here!
        if not key:
            return None
        node = self.root
        for char in key:
            if char not in node.children:
                child = TrieNode(node)
                node.children[char] = child
                node = child
                child.value = char
            else:
                node = node.children[char]
        node.end = 1

    def search(self, key):
        node = self.root
        for char in key:
            if char not in node.children:
                break
            else:
                node = node.children[char]
        return node.end

    def searchs(self, s, full=1):
        """ 搜索句子,得到单词列表,
        full=0, 用于检查是否有单词在s中
        """
        pos = 0
        rs = None
        if full:
            rs = []
        while pos < len(s):
            node = self.root
            enode = None
            for char in s[pos:]:
                if char not in node.children:
                    break
                node = node.children[char]
                if node.end:
                    enode = node
            if enode:
                if full:
                    rs.append(enode.get_value())
                else:
                    return enode
            pos += 1
        return rs

    def display_node(self, node, log=None):
        def _log(n):
            if log is not None:
                log(n.get_value())
            else:
                print n.get_value()
        if node.end:
            _log(node)
        for key in node.children.iterkeys():
            self.display_node(node.children[key], log=log)
        return

    def display(self, log=None):
        self.display_node(self.root, log=log)

    @classmethod
    def test(cls):
        trie = cls()
        trie.insert('hello')
        trie.insert('nice')
        trie.insert('to')
        trie.insert('meet')
        trie.insert('you')
        trie.insert(u'中文')
        trie.insert(u'可以')
        trie.display()
        print 'search(hello):', trie.search('hello')
        print 'search(HELLO):', trie.search('HELLO')
        print(trie.searchs(u'中文是否可以ad找到to呢？' ))
        trie.benchmark()

    def benchmark(self, n=1000000):
        import timeit
        s = u'主席你好啊'
        def _ban():
            self.searchs(s, full=0)
        use = timeit.timeit(_ban, number=n)
        print 'used:%s per:%f' % (use, use / float(n))

    def replaces(self, s, ch):
        """ 将敏感词替换成ch """
        orig = s
        s = orig.lower()
        l = len(s)
        ch = unicode(ch)
        for i in xrange(0, l, 1):
            node = self.root
            e = 0
            for j in xrange(i, l, 1):
                k = s[j:j+1]
                if k not in node.children:
                    break
                node = node.children[k]
                if node.end:
                    e = j
            if not e:
                continue
            orig = orig[:i] + (e-i+1)*ch + orig[e+1:]
        #            orig[i:e+1] = (e-i+1)*ch
        #            orig = orig[:j] + ch + orig[j+1:]
        return orig


def encode(u):
    if not isinstance(u, unicode):
        u = u.decode('utf8')
    return u.encode('utf16')[2:]

def decode(s):
    return s.decode('utf16')

def main():
    #test_IntBiteMap()
    #test_IntRegionMap()
    pass

if __name__ == '__main__':
    main()
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------


