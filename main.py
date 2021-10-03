import tornado
from tornado import web
from tornado.ioloop import IOLoop
from tornado.options import options

from views import FiscalServiceView

options.define(
    'port',
    default=8888,
    help='port to listen on',
)


def main():
    application = tornado.web.Application([
        (r"/([^/]+)", FiscalServiceView),
    ])
    application.listen(options.port)
    print(f'Listening on http://localhost:{options.port}')
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
