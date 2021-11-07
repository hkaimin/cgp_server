#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os.path import dirname, abspath
from pprint import pprint

sys.path.append(dirname(dirname(abspath(__file__))))
reload(sys);
sys.setdefaultencoding('utf-8')

from webadmin import default_config as DefaultConfig

sys.modules['config'] = DefaultConfig

from webadmin.application import create_app

def print_endpoints(app):
    keys = app.view_functions.keys()
    keys.sort()
    pprint(keys)

def use_local_database(app):
    for gamesvr in app.extensions['zoning'].gamesvrs.itervalues():
        gamesvr['resource_db'] = 'mongodb://localhost/rich9_res'
        gamesvr['user_db'] = 'mongodb://localhost/rich9'
        gamesvr['logging_db'] = 'mongodb://localhost/rich9_log'

if __name__ == '__main__':
    app = create_app()
    #use_local_database(app)
    #print_endpoints(app)
    app.run(debug=True, host='0.0.0.0')
