(import contextlib [contextmanager]
        datetime [datetime])

(require zvms.macros constructor)

(defclass CheckerError [Exception]
  #^str message)

(defclass Checker []
  (defn __call__ [self]
    self)
  (defn render [self] ...)
  
  (defn stringify [self]
    (self.render))
  
  (defn checker [self json] ...)
  
  (defn jsonify [self]
    (self.stringify))
  
  (setv where [])
  
  (defn [contextmanager] path [#^str s]
    (Checker.where.append s)
    (yield)
    (Checker.where.pop))
  
  (defn error [#^"Checker" expected found]
    (let [where (.join "." Checker.where)]
      (Checker.where.clear)
      (raise (CheckerError where (expected.jsonify) found)))))

(defclass Any [Checker]
  (defn render [self]
    "{}")
  
  (defn stringify [self]
    "any")
  
  (defn as-params [self]
    {}))

(defclass Object [Checker]
  (setv module "")
  
  (defn __init__ []))