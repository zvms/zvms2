(import datetime [timedelta] 
        zvms.apilib *
        zvms.res *
        zvms.util [inexact-now])

(require zvms.apilib *
         zvms.util [select
                    select-many])

(defstruct SingleVolunteer
  #^int id
  #^str name
  #^str time
  #^int status
  #^bool signable)

(defapi [:rule "/volunteer/list"
         :models [Volunteer StuVol ClassVol]
         :returns (of list SingleVolunteer)
         :doc "列出义工"]
  list-volunteers []
  (import sqlalchemy [or_])
  (success  (select (if (= (:auth token-data) 0)
                      (Volunteer.query.filter (or_ ( = Volunteer.holder-id (:id token-data))
                                                   (Volunteer.id.in_ (. db session 
                                                                        (query (StuVol.vol-id.label "vol_id"))
                                                                        (filter-by :stu-id (:id token-data))
                                                                        (subquery)
                                                                        vol-id))
                                                   (Volunteer.id.in_ (. db session
                                                                        (query (ClassVol.vol-id.label "vol_id"))
                                                                        (filter-by :class-id (:cls token-data))
                                                                        (subquery)
                                                                        vol-id))))
                      Volunteer.query)
                    id
                    name 
                    time with str
                    calculated-status as status)))

(import zvms.views.class [SingleUser SingleClass])

(defstruct VolunteerInfoResponse
  #^str name
  #^VolType type
  #^int reward
  #^datetime time
  #^str description
  #^VolStatus status
  #^int holder
  #^str holder-name
  #^(of list SingleUser) joiners
  #^(of list SingleClass) classes)

(defapi [:rule "/volunteer/<int:id>"
         :models [Volunteer User]
         :returns VolunteerInfoResponse
         :doc "获取一个义工的详细信息"]
  get-volunteer-info []
  (success  (select (get/error Volunteer id)
                    name
                    type
                    reward
                    time with str
                    description
                    computed-status as status
                    holder-id as holder
                    holder-id as holder-name with (fn [id]
                                                    (. User query (get id) name))
                    joiners
                    classes)))

(defmacro _create-volunteer [type]
  `(. (insert (Volunteer :name name
                         :description description
                         :time time
                         :reward reward
                         :type ~type
                         :holder-id (:id token-data))) id))

(defstruct ClassLimit
  #^int id
  #^int max)

(defapi [:rule "/volunteer/create/inside"
         :method "POST"
         :models [Volunteer ClassVol]
         :params InsideVolunteer
         :doc "创建可自由报名的校内义工"]
  create-inside-volunteer [#^str name
                           #^str description
                           #^datetime time
                           #^int reward
                           #^(of list ClassLimit) classes]
  (let [id (_create-volunteer VolType.INSIDE)]
    (if (authorized (| Categ.CLASS Categ.MANAGER) (:auth token-data))
      (for [class classes]
        (let [cls (get/error (:id class) ErrorCode.CLASS-NOT-FOUND)]
          (when (> (:max class) (cls.members.count))
            (return (error ErrorCode.VOLUNTEER-MEMBERS-OVERFLOWN)))
          (insert (ClassVol :class-id (:id class)
                            :vol-id id
                            :max (:max class)))))
      (for [class classes]
        (cond
          (!= (:id class) (:cls token-data))
            (return (error ErrorCode.NO-ACCESS-TO-OTHER-CLASSES))
          (> (:max class) (cls.members.count))
            (return (error ErrorCode.VOLUNTEER-MEMBERS-OVERFLOWN))
          True
            (insert (ClassVol :class-id (:id class)
                              :vol-id id
                              :max (:max class))))))
    (success)))

(defapi [:rule "/volunteer/create/appointed" 
         :method "POST" 
         :models [Volunteer ClassVol StuVol]
         :params AppointedVolunteer
         :doc "创建成员指定的义工"]
  create-appointed-volunteer [#^str name 
                              #^str description 
                              #^datetime time 
                              #^int reward 
                              #^VolType type
                              #^(of list str) joiners]
  (let [id (_create-volunteer type)]
    (insert (ClassVol
             :class-id (:cls token-data)
             :vol-id id
             :max 0))
    (for [joiner joiners]
      (let [joiner (User.get/error joiner ErrorCode.USER-NOT-FOUND)]
        (if (!= joiner.class-id (:cls token-data))
          (return (error ErrorCode.NO-ACCESS-TO-OTHER-CLASSES))
          (insert (StuVol :stu-id joiner.id
                          :vol-id id
                          :status ThoughtStatus.DRAFT
                          :thought ""
                          :reward -1)))))
    (success)))

(defmacro audit-volunteer-api [rule doc name status message]
  `(defapi [:rule ~rule
           :method "POST"
           :models [Volunteer]
           :auth Categ.CLASS
           :doc ~doc]
    ~name []
    (let [vol (get/error Volunteer id)
          now (inexact-now)]
      (import zvms.models [auth-class])
      (when (& (:auth token-data) Categ.CLASS)
        (auth-class (vol.holder.class-id token-data)))
      (. Volunteer query (filter-by :id id) (update {Volunteer.status (. VolStatus ~status)}))
      (insert (UserNotice
               :user-id vol.holder-id
               :notice-id (. (insert (Notice
                                      :title "义工过审"
                                      :content (.format ~message vol.name)
                                      :sendtime now
                                      :deadtime (+ now (timedelta :days 10)))) id)))
      (success))))

(audit-volunteer-api "/volunteer/<int:id>/audit/accept"
                     "审核通过义工"
                     accept-volunteer
                     AUDITED
                     "您的义工{}已过审")

(audit-volunteer-api "/volunteer/<int:id>/audit/reject"
                     "审核拒绝义工"
                     reject-volunteer
                     REJECTED
                     "您的义工{}已被拒绝")

(defstruct SpecialVolunteerJoiner
  #^str id
  #^int reward)

(defapi [:rule "/volunteer/create/special"
         :method "POST"
         :models [Volunteer Notice StuVol UserNotice]
         :auth Categ.MANAGER
         :params SpecialVolunteer
         :doc "创建特殊义工(竞赛等)"]
  create-special-volunteer [#^str name
                            #^VolType type
                            #^(of list SpecialVolunteerJoiner) joiners]
  (let [id (. (insert (Volunteer :name name
                                 :description ""
                                 :status VolStatus.AUDITED
                                 :holder-id (:id token-data)
                                 :time (inexact-now)
                                 :type type
                                 :reward reward)) id)
        now (inexact-now)
        deadtime (+ now (timedelta :days 3))
        notice-ids (dfor joiner joiners 
                         (:reward joiner)
                         (. (insert (Notice :title "义工时间"
                                            :content (.format "您由于{}获得了{}义工时间" name reward)
                                            :sender 0
                                            :sendtime now
                                            :deadtime deadtime)) id))]
    (for [joiner joiners]
      (let [user (. (User.get/error (:id joiner) ErrorCode.USER-NOT-FOUND) id)]
        (insert (StuVol :vol-id id
                        :stu-id user.id
                        :status ThoughtStatus.ACCEPTED
                        :thought name
                        :reason ""
                        :reward (:reward joiner)))
        (insert (UserNotice :user-id joiner
                            :notice-id (get notice-ids (:reward joiner))))))))