(import datetime[timedelta] 
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

(defapi [:rule "/volunteer/<int:id>"
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
                    from 
                    joiners
                    classes)))

(defmacro _create-volunteer [type]
  `(. (insert (Volunteer :name name
                         :description description
                         :time time
                         :reward reward
                         :type ~type
                         :holder-id (:id token-data))) id))

(defapi [:rule "/volunteer/create/outside" 
         :method "POST" 
         :params OutsideVolunteer
         :doc "创建校外义工"]
  create-outside-volunteer [#^str name 
                            #^str description 
                            #^datetime time 
                            #^int reward 
                            #^(of list str) joiners]
  (let [id (_create-volunteer VolType.OUTSIDE)]
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
    (success )))

(defmacro [:rule "/volunteer/<int:id>/audit/accept"
           :method "POST"
           :auth Categ.CLASS
           :doc "审核通过义工"]
  )

(defapi [:rule "/volunteer/create/special"
         :method "POST"
         :auth Categ.MANAGER
         :params SpecialVolunteer
         :doc "创建特殊义工(竞赛等)"]
  create-special-volunteer [#^str name
                            #^VolType type
                            #^int reward
                            #^(of list str) joiners]
  (let [id (. (insert (Volunteer :name name
                                 :description ""
                                 :status VolStatus.ACCEPTED
                                 :holder-id (:id token-data)
                                 :time (inexact-now)
                                 :type type
                                 :reward reward)) id)
        not (inexact-now)
        notice-id (. (insert (Notice :title "义工时间"
                                     :content (.format "您由于{}获得了{}义工时间" name reward)
                                     :sender 0
                                     :sendtime now
                                     :deadtime (+ now (timedelta :days 3)))) id)]
    (for [joiner joiners]
      (let [joiner (. (User.get/error joiner ErrorCode.USER-NOT-FOUND) id)]
        (insert (StuVol :vol-id id
                        :stu-id joiner
                        :status ThoughtStatus.ACCEPTED
                        :thought name
                        :reason ""
                        :reward reward))
        (insert (UserNotice :user-id joiner
                            :notice-id notice-id))))))