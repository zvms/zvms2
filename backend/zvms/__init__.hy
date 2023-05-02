(defn create-app []
  (import flask [Flask]
          flask_cors [CORS])
  
  (import zvms.res [STATIC_FOLDER])

  (import zvms.config :as config)
  (setv app (Flask __name__))
  (CORS app :supports_credential True
        :resources #{"/*" "*"}
        :max_age 600)
  (app.config.from_object config)
  (setv app.static_folder STATIC_FOLDER)
  
  (.push (app.test_request_context))
  
  ((app.errorhandler 404) (fn [e]
                            #({"type" "ERROR"
                               "message" "请求地址错误"}
                              404)))
  ((app.errorhandler 500) (fn [e]
                            #({"type" "ERROR"
                               "message" "服务器内部错误"}
                              500)))
  
  (import zvms.tokenlib :as tk
          zvms.views
          zvms.views.notice [load_public_notice]
          zvms.apilib [Api]
          zvms.models [db])
  
  (load_public_notice)
  
  (tk.init_app app)
  (Api.init_app app)
  (db.init_app app)
  
  app)