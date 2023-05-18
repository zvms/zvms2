(import importlib [reload]
        tornado.ioloop [IOLoop]
        tornado.wsgi [WSGIContainer]
        tornado.httpserver [HTTPServer])

(import zvms)

#^HTTPServer server

(when (= __name__ "__main__")
 (while True
   (try 
     (setv wsgi (WSGIContainer (zvms.create-app)) 
           server (HTTPServer wsgi)) 
     (server.listen zvms.res.PORT) 
     (print "服务开始")
     (.start (IOLoop.instance))
     (except [zvms.ZvmsExit]
             (setv zvms (reload zvms))))))