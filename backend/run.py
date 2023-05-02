from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer

from zvms import create_app

wsgi = WSGIContainer(create_app())
server = HTTPServer(wsgi)

if __name__ == '__main__':
    print('服务开始')
    server.listen(11451)
    IOLoop.instance().start()