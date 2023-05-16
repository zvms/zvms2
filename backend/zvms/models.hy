(import macros [flatten1])

(defmacro defmodel [name columns #*body]
  (setv auto-increment None)
  (for [column columns]
    (when (in ':auto-increment column)
      (setv auto-increment (get column 0))
      (break)))
  `(defclass ~name [db.Model]
     (setv ~@(flatten1 (gfor column columns
                             #((get column 0)
                               `(Column ~@(cut column 1 None))))))
     ~(if (is auto-increment None)
        '...
        `(defn __init__ [self #**kwargs]
           (.__init__ (super) self #*kwargs)
           (when (is (. self ~auto-increment) None)
             (setv max (. db session 
                          (query (func.max (. ~name ~auto-increment)))
                          (scalar))
                   (. self ~auto-increment) (+ (or max 0) 1)))))
     ~@body))

(print (hy.repr (hy.macroexpand '(defmodel Notice
                                   [[id Integer :primary-key True :auto-increment True]
                                    [sender-id Integer :name "sender"]]
                                   (defn [property] sender [self] ...)))))