(import functools [wraps]
        pprint [pprint]
        datetime [datetime]
        types [Callable
               FunctionType]
        typing [Iterable
                TypedDict]
        pprint [pprint]
        json
        re
        zvms.util [inexact-now]
        zvms.typing *
        zvms.res [Categ])

(require hyrule *
         zvms.macros *)

(defclass Api []
  (setv #^(of list "Api") apis []
        #^(of list Object) structs [])
  
  (constructor #^Callable func
               #^str rule
               #^str method
               #^Categ auth
               #^(of dict str str) url-params
               #^hy.models.Symbol params
               returns
               #^str doc)
  
  (defn init-app [app]
    (for [api Api.apis]
      (app.add-url-rule api.rule 
                        :methods [api.method]
                        :view-func (deco api.func 
                                         (if (is api.params None)
                                           (Any)
                                           api.params)
                                         (if (is api.returns None)
                                           (Any)
                                           (annotations->params api.returns))
                                         api.auth)))))

(setv json-header {"Content-Type" "application/json ; charset=utf-8"})

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
             zvms.models [db Issue]
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
                 #(json.dumps (error ex.msg)))
         (except [ex [ProcessorError]]
                 (let [error-info (dict (zip #("where" "expected" "found")
                                 ex.args))]
                   (when __debug__
                     (pprint error-info))
                   (insert (Issue
                            :time (inexact-now)
                            :reporter 0
                            :content (.format "(用户: {}) {}: {}'"
                                              (:id token-data "<未登录>")
                                              ex.msg
                                              (json.dumps error-info :indent 4))))
                   (json.dumps (| (error ex.msg) error-info)))))))))

(defclass TokenData [TypedDict]
  #^int id
  #^int auth
  #^int cls
  #^str name)

(defn pipline [#^(of Iterable Callable) fns obj]
  (while fns
    (setv obj ((fns.pop) obj)))
  obj)

(defn annotations->params-helper [#^hy.models.Object ann]
  (match ann
    (hy.models.Symbol)
      (case ann
        'int Int
        'float Float
        'str String
        'bool Boolean
        'NoneType Null
        'datetime DateTime
        else (get Api.structs ann))
    (hy.models.Expression ['| #*rest])
      (let [metadata []
            union-elts []]
        (for [i rest]
          (if (isinstance i FunctionType)
            (metadata.append i)
            (union-elts.append i)))
        (cond
          (and metadata (> (len union-elts) 1))
            (pipline metadata (Union union-elts))
          (> (len union-elts) 1)
            (Union union-elts)
          metadata
            (pipline (get union-elts 0))
          True
            (get union-elts 0)))))

(defn annotations->params [#^str name #^bool optional #^(of tuple hy.models.Expression) ann]
  (Object name optional (dfor [_ key value] ann
                              key (annotations->params-helper value))))

(defmacro defstruct [name optional #*fields]
  `(do
     (defclass ~name [TypedDict :total (not ~optional)]
       ~@fields)
     (Api.structs.append (annotations->params ~(str name) ~optional ~fields))))

#_(defstruct Accept
    #^int reward)

#_(do
    (defclass Accept [TypedDict :total (not False)]
      #^int reward)
    (Api.structs.append (annotations->params "Accept" False #('(annotate reward int)))))

#_(defapi [:rule "/thought/<int:volId>/<int:stuId>/audit/final"
           :method "POST"
           :auth Categ.AUDITOR
           :params 'Accept
           :doc "终审感想(义管会)"]
    final-audit [#^int reward]
    ...)

(defmacro defapi [options name params #*body]
  (let [options (| {"method" "GET"
                    "params-optional" False
                    "params" None
                    "returns" None
                    "doc" ""}
                   (dict (do-mac options)))
        url-params (dict (gfor param (re.findall r"\<.+?\>" (:rule options))
                               (if (param.startswith "<int:")
                                 #((cut param 5 -1) 'int)
                                 #((cut param 1 -1) 'str))))]
    `(do
       ~(if (and (:params options) (not-in (:params options) Api.structs))
          `(defstruct (:params options) (:params-optional options) params)
          ...)
       (defn ~name [#^TokenData token-data
                    ~@(gfor [name type] url-params `(annotate ~type ~(hy.models.Symbol name)))
                    ~@fields]
         ~@body)
       (Api.apis.append (Api :func ~name
                             :url-params (dfor [name type] name (case type
                                                                  'int "number"
                                                                  'str "string"))
                             #**(~(dfor [k v] options :if (!= k "params-optional") k v)))))))

#_(do
    (defstruct Accept False
               #^int reward)
    (defn final-audit [#^TokenData token-data
                       #^int stuId
                       #^int volId
                       #^int reward]
      ...)
    (Api.apis.append (Api :func final-audit
                          :rule "/thought/<int:volId>/<int:stuId>/audit/final"
                          :method "POST"
                          :url-params {"volId" "number" "stuId" "number"}
                          :params (:Accept Api.structs)
                          :returns None
                          :doc "终审感想(义管会)")))