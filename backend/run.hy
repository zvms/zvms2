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
           server (HTTPServer wsig)) 
     (server.listen 11452) 
     (.start (IOLoop.instance))
     (except [KeyboardInterrupt]
             (setv zvms (reload zvms))))))