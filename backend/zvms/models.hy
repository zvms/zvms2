(import zvms.macros [flatten1 defmth])

(defmacro defmodel [name columns #*body]
  (setv auto-increment None
        primary-keys [])
  (for [column columns]
    (when (in ':auto-increment column)
      (setv auto-increment (get column 0)))
    (when (in ':primary-key column)
      (primary-keys.append (get column 0))))
  `(defclass ~name [db.Model]
     (setv ~@(flatten1 (gfor column columns
                             #((get column 0)
                               `(Column ~@(cut column 1 None))))))
     (defmth query-self []
       (. ~name query (filter-by ~@(flatten1 (gfor pk primary-keys
                                                   #((hy.models.Keyword pk) `(. self ~pk)))))))
     (defmth delete []
       (. self (query-self) (delete)))
     (defmth update [#**kwargs]
       (. self (query-self) (update (dfor [k v] (kwargs.items)
                                          (getattr ~name k) v))))
     ~(if (is auto-increment None)
        '...
        `(defmth __init__ [#**kwargs]
           (.__init__ (super) self #*kwargs)
           (when (is (. self ~auto-increment) None)
             (setv max (. db session 
                          (query (func.max (. ~name ~auto-increment)))
                          (scalar))
                   (. self ~auto-increment) (+ (or max 0) 1)))))
     
     ~@body))

(defn insert [self]
  (db.session.add self)
  self)