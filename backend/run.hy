(import importlib [reload]
        tornado.ioloop [IOLoop]
        tornado.wsgi [WSGIContainer]
        tornado.httpserver [HTTPServer])

(import zvms)

(require hyrule [defmain])

#^HTTPServer server

(when (= __name__ "__main__")
  (let [wsgi (WSGIContainer (create-app))
        server (HTTPServer wsgi)]
    (print "服务开始")
    (server.listen 11452)
    (.start (IOLoop.instance))))

(defmain []
  (while True
    (try 
      (setv wsgi (WSGIContainer (zvms.create-app)) 
            server (HTTPServer wsig)) 
      (server.listen 11452) 
      (.start (IOLoop.instance))
      (except [KeyboardInterrupt]
              (setv zvms (reload zvms))))))