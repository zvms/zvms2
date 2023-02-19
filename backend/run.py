from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer

from zvms import create_app

wsgi = WSGIContainer(create_app())
server = HTTPServer(wsgi)

if __name__ == '__main__':
    server.listen(1145)
    IOLoop.instance().start()