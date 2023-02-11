from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer

from zvms import app

wsgi = WSGIContainer(app)
server = HTTPServer(wsgi)

if __name__ == '__main__':
    server.listen(1145)
    IOLoop.instance().start()