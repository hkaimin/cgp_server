#!/usr/bin/env python
# -*- coding:utf-8 -*-

from StringIO import StringIO

AIS = {
    u'判断': 'IFNode',
    u'顺序': 'OrderNode',
    u'循环': 'LoopNode',
    u'动作': 'ActionNode',
    u'脉冲': 'ImpulseNode',
    u'跳转': 'SwitchNode',
    }

T = '	'
CR = '\n'


class BaseFreemind(object):
    def ai_by_file(self, fm_file):
        """  """
        with open(fm_file, 'rb') as f:
            return self.ai(f)

    def ai_by_data(self, fm_data):
        """  """
        sio = StringIO(fm_data)
        return self.ai(sio)

    def _code_append(self, code, codes, spaces=T):
        codes.append(spaces + code)

    def _parse_ai(self, text):
        """ 解释节点内容:
            ai, doc, condition, params
        """
        index = 0
        #ai, doc, condition, params = '', '', '', ''
        parts = ['', '', '', '']
        i = 0
        while index < len(text):
            if text[index] == '-' and i <= 1:
                i = 1
            elif text[index] == '@':
                i = 2
            elif text[index] == '#':
                i = 3
            else:
                parts[i] += text[index]
            index += 1
        return parts

    def _parse_ai_node(self, node):
        """ ai解释 """
        pass

    def _iter_ai_node(self, root_node, level):
        pnodes = [root_node]
        nodes = []
        for i in xrange(level):
            for p in pnodes:
                nodes.extend(p.getchildren())
            pnodes, nodes = nodes, []
        for n in pnodes:
            yield n

    def ai(self, freemind, level=2):
        """ param reemind: 输入freemind的文件内容,
            param level: ai节点所在层
            返回:ai脚本字符串
        """

        import xml.etree.ElementTree as etree
        doc = etree.ElementTree()
        doc.parse(freemind)

        root = doc.find('node')
        ai_py = {}
        for n in self._iter_ai_node(root, level):
            try:
                ai_id, ai_doc, codes = self._parse_ai_node(n)
                if codes:
                    ai_py[ai_id] = (ai_doc, codes)
            except StandardError as e:
                print u'aicode_error: 处理节点(%s)错误' % n.get('TEXT'), str(e)
                import traceback
                traceback.print_exc()

#        #保存
#        ai = '\n'.join(ai_py)
#        return ai.encode('utf-8')
        return ai_py


class Freemind2AI(BaseFreemind):
    def __init__(self):
        pass

    def _parse_node(self, node, codes, index=0, spnode=''):
        """ 分析单个节点 """
        text = node.get('TEXT')
        if text[:3] == 'AI-':
            #子节点
            ai_id, ai_doc = text[3:].split('-', 1)
            self._code_append('%s.add_child(get_ai(%s)())'%(spnode, ai_id.strip()), codes)
            return
        if text[0] == '#': #注释
            return
        ai, doc, condition, params = self._parse_ai(text)
        #创建
        name = '%s_%d' % (spnode, index) if spnode else 'node_%d' % index
        n = AIS.get(ai.strip(), None)
        if n is None:
            raise ValueError, u'节点(%s)类型解释错误' % text
        if params.strip():
            self._code_append('%s = %s("%s")'%(name, n, params.strip()), codes)
        else:
            self._code_append('%s = %s()'%(name, n, ), codes)
            #name
        if doc.strip():
            self._code_append('%s.name = u"%s"'%(name, doc.strip()), codes)
            #条件
        if condition.strip():
            if n in ['ActionNode']:
                func = 'set_action'
            else:
                func = 'set_condition'
            self._code_append('%s.%s("%s")'%(name, func, condition.strip()), codes)
        if spnode:
            self._code_append('%s.add_child(%s)'%(spnode, name), codes)
            #
        children = node.getchildren()
        for index, n in enumerate(children):
            self._parse_node(n, codes, index=index, spnode=name)
        return name

    def _parse_ai_node(self, node):
        """ ai解释 """
        text = node.get('TEXT')
        if text[:3] != 'AI-':
            return None, None, None
        codes = [
            '#!/usr/bin/env python',
            '# -*- coding:utf-8 -*-',
            '',
        ]
        ai_id, ai_doc = text[3:].split('-', 1)
#        codes.append('@wrap_register(%s)' % ai_id.strip())
        codes.append('def ai_%s():' % ai_id.strip())
        codes.append(T + '""" %s """' % ai_doc)
        children = node.getchildren()
        for index, n in enumerate(children):
            #应该只有一个node
            name = self._parse_node(n, codes, index=index)
            codes.append(T + 'return %s' % name)
            codes.append(CR)
            return ai_id, ai_doc, codes


class Freemind2Py(BaseFreemind):
    """ 翻译成py代码, 决策树用 """
    def _parse_LoopNode(self, codes, condition, params, spaces):
        """ 循环 """
        params = eval('dict(%s)' % params)
        self._code_append('for i in xrange(%s):' % params['times'], codes, spaces=spaces)

    def _parse_IFNode(self, codes, condition, params, spaces):
        self._code_append('if %s:' % condition, codes, spaces=spaces)

    def _parse_ActionNode(self, codes, condition, params, spaces):
        self._code_append('%s' % condition, codes, spaces=spaces)

    def _parse_OrderNode(self, codes, condition, params, spaces):
        self._code_append('if 1:', codes, spaces=spaces)

    def _parse_node(self, node, codes, spaces=''):
        """ 分析单个节点 """
        text = node.get('TEXT')

        print "~", text

        if text[0] == '#': #注释
            return

        if text[:3] == 'AI-':
            #子节点
            ai_id, ai_doc = text[3:].split('-', 1)
            self._code_append('ai_%s(**kw))'%(ai_id.strip(), ), codes)
            return

        ai, doc, condition, params = self._parse_ai(text)
        #创建
        n = AIS.get(ai.strip(), None)
        if n is None:
            raise ValueError, u'节点(%s)类型解释错误' % text
        func = getattr(self, '_parse_%s' % n)
        if doc:
            self._code_append('#%s' % doc, codes, spaces=spaces)
        func(codes, condition, params, spaces)
        children = node.getchildren()
        for index, n in enumerate(children):
            self._parse_node(n, codes, spaces=spaces+T)

    def _parse_ai_node(self, node):
        """ ai解释 """
        text = node.get('TEXT')
        if text[:3] != 'AI-':
            return None, None, None
        codes = [
            '#!/usr/bin/env python',
            '# -*- coding:utf-8 -*-',
            '',
            ]

        print "~~~~~~", text
        ai_id, ai_doc = text[3:].split('-', 1)
        codes.append('def ai_%s(**kw):' % ai_id.strip())
        codes.append(T + '""" %s """' % ai_doc)

        #todo 用特殊做法,让kw的内容进入函数内,只支持py2.x,
        codes.append(T + 'locals().update(kw);exec "";')

        children = node.getchildren()
        for index, n in enumerate(children):
            #应该只有一个node
            print "--->", index, n
            self._parse_node(n, codes, spaces=T)
            codes.append(CR)
            return ai_id, ai_doc, codes

