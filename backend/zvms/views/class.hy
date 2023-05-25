(import zvms.apilib *
        zvms.res *)

(require zvms.apilib *
         zvms.util [select
                    select-many])

(defstruct SingleUser 
           #^int id
           #^str name
           #^int auth)

(defstruct SingleClass 
           #^int id
           #^str name)

(defapi [:rule "/class/list"
         :models [Class]
         :returns (of list SingleClass)
         :doc "列出班级"]
  list-classes [] 
  (success (select-many (Class.query.filter (!= Class.id 0)) 
                         id 
                         name)))

(defstruct ClassInfoResponse 
           #^str name
           #^(of list SingleUser) students)

(defapi [:rule "/class/<int:id>"
         :models [User]
         :returns ClassInfoResponse
         :doc "获取班级详细信息"]
  get-class-info []
  (success (select (get/error Class id)
                    name
                    id students with (fn [id] 
                                       (list (select-many (User.query.filter (= User.class-id id)
                                                                             (& User.auth Categ.STUDENT)) 
                                                          id 
                                                          name 
                                                          auth))))))