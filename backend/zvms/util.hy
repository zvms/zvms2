(defmacro case [subject #* args]
  (setv items ['cond]
        sym (hy.gensym)
        action 'test)
  (for [arg args]
    (cond
      (= action 'test)
      (if (= arg 'else)
        (do (items.append 'True)
            (setv action 'else))
        (do (items.append `(= ~sym ~arg))
            (setv action 'body)))
      (= action 'body)
      (do (items.append arg)
          (setv action 'test))
      (= action 'else)
      (return `(let [~sym ~subject]
                 (~@items ~arg)))))
  `(let [~sym ~subject]
     (~@items)))
(eval-and-compile
 (import typing [Iterable])

 (defn convention-convert [ident src dst]
   (let [elems (map str.lower (case src
                                'snake (ident.split "_")
                                'upper-snake (ident.split "_")
                                'camel (chain #((.group (re.match r "^[a-z]*" ident))) (re.findall r "[A-Z][a-z]*" ident))
                                'pascal (re.findall r "[A-Z][a-z]*" ident)
                                'lisp (ident.split "-")
                                'url (ident.split "/")
                                'text (ident.split)))]
     (case dst
       'snake (.join "_" elems)
       'upper-snake (.join "_" (map str.upper elems))
       'camel (let [iter (iter elems)]
                (+ (next iter) (.join "" (map str.capitalize iter))))
       'pascal (.join "" (map str.capitalize elems))
       'lisp (.join "-" elems))))

 (defn coll? [obj]
   (and (isinstance obj Iterable) (not (isinstance obj #(str bytes))))) 

 (defn chunks [iterable n]
   (for [i (range 0 (len iterable) n)]
     (yield (cut iterable i (+ i n)))))
 
 (defn flatten1 [iterable]
   (for [i iterable]
     (if (coll? i)
       (yield-from i)
       (yield i)))))

(import datetime [datetime])

(defn inexact-now []
  (.replace (datetime.now) :microsecond 0))

(defmacro of [obj #* args]
  (if (> (len args) 1)
    `(get ~obj ~args)
    `(get ~obj ~@args)))

(defmacro constructor [#* fields]
  `(defn __init__ [self ~@fields]
     (setv ~@(flatten1 (gfor field (gfor f fields (if (coll? f) (get f -2) f))
                             #(`(. self ~field) field))))))

(defmacro defmth [name params #* body]
  `(defn ~name [self / ~@params]
     ~@body))

(defmacro select [subject #* args]
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
        'from (return `(let [~sym ~subject]
                         (| ~(hy.models.Dict items)
                            (select ~(next it)
                                    ~@it))))
        else
          (do 
            (case action 
              'as (setv (get items -2) (convention-convert arg 'lisp 'camel)) 
              'with (setv (get items -1) arg) 
              'add (do 
                     (items.append (convention-convert arg 'lisp 'camel)) 
                     (items.append `(. ~sym ~arg))))
            (setv action 'add)))
      (except [StopIteration]
              (return `(let [~sym ~subject]
                         ~(hy.models.Dict items)))))))

(defmacro select-many [iterable #* args]
  (let [sym (hy.gensym)]
    `(lfor ~sym ~iterable
           (select ~sym ~@args))))