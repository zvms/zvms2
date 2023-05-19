(import zvms.apilib *
        zvms.res *)

(require zvms.apilib *
         zvms.util [select
                    select-many])

(defstruct SingleUser None False
           #^int id
           #^str name
           #^int auth)

(defstruct SingleClass None False
           #^int id
           #^str name)

(defapi [:rule "/class/list"
         :models [Class]
         :returns (of list SingleClass)]
  list-classes [] 
  (success "获取成功" (list (select-many (Class.query.filter (!= Class.id 0)) 
                                     id 
                                     name))))

(defstruct ClassInfoResponse None False
           #^str name
           #^(of list SingleUser) students)

(defapi [:rule "/class/<int:id>"
         :models [User]
         :returns ClassInfoResponse]
  get-class-info []
  (success "获取成功" (select (get/error Class id)
                          name
                          id students with (fn [id] 
                                             (list (select-many (User.query.filter (= User.class-id id)
                                                                                   (& User.auth Categ.STUDENT)) 
                                                                id 
                                                                name 
                                                                auth))))))