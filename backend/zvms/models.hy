(import flask-sqlalchemy *
        sqlalchemy *)

(require zvms.util [defmth])

(eval-when-compile
 (import zvms.util [flatten1]))

(defmacro defmodel [name table-name columns #* body]
  (setv auto-increment None
        primary-keys [])
  (for [column columns]
    (when (in ':autoincrement column)
      (setv auto-increment (get column 0)))
    (when (in ':primary-key column)
      (primary-keys.append (get column 0))))
  `(defclass ~name [db.Model]
     (setv __tablename__ ~(str table-name)
           ~@(flatten1 (gfor column columns
                             #((get column 0)
                               `(Column ~@(cut column 1 None))))))
     
     (defmth query-self []
       (. ~name query (filter-by ~@(flatten1 (gfor pk primary-keys
                                                   #((hy.models.Keyword pk) `(. self ~pk)))))))
     
     (defmth on-delete [] ...)            
     
     (defmth delete []
       (self.on-delete)
       (. self (query-self) (delete)))
     
     (defmth update [#**kwargs]
       (. self (query-self) (update (dfor [k v] (kwargs.items)
                                          (getattr ~name k) v))))
     
     ~(if (is auto-increment None)
        '...
        `(defmth __init__ [#**kwargs]
           (.__init__ (super) #**kwargs)
           (when (is (. self ~auto-increment) None)
             (setv max (. db session 
                          (query (func.max (. ~name ~auto-increment)))
                          (scalar))
                   (. self ~auto-increment) (+ (or max 0) 1)))))
     
     ~@body))

(setv db (SQLAlchemy))

(defn insert [self]
  (db.session.add self)
  self)

(defn get/error [model ident #^str [msg "未查询到相关数据"]]
  (let [res (model.query.get ident)]
    (if (is res None)
      (raise (ZvmsError msg))
      res)))

(defn error [#^str msg]
  (db.session.rollback)
  {"type" "ERROR" "message" msg})

(defn success [#^str msg [result None] #**kwargs]
  (let [res {"type" "SUCCESS" "message" msg}]
    (cond
      (not? result None)
        (setv (get res "result") result)
      kwargs
        (setv (get res "result") kwargs))
    (db.session.commit)
    res))

(defmodel Class
  class
  [[id Integer :primary-key True :autoincrement True]
   [name (String 5)]]
  (defmth on-delete []
    (. ClassNotice query (filter-by :class-id self.id) (delete))
    (. ClassVol query (filter-by :class-id self.id) (delete))
    (. User query (filter-by :class-id self.id) (delete))))

(defmodel User
  user
  [[id Integer :primary-key True :autoincrement True]
   [name (String 5)]
   [class-id Integer :name "class"]
   [pwd (String 32)]
   [auth Integer]]
  (defmth on-delete []
    (. UserNotice query (filter-by :user-id self.id) (delete))
    (. StuVol query (filter-by :stu-id self.id) (delete))
    (. Volunteer query (filter-by :holder-id self.id) (delete))))

(defmodel Notice
  notice 
  [[id Integer :primary-key True :autoincrement True]
   [title (String 32)]
   [content (String 1024)]
   [sender Integer]
   [sendtime DateTime]
   [deadtime DateTime]]
  (defmth on-delete []
    (. UserNotice query (filter-by :notice-id self.id) (delete))
    (. ClassNotice query (filter-by :notice-id self.id) (delete))
    (. SchoolNotice query (filter-by :notice-id self.id) (delete))))  

(defmodel Volunteer 
  volunteer
  [[id Integer :primary-key True :autoincrement True]
   [name (String 32)]
   [description (String 1024)]
   [status SmallInteger]
   [holder-id Integer :name "holder"]
   [time DateTime]
   [type SmallInteger]
   [reward Integer]]
  (defmth on-delete []
    (. StuVol query (filter-by :vol-id self.id) (delete))))

  (defmodel StuVol
  stu-vol
  [[vol-id Integer :primary-key True :name "volunteer"]
   [stu-id Integer :primary-key True :name "student"]
   [status SmallInteger]
   [thought (String 1024)]
   [reason (String 64)]
   [reward Integer]])

  (defmodel ClassVol
  class-vol
  [[vol-id Integer :primary-key True :name "volunteer"]
   [class-id Integer :primary-key True :name "class"]
   [max Integer]])

  (defmodel Picture
  picture
  [[vol-id Integer :primary-key True :name "volunteer"]
   [stu-id Integer :primary-key True :name "student"]
   [hash (String 32)]
   [extension (String 5)]])

  (defmodel UserNotice
  user-notice
  [[user-id Integer :primary-key True :name "user"]
   [notice-id Integer :primary-key True :name "notice"]])

  (defmodel ClassNotice
  class-notice
  [[class-id Integer :primary-key True :name "class"]
   [notice-id Integer :primary-key True :name "notice"]])
  
  (defmodel SchoolNotice
  school-notice
  [[notice-id Integer :primary-key True :name "notice"]])

(defmodel Issue
  issue
  [[id Integer :primary-key True :autoincrement True]
   [time DateTime]
   [author Integer]
   [content (String 255)]])