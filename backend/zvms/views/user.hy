(import collections [defaultdict]
        datetime [timedelta]
        jwt
        zvms.apilib *
        zvms.util [inexact-now])

(require zvms.apilib *
         zvms.util [defmth select])

(defclass IncorrectLoginRecord []
  (setv __slots__ ["times" "enabled_since"])
  
  (defmth __init__ []
    (setv self.times 0
          self.enabled-since (inexact-now))))

(setv incorrect-login-records (defaultdict IncorrectLoginRecord))

(defn generate-token [#^dict data]
  (import zvms [app])
  (jwt.encode data :key (:SECRET-KEY app.config)))

(defn read-token [token]
  (import zvms [app])
  (jwt.decode (token.encode) :key (:SECRET-KEY app.config) :algorithms "HS256"))

(defstruct UserLoginResponse None False
           #^str token
           #^int id
           #^str userName
           #^str clsName)

(defapi [:rule "/user/login"
         :method "POST"
         :auth Categ.NONE
         :params UserLogin
         :returns UserLoginResponse
         :models [User Class]
         :doc "用户登录"]
  login [#^str id #^str pwd]
  (import flask [request])
  (let [record (get incorrect-login-records request.remote-addr)
        now (inexact-now)]
    (cond
      (> record.times 5)
        (do (setv record.times 0
                  record.enabled-since (+ now (timedelta :minutes 5)))
            (| (error "登录过于频繁") {"noretry" True}))
      (> record.enabled-since now)
        (| (error "登录过于频繁") {"noretry" True})
      True
        (do
          (setv user None)
          (for [i (User.query.filter-by :name id)]
            (setv user i)
            (break))
          (when (and (id.isdecimal) (is user None))
            (setv user (User.query.get (int id))))
          (if (or (is user None) (!= user.pwd pwd))
            (do
              (+= record.times 1)
              (| (error "用户名或密码错误") {"noretry" False}))
            (do
              (setv record.times 0)
              (success "登录成功"
                       :token (generate-token (select user
                                                      id
                                                      name
                                                      auth
                                                      class-id as class))
                       #** (select user
                                   id
                                   name
                                   class-id with (fn [id] (. Class query (get id) name))))))))))

; 这个API实际上什么都不做, 但先留着, 没准以后会用到
(defapi [:rule "/user/logout"
         :method "POST"
         :doc "用户登出"]
  logout []
  (success "登出成功"))

(defstruct UserInfoResponse None False
           #^str name
           #^int cls
           #^int auth
           #^str clsName)

(defapi [:rule "/user/<int:id>"
         :models [User]
         :returns UserInfoResponse
         :doc "获取一个用户的详细信息"]
  get-user-info []
  (success "获取成功" #** (select (get/error User id)
                              name
                              auth
                              class-id as cls
                              class-id as clsName with (fn [id] (. Class query (get id) name)))))

(defstruct StudentScoresResponse None False
           #^int inside
           #^int outside
           #^int large)

(defapi [:rule "/user/<int:id>/scores"
         :models [User]
         :returns StudentScoresResponse
         :doc "获取一个学生用户的义工分"]
  get-student-scores []
  (success "获取成功" (select (get/error User id)
                          inside
                          outside
                          large)))

(defapi [:rule "/user/<int:id>/mod-pwd"
         :method "POST"
         :models [User Issue]
         :params ModPwd
         :doc "修改某人的密码"]
  modify-password [#^str old-pwd #^str new-pwd]
  (if (!= (len new-pwd) 32)
    (error "密码格式错误")
    (do
      (let [user (get/error User id)]
        (cond
          (and (!= user.id (:id token-data)) (not (and (& (:auth token-data) (| Categ.SYSTEM Categ.MANAGER))
                                                       (not (& user.auth Categ.SYSTEM)))))
            (error "无权限修改此人的密码")
          (!= user.pwd old-pwd)
            (error "旧密码错误")
          True
            (do
              (setv user.pwd new-pwd)
              (when (!= user.id (:id token-data))
                (insert (Issue
                         :reporter 0
                         :content (.format "用户{}将{}的密码修改了" (:name token-data) id)
                         :time (inexact-now))))
              (success "修改成功")))))))

#_(if (!= user.id (:id token-data))
    (if (& (:auth token-data) (| Categ.MANAGER Categ.SYSTEM))
      (if (& user.auth Categ.SYSTEM)
        (error)
        (success))
      (error))
    (error))