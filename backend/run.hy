(import importlib [reload]
        tornado.ioloop [IOLoop]
        tornado.wsgi [WSGIContainer]
        tornado.httpserver [HTTPServer])

(import zvms)

(require hyrule [defmain])

#^HTTPServer server

(defmain []
  (while True
    (try 
      (setv wsgi (WSGIContainer (zvms.create-app)) 
            server (HTTPServer wsig)) 
      (server.listen 11452) 
      (.start (IOLoop.instance))
      (except [KeyboardInterrupt]
              (setv zvms (reload zvms))))))