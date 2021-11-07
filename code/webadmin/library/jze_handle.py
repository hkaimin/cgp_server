#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import zlib
from collections import OrderedDict
from rd1sdk import aes

AES_KEY = 'xf3R0xdcmx8bxc0J'
encrypter = aes.new_aes_encrypt(AES_KEY)
decrypter = aes.new_aes_decrypt(AES_KEY)

def jze_pack(json_object):
    data = json.dumps(json_object)
    data = zlib.compress(data, 6)
    data = encrypter(data)
    return data

def jze_unpack(data):
    data = decrypter(data)
    data = zlib.decompress(data)
    json_object = json.loads(data, object_pairs_hook=OrderedDict)
    return json_object

class JzeFile(object):

    def __init__(self, file_contents):
        self.file_contents = file_contents
        self.json_object = jze_unpack(self.file_contents)

    @property
    def json_string(self):
        return json.dumps(self.json_object, indent=4)

class JzeCreator(object):

    def __init__(self, docs):
        self.docs = docs
        self.filebytes = jze_pack(docs)


