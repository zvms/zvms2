(eval-and-compile
 (import hyrule [coll?])

 (defn chunks [iterable n]
   (for [i (range 0 (len iterable) n)]
     (yield (cut iterable i (+ i n)))))
 
 (defn flatten1 [iterable]
   (for [i iterable]
     (if (coll? i)
       (yield-from i)
       (yield i)))))

(require hyrule [case])

(defmacro constructor [#*fields]
  `(defn __init__ [self ~@fields]
     (setv ~@(flatten1 (gfor field (gfor f fields (if (coll? f) (get f -2) f))
                             #(`(. self ~field) field))))))

(defmacro defmth [name params #*body]
  `(defn ~name [self / ~@params]
     ~@body))

(defmacro select [subject #*args]
  (setv it (iter args)
        items [] 
        action 'add
        sym (hy.gensym))
  (while True
    (try
      (setv arg (next it))
      (case arg
        'as (setv action 'as)
        'with (setv action 'with)
        'select (return `(let [~sym ~subject]
                           (| ~(hy.models.Dict items)
                              (select (. ~sym ~(next it))
                                      ~@it))))
        else
          (do 
            (case action 
              'as (setv (get items -2) (str arg)) 
              'with (setv (get items -1) arg) 
              'add (do 
                     (items.append (str arg)) 
                     (items.append `(. ~sym ~arg))))
            (setv action 'add)))
      (except [StopIteration]
              (return `(let [~sym ~subject]
                         ~(hy.models.Dict items)))))))

(defmacro select-many [iterable #*args]
  (let [sym (hy.gensym)]
    `(gfor ~sym ~iterable
           (select ~sym ~@args))))