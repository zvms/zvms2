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