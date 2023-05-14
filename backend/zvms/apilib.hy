(import functools [wraps]
        pprint [pprint]
        datetime [datetime]
        types [FunctionType]
        typing [Iterable
                Callable
                TypedDict]
        pprint [pprint]
        json
        re
        zvms.util [inexact-now]
        zvms.typing *
        zvms.res [Categ]
        zvms.macros [flatten1 chunks])

(require hyrule *
         zvms.macros *)

(defclass Api []
  (setv #^(of list "Api") apis []
        #^(of dict str Object) structs {})
  
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
            (setv (get ex "msg") msg)
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
                         (except [] {})))
           token-data (if (= auth Categ.None)
                        {}
                        (try
                          (let [token-data (request.headers.get "Authorization")]
                            (when (not data)
                              (raise InvalidSignatureError))
                            (setv token-data (tk.read token-data))
                            (cond
                              (not (tk.exists token-data))
                              (return #((json.dumps {"type" "ERROR" "message" "Token失效, 请重新登陆"}) json-header))
                              (not (auth.authorized (:auth token-data)))
                              (return #((json.dumps {"type" "ERROR" "message" "权限不足"}) json-header))
                              True token-data))
                          (except [InvalidSignatureError]
                                  (return #((json.dumps {"type" "ERROR" "message" "未获取到Token, 请重新登陆"}) json-header)))))]
       (when __debug__
         (with [f (open "log.txt" "a" :encoding "utf-8")]
               (let [log f"{(inexact-now)}[{request.remote-addr}]"]
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

(defn annotations->params [#^hy.models.Object ann]
  (match ann
    (hy.models.Symbol)
      (case ann
        'int Int
        'float Float
        'str String
        'bool Boolean
        'NoneType Null
        'datetime DateTime
        'Any (Any)
        else (get Api.structs (str ann)))
    (hy.models.Expression ['of 'list generic-param])
      (Array (annotations->params generic-param))
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

(defmacro defstruct [name base optional #*fields]
  (setv doc 'None)
  (when (isinstance (get fields 0) hy.models.String)
    (setv doc (get fields 0)
          fields (cut fields 1 None)))
  `(do
     (defclass ~name [TypedDict ~@(if (= base 'None) #() #(base)) :total (not ~optional)]
       ~@fields)
     (setv (get Api.structs ~(str name)) (Object ~(str name) ~base ~optional ~doc (dfor [_ key value] '~fields (str key) (annotations->params value))))))

(defmacro defapi [options name params #*body]
  (let [options (| {"method" '"GET"
                    "auth" 'Categ.ANY
                    "params-optional" 'False
                    "params" 'None
                    "returns" 'Any
                    "doc" '""}
                   (dfor [k v] (chunks options 2) (. k name) v))
        url-params (dict (gfor param (re.findall r"\<.+?\>" (:rule options))
                               (if (param.startswith "<int:")
                                 #((cut param 5 -1) 'int)
                                 #((cut param 1 -1) 'str))))
        need-params (and (!= (:params options) 'None) (not-in (str (:params options)) Api.structs))]
    `(do
       ~(if need-params
            `(defstruct ~(:params options)
               None 
               ~(get options "params-optional")
               ~@params)
            '...)
       (defn ~name [#^TokenData token-data
                      ~@(gfor [name type] url-params `(annotate ~type ~(hy.models.Symbol name)))
                      ~@params]
           ~@body)
       (Api.apis.append (Api :func ~name 
                             :rule ~(:rule options)
                             :method ~(:method options)
                             :auth ~(:auth options)
                             :doc ~(:doc options)
                             :url-params ~(dfor [name type] url-params name (case type 
                                                                              'int "number" 
                                                                              'str "string")) 
                             :params ~(if need-params `(get Api.structs ~(str (:params options))) None)
                             :returns (annotations->params '~(:returns options)))))))