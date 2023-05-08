(import tornado.ioloop [IOLoop]
        tornado.wsgi [WSGIContainer]
        tornado.httpserver [HTTPServer])

(import zvms [create-app])

(when (= __name__ "__main__")
  (let [wsgi (WSGIContainer (create-app))
        server (HTTPServer wsgi)]
    (print "服务开始")
    (server.listen 11452)
    (.start (IOLoop.instance))))