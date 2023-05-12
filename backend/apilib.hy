(import functools [wraps]
        pprint [pprint]
        datetime [datetime]
        typing [Callable]
        json
        re
        zvms.util [inexact-now]
        zvms.typing [Processor Any ProcessorError]
        zvms.res [Categ])

(require hyrule *
         zvms.macros *)

(defclass Api []
  (setv #^(of list "Api") apis []
        search-url-params (re.compile r"\<.+?\>"))
  
  (defmth __init__ [rule
                    func
                    [method "GET"]
                    [params Any]
                    [returns Any]
                    [auth Categ.ANY]]
    (Api.apis.append self)
    (setv self.rule rule
          self.func func
          self.url-params {}
          self.method method
          self.params params
          self.returns returns)
    (for [param (Api.search-url-params.findall rule)]
      (if (arg.startswith "<int:")
        (setv (get self.url-params (cut param 5 -1)) "number")
        (setv (get self.url-params (cut param 1 -1)) "string"))))
  (defn init-app [app]
    (for [api Api.apis]
      (app.add-url-rule api.rule 
                        :methods [api.method]
                        :view-func (deco api.func 
                                         api.params
                                         api.returns
                                         api.auth)))))

(setv json-header {"Content-Type": "application/json ; charset=utf-8"})

(defn process [#^Processor proc json #^str msg]
  (try
    (proc.process json)
    (except [ex [ProcessorError]]
            (setv (:msg ex) msg)
            (raise ex))))

(defn deco [#^Callable impl 
            #^Processor params 
            #^Processor response
            #^Categ auth]
  ((wraps impl) 
   (fn [#*args #**kwargs] 
     (import flask [request]
             zvms.models [Issue]
             zvms.tokenlib :as tk)
     (let [json-data (if (in request.method #("GET" "DELETE"))
                       request.args
                       (try
                         (json.loads (. request (get-data) (decode "utf-8")))
                         {}))
           token-data (if (= auth Categ.None)
                        {}
                        (try
                          (let [token-data (request.headers.get "Authorization")]
                            (when (not data)
                              (raise InvalidSignatureError))
                            (setv token-data (tk.read token-data))
                            (cond
                              (not (tk.exists token-data))
                              (return (json.dumps {"type" "ERROR" "message" "Token失效, 请重新登陆"}) json-header)
                              (not (auth.authorized (:auth token-data)))
                              (return (json.dumps {"type" "ERROR" "message" "权限不足"}))
                              True token-data))
                          (except [InvalidSignatureError]
                                  (return (json.dumps {"type" "ERROR" "message" "未获取到Token, 请重新登陆"}) json-header))))]
       (when __debug__
         (with [(open "log.txt" "a" :encoding "utf-8") f]
               (let [log f "{(inexact-now)}[{request.remote-addr}]"]
                 (unless (= auth Categ.None)
                         (+= s f "({(:id token-data)})"))
                 (+= s (+ "[" request.method "]" request.path))
                 (print s)
                 (print s :file f))))
       (try
         (let [json-data (process params json-data "传入的数据错误")
               ret (impl #*args #**kwargs #**json-data :token-data token-data)
               result (:result ret)]
           (when (= (:type ret) "SUCCESS")
             (process returns result "服务器返回的数据错误"))
           #((json.dumps ret) json-header))
         (except [ex [ZvmsError]]
                 #(json.dumps )))))))