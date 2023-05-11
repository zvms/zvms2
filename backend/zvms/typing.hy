(import contextlib [contextmanager]
        datetime [datetime]
        types {NoneType}
        datetime [datetime])

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

(defmacro mismatch []
  '(except [ValueError TypeError]
           (err)))

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

(setv Any (Any))

(defclass Object [Processor]
  (setv module "")

  (constructor name fields optional)
  
  (defmth render []
    f"{Object.module}{(. (type self) __name__)}")
  
  (defmth jsonify []
    (dfor [k v] (self.fields.items) k (v.jsonify)))
  
  (defmth as-params []
    (dfor [k v] (self.fields.items) k (v.render)))
  
  (defmth process [json]
    (typecheck dict)
    (if self.optional
      (dfor [k v] json
            (with-path k
              (if (in k self.fields)
                (. self fields [k] (process v))
                v)))
      (dfor [k v] (self.fields.items)
            (with-path k
              (if (in k json)
                (v.process (get json k))
                (err)))))))

(defclass Simple [Processor]
  (defmth __init__ [#^type type #^str tsname [#^str name None]]
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
    (try
      (int json)
      (mismatch))))

(defclass DateTime [Processor]
  (defmth render []
    "string")
  
  (defmth jsonify []
    "datetime")
  
  (defmth process [json]
    (try
      (datetime.strptime json "%y-%m-%d-%H-%M")
      (mismatch))))

(setv URLInt URLInt
      DateTime DateTime)

(defclass Array [Processor]
  (constructor item)
  
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
  (constructor elts)
  
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

(defmacro range-jsonify [name] 
  `(defmth jsonify []
    {~name
     {"__min__" self.min
      "__max__" self.max
      "__raw__" (self.simple.jsonify)}}))

(defclass Range [Processor]
  (defmth __init__ [#^Processor simple [min None] [max None]]
    (setv self.simple simple
          self.min min
          self.max max))
  
  (defmth render []
    (self.simple.render))
  
  (range-jsonify "__range__")
  
  (defmth process [json]
    (let [processed (self.simple.process json)]
      (check-between json)
      processed)))

(defclass Len [Processor]
  (defmth __init__ [#^Processor simple [min None] [max None] ]
    (setv self.simple simple
          self.min min
          self.max (or max min)))
  
  (defmth render []
    (self.simple.render)) 
  
  (range-jsonify "__len__")
  
  (defmth process [json]
    (let [processed (self.simple.process json)]
      (check-between (len json))
      processed)))

(defclass Enum [Processo]
  (constructor enum)
  
  (defmth render []
    (+ "enums." self.enum.__name__))
    
  (defmth process [json]
    (try
      (self.enum json)
      (mismatch))))

(defclass URLEnum [Processor]
  (constructor enum)
  
  (defmth render []
    (+ "enums." self.enum.__name__))
  
  (defmth jsonify []
    (+ "enums.url." self.enum.__name__))
  
  (defmth process [json]
    (try
      (self.enum (int json))
      (mismatch))))