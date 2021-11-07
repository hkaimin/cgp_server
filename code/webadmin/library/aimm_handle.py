#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .free_mind import Freemind2Py

fm2py = Freemind2Py()

class AimmFile(object):

    def __init__(self, file_contents):
        self.file_contents = file_contents
        self.init_docs()

    def init_docs(self):
        nodes = fm2py.ai_by_data(self.file_contents)
        self.docs = {}
        for id, (name, code) in nodes.iteritems():
            id = int(id)
            code = '\n'.join(code).strip();
            doc = {'_id': id, 'name': name, 'code': code}
            self.docs[id] = doc

    def diff(self, src_docs):
        ''' 和已有的 docs 比较 '''

        create = []
        update = []
        for id, doc in self.docs.iteritems():
            if doc['_id'] in src_docs:
                update.append(id)
            else:
                create.append(id)

        remove = []
        for src_id, src_doc in src_docs.iteritems():
            if src_doc['_id'] not in self.docs:
                remove.append(src_id)

        return dict(create=create, update=update, remove=remove)

