(import contextlib [contextmanager]
        datetime [datetime]
        types [NoneType]
        typing [Iterable
                Optional]
        datetime [datetime]
        enum [EnumType])

(require hyrule *
         zvms.macros *)

(defclass ProcessorError [Exception]
  #^str message)

(defclass Processor []
  (defmth __call__ []
    self)
  
  (defmth render [] ...)

  (defmth jsonify []
    (self.render))
  
  (defmth process [json]
    json)
  
  (setv where [])
  
  (defn [contextmanager] path [#^str s]
    (Processor.where.append s)
    (yield)
    (Processor.where.pop))
  
  (defn error [#^"Processor" expected found]
    (let [where (.join "." Processor.where)]
      (Processor.where.clear)
      (raise (ProcessorError where (expected.jsonify) found)))))

(defmacro err []
  '(Processor.error self json))

(defmacro try-type [#*body]
  `(try
     ~@body
     (except [ValueError TypeError]
             (err))))

(defmacro typecheck [type]
  `(unless (isinstance json ~type) 
           (err)))

(defmacro with-path [s #*body]
  `(with [(Processor.path s)]
         ~@body))

(defclass Any [Processor]
  (defmth render []
    "{}")
  
  (defmth jsonify []
    "any")
  
  (defmth as-params []
    {}))

(defclass Object [Processor]
  (setv module "")
  
  (defmth __init__ [#^str name 
                    #^(of Optional "Object") base 
                    #^bool optional  
                    #^(of Optional str) doc
                    #^(of dict str Processor) fields]
    (setv self.name name
          self.base base
          self.optional optional
          self.doc doc
          self.fields fields
          self.inherited-fields (if (is base None) fields (| fields base.inherited-fields))))
  
  (defmth render []
    f"{Object.module}{self.name}")
  
  (defmth jsonify []
    (dfor [k v] (self.inherited-fields.items) k (v.jsonify)))
  
  (defmth as-params []
    (if self.optional
      {"kwargs" (self.render)}
      (dfor [k v] (self.fields.items) k (v.render))))
  
  (defmth process [json]
    (typecheck dict) 
    (dict (if self.optional
            (gfor [k v] json
                  (with-path k
                    (if (in k self.inherited-fields)
                      #(k (.self fields [k] (process v)))
                      v)))
            (gfor [k v] (self.inherited-fields.items)
                  (with-path k
                    (if (in k json)
                      #(k (v.process (get json k)))
                      (err))))))))

(defclass Simple [Processor]
  (defmth __init__ [#^type type #^str tsname #^str [name None]]
    (setv self.type type
          self.tsname tsname
          self.name (or name tsname)))
  
  (defmth render []
    self.tsname)
  
  (defmth jsonify []
    self.name)
  
  (defmth process [json]
    (typecheck self.type)
    json))

(setv String (Simple str "string")
      Int (Simple int "number" "int")
      Float (Simple float "number" "float")
      Boolean (Simple bool "boolean")
      Null (Simple NoneType "null"))

(defclass URLInt [Processor]
  (defmth render []
    "number")
  
  (defmth jsonify []
    "urlint")
  
  (defmth process [json]
    (try-type
      (int json))))

(defclass DateTime [Processor]
  (defmth render []
    "string")
  
  (defmth jsonify []
    "datetime")
  
  (defmth process [json]
    (try-type
      (datetime.strptime json "%y-%m-%d-%H-%M"))))

(defclass Array [Processor]
  (constructor #^Processor item)
  
  (defmth render []
    (+ "Array<" (self.item.render) ">"))
  
  (defmth jsonify []
    [(self.item.jsonify)])
  
  (defmth process [json]
    (typecheck #(list tuple))
    (lfor [i v] (enumerate json)
      (with-path (str i)
        (self.item.process v)))))

(defclass Union [Processor]
  (constructor #^(of Iterable Processor) elts)
  
  (defmth render []
    (.join " | " (gfor elt self.elts (elt.render))))
  
  (defmth jsonify []
    {"__union__" (lfor elt self.elts (elt.jsonify))})
  
  (defmth process [json]
    (for [elt self.elts]
      (try
        (return (elt.process json))
        (except [ProcessorError] ...)))
    (err)))

(defmacro check-between [comparator]
  `(when (not (and (or (is self.min None) (>= ~comparator self.min)) 
                   (or (is self.max None) (< ~comparator self.max))))
     (err)))

(defmacro metadata-info [name] 
  `(do
     (constructor #^Processor simple min max)

     (defmth render []
       (self.simple render))
     
     (defmth jsonify [] 
       {~name 
        {"__min__" self.min 
         "__max__" self.max 
         "__raw__" (self.simple.jsonify)}})))

(defmacro def-metadata-fn [name class]
  `(defn ~name [min [max None]]
     (when (is max None)
       (setv max min
             min 0))
     (fn [simple]
       (~class simple min max))))

(def-metadata-fn Range RangeProcessor)
(def-metadata-fn Len LenProcessor)

(defclass RangeProcessor [Processor]
  (metadata-info "__range__")
  
  (defmth process [json]
    (let [processed (self.simple.process json)]
      (check-between json)
      processed)))

(defclass LenProcessor [Processor]
  (metadata-info "__len__")
  
  (defmth process [json]
    (let [processed (self.simple.process json)]
      (check-between (len json))
      processed)))

(defclass Enum [Processor]
  (constructor #^EnumType enum)
  
  (defmth render []
    (+ "enums." self.enum.__name__))
    
  (defmth process [json]
    (try-type
      (self.enum json))))

(defclass URLEnum [Processor]
  (constructor #^EnumType enum)
  
  (defmth render []
    (+ "enums." self.enum.__name__))
  
  (defmth jsonify []
    (+ "enums.url." self.enum.__name__))
  
  (defmth process [json]
    (try-type
      (self.enum (int json)))))
