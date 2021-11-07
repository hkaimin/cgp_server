#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from corelib import log
from corelib.process import BaseApp, daemon
import config


class Application(BaseApp):

    def __init__(self):
        BaseApp.__init__(self)

    def start(self):
        log.warn('run...')
        sys.argv.insert(1, 'webadmin')
        from webadmin.main import main
        main()

def main():
    log.warning("admin_path:::%s", config.admin_path)
    sys.path.insert(0, config.admin_path)
    app = Application()
    daemon(app)
