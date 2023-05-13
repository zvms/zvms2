(eval-when-compile
 (import hyrule [coll?])

 (defn chunks [iterable n]
   (for [i (range (// (len iterable) n))]
     (yield (cut iterable i (+ i n)))))
 
 (defn flatten1 [iterable]
   (for [i iterable]
     (if (coll? i)
       (yield-from i)
       (yield i)))))

(defmacro constructor [#*fields]
  `(defn __init__ [self ~@fields]
     (setv ~@(flatten1 (gfor field (gfor f fields (if (coll? f) (get f -2) f))
                             #(`(. self ~field) field))))))

(defmacro defmth [name params #*body]
  `(defn ~name [self ~@params]
     ~@body))
