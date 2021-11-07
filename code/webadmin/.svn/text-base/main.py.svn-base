#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webadmin.application import create_app

def main():
    app = create_app()
    port = int(app.config.get('SERVER_HOST_PORT'))
    if not app.debug:
        from gevent.pywsgi import WSGIServer
        svr = WSGIServer(('0.0.0.0', port), app)
        svr.environ['SERVER_NAME'] = 'webadmin'
        svr.serve_forever()
    else:
        app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
