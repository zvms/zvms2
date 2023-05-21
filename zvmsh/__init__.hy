(defclass Api []
  (defn __init__ [self
                  #^str name
                  #^str [doc ""]
                  #^(get dict #(str str)) config]
    (setv self.name name
          self.__doc__ doc
          self.routes []
          self.children []
          self.config
          (| (dict
              :prompt "> "
              :cmd-not-found "未找到命令"
              :failed-to-read "读取文件失败"
              :autorun "autorun.sh"
              :info "输入help :a 获取帮助"
              :on-exiting []
              :help ['help]
              :exit ['exit]
              :vars ['vars]
              :del ['del]
              :export ['export]
              :set ['set]
              :source ['source]
              :eval ['eval]
              :vars-cfg "vars.cfg")
             config)))
  
  (defn register [#^"App" child]
    (self.children.append child))
  
  (defn help [self #^tuple args]
    (defn helper []
      (for [[rule view] self.routes]
        (route-help rule view)
        (when view.__doc__
          (print view.__doc__))
        (print)))
    (if (not args)
      (do (print_ self.__doc__)
          (helper)
          (for [child self.children]
            (child.help)))
      (if (= (get args 0) :a)
        (print "{} 获取帮助
:a 全局帮助
:i 子模块索引
<name>"))))

  (defn run-cmd [self 
                 #^hy.models.Symbol entrypoint
                 #^tuple args]
    (cond
      (in entrypoint (:help self.config))
        (self.help (cut cmd 1 None))
      (in entrypoint (:exit self.config))
        (exit)
      (in entrypoint (:vars self.config))
        (for [[k v] (vars.items)]
          (print k v))
      (in entrypoint (:del self.config))
        (del (get vars (get cmd 1)))
      (in entrypoint (:eval self.config))
        (let [res (hy.eval (get cmd 1))]
          (when (not? res None)
            (print res)))
      (in entrypoint (:source self.config))
        (with [f (open (get cmd 1))]
              (for [line f]
                (self.run-cmd #* (hy.read-many line))))
      True 
        (for [[rule view] self.routes]
          (let [res (rule-match rule (+ [subject] args))]
            (when (not? res None)
              (view #* res)))
          (else
           (print (:cmd-not-found self.config))))))
  
  (defn rule-match [#^hy.models.Expression rule
                    #^list args]
    )
  
  (defn run [self]
    (setv self.vars {})
    (while True
      (setv cmd (list (hy.read-many (input (:prompt self.config)))))
      (when (not cmd)
        (continue))
      (self.run-cmd #* cmd)))
  
  )

(defmacro route [app name rule #* body]
  (setv params [])
  (for [i rule]
    (when (isinstance i hy.models.Expression)
      (params.append i)))
  `(do
     (defn ~name [~@params]
       ~@body)
     (.routes.append ~app #('~rule ~name))))