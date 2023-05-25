(import zvms.apilib [ZvmsExit])

(setv app None)

(defn create-app []
  (import flask [Flask]
          flask-cors [CORS]
          zvms.res [STATIC-FOLDER ErrorCode]
          zvms.config :as config)

  (global app)

  (setv app (Flask __name__))
  (CORS app :supports-credential True
        :resources #{"/*" "*"}
        :max-age 600)
  (app.config.from-object config)
  (setv app.static_folder STATIC_FOLDER)
  
  (.push (app.test-request_context))
  
  ((app.errorhandler 404) (fn [ex]
                            #(#[[{"type": "ERROR", "code": ErrorCode.ERROR-404}]]
                              404)))
  ((app.errorhandler 500) (fn [ex]
                            #(#[[{"type": "ERROR", "code": ErrorCode.ERROR-500}]]
                              500)))
  
  (import zvms.views
          zvms.views.notice [load-main-menu-notice]
          zvms.apilib [Api]
          zvms.models [db])
  
  (load-main-menu-notice)
  
  (Api.init-app app)
  (db.init-app app)
  (db.create-all)
  
  app)