(eval-when-compile
 (defn chunks [iterable n]
   (for [i (range (// (len iterable) n))]
     (yield (cut iterable i (+ i n)))))
 
 (defn ))

(defmacro constructor [#* fields]
  `(defn __init__ [self ~@fields]
     (setv ~@(gfor field fields
                   ))))