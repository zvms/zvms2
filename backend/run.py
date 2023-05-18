from importlib import reload

from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer

import zvms

server: HTTPServer


def start_server():
    global server
    wsgi = WSGIContainer(zvms.create_app())
    server = HTTPServer(wsgi)
    server.listen(11452)
    IOLoop.instance().start()

if __name__ == '__main__':
    while True:
        try:
            start_server()
        except zvms.ZvmsExit:
            server.stop()
            zvms = reload(zvms)