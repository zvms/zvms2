(import datetime [timedelta]
        base64 [b64decode]
        typing [Optional]
        binascii
        requests
        os.path
        zvms.apilib *
        zvms.res *
        zvms.util [md5ify])

(require zvms.apilib *
         zvms.util [select
                    select-many
                    case
                    of
                    with-name])

(defapi [:rule "/thought/<int:vol-id>/signup"
         :method "POST"
         :models [Volunteer Student ClassVol StuVol]
         :params SignupVolunteer
         :doc "报名一个义工"]
  signup-volunteer [#^(of list str) students]
  (import zvms.models [auth-self auth-class])
  (let [vol (get/error Volunteer vol-id ErrorCode.VOLUNTEER-NOT-FOUND)
        stu-names []
        now (inexact-now)
        deadtime (+ now (timedelta :days 10))]
    (cond
      (!= vol.status VolStatus.AUDITED)
      (error ErrorCode.VOLUNTEER-NOT-AUDITED)
      (< vol.time now)
      (error ErrorCode.VOLUNTEER-FINISHED)
      True
      (do (for [stu-id students]
            (let [stu (Student.get/error stu-id ErrorCode.USER-NOT-FOUND)
                  cv (get/error ClassVol #(vol-id stu.class-id) ErrorCode.CLASS-NOT-PERMITTED)]
              (cond
                (StuVol.query.get #(vol-id stu.id))
                  (return (error ErrorCode.STUDENT-ALREADY-JOINED stu-id))
                (>= cv.now cv.max)
                  (return (error ErrorCode.VOLUNTEER-LIMITS-EXCEEDED))
                (authorized Categ.CLASS (:auth token-data))
                  (auth-class stu.id token-data)
                True
                  (auth-self stu-id token-data))
              (stu-names.append stu.name)
              (insert (StuVol :stu-id stu.id
                              :vol-id vol-id
                              :status (if (= (:auth token-data) 0)
                                        ThoughtStatus.WAITING-FOR-SIGNUP-AUDIT
                                        ThoughtStatus.DRAFT)
                              :thought ""
                              :reward -1))))
          (insert (UserNotice :user-id vol.holder-id
                              :notice-id (. (insert (Notice :title "学生报名"
                                                            :content (.format "学生{}报名了你的义工{}"
                                                                              (.join ", " stu-names)
                                                                              vol.name)
                                                            :sendtime now
                                                            :deadtime deadtime
                                                            :sender 0)) id)))
          (success)))))

(defstruct SingleSignup
  #^int vol-id
  #^str vol-name
  #^int stu-id
  #^int stu-name)

(defapi [:rule "/thought/signup/list/<int:cls-id>"
         :models [StuVol Volunteer]
         :returns (of list SingleSignup)
         :doc "列出一个班级的所有报名"]
  list-signup []
  (success (select-many (gfor sv (StuVol.query) :if (= sv.stu.class-id cls-id) sv)
                        stu-id
                        vol-id
                        stu-id as stu-name with (with-name User)
                        vol-id as vol-name with (with-name Volunteer))))

(defstruct SingleThought
  #^ThoughtStatus status
  #^int stu-id
  #^int vol-id
  #^int stu-name
  #^int vol-name
  #^datetime time)

(defmacro optional-arg [name]
  `(unpack-iterable (if (is ~name None)
                      #()
                      #(= (. StuVol ~name) (int name)))))

; 目前需要GET可选参数的API只有这一个, 因此写法有点奇怪
; 前端需要将整形的学生ID和状态转换为字符串型, 如果不需要其中一个选项, 传入null
(defapi [:rule "/thought/search"
         :models [StuVol]
         :params SearchThoughts
         :returns (of list SingleThought)
         :doc "搜索感想"]
  search-thoughts [#^(of Optional str) stu-id
                   #^(of Optional str) status]
  (let [conds [(optional-arg stu-id) (optional-arg status)]]
    (success (select-many (. StuVol query (filter #* conds) (order-by (StuVol.vol-id.desc)))
                          status
                          stu-id
                          vol-id
                          stu-id as stu-name with (with-name User)
                          select vol
                            name as vol-name
                            time as vol-time with str))))

(defstruct ThoughtInfoResponse
  #^ThoughtStatus status
  #^str reason
  #^int reward
  #^(of list str) pics
  #^bool repulsed)

(defapi [:rule "/thought/<int:vol-id>/<int:stu-id>"
         :models [Thought]
         :returns ThoughtInfoResponse
         :doc "获取一个感想的详细信息"]
  get-thought-info []
  (success (select (get/error Thought #(vol-id stu-id))
                   status
                   reason with (fn [s] (or s ""))
                   reward
                   pics
                   thought
                   reason as repulsed with (fn [s] (not? s None)))))

(defn _auth-thought [#^int stu-id #^TokenData token-data]
  (if (& Categ.CLASS (:auth token-data))
    (or (auth-class (. (get/error User stu-id) class-id) token-data) True)
    (and (auth-self stu-id token-data) False)))

(defn _save-thought [#^int vol-id 
                     #^int stu-id 
                     #^str thought 
                     #^(of list str) pics
                     #^ThoughtStatus status]
  (import zvms.models [StuVol])
  (let [_thought (get/error StuVol #(vol-id stu-id))
        ids #{}]
    (case _thought.status
      ThoughtStatus.DRAFT ...
      ThoughtStatus.WAITING-FOR-SIGNUP-AUDIT 
        (raise (ZvmsError ErrorCode.CANT-BE-SUBMITTED))
      else
        (raise (ZvmsError ErrorCode.BO-DUPLICATED-SUBMIT)))
    (thought.update :status status
                    :thought _thought)
    (for [pic pics]
      (when (is (Picture.query.get #(pic vol-id stu-id)) None)
        (insert (Picture :pic-id pic 
                         :vol-id vol-id 
                         :stu-id stu-id)))
      (ids.add pic))
    (. Picture query 
       (filter-by :stu-id stu-id 
                  :vol-id vol-id)
       (filter (Picture.identifier.not-in ids))
       (delete))))

(defapi [:rule "/thought/<int:vol-id>/<int:stu-id>/save"
         :method "POST"
         :params Thought
         :doc "保存感想草稿"]
  save-thought [#^str thought #^(of list str) pics]
  (_auth-thought stu-id token-data)
  (_save-thought vol-id stu-id thought pics ThoughtStatus.DRAFT)
  (success))

(defapi [:rule "/thought/<int:vol-id>/<int:stu-id>/submit"
         :method "POST"
         :params Thought
         :doc "提交感想"]
  submit-thought [#^str thought #^(of list str) pics]
  (_save-thought vol-id stu-id thought pics
                 (if (_auth-thought stu-id token-data)
                   ThoughtStatus.WAITING-FOR-FINAL-AUDIT
                   ThoughtStatus.WAITING-FOR-FIRST-AUDIT))
  (success))

(defmacro auth-thought-api [rule
                            auth
                            doc
                            name
                            additional-param
                            need-auth-class
                            expected-status
                            expectation-fails-code
                            thought-updates
                            subsequent-status
                            notice-title
                            notice-content]
  `(defapi [:rule ~(+ "/thought/<int:vol-id>/<int:stu-id>/" rule)
            :method "POST"
            :models [User StuVol UserNotice Notice]
            :auth ~auth
            :doc ~doc
            ~@(if (= additional-param 'None)
                #()
                #(:param (get additional-param 0)))]
     ~name [~@(if (= additional-param 'None)
               #()
               #((get additional-param 1)))]
     ~@(if (= need-auth-class 'True)
         #('(auth-class (. User query (get stu-id) class-id) token-data))
         #())
     (let [thought (get/error StuVol #(vol-id stu-id))
           now (inexact-now)
           deadtime (+ now (timedelta :days 10))]
       (if (!= thought.status (. ThoughtStatus ~expected-status))
         (error (. ErrorCode ~expectation-fails-code))
         (do (thought.update :status (. ThoughtStatus ~subsequent-status)
                             ~@thought-updates)
             (insert (UserNotice :user-id thought.stu-id
                                 :notice-id (. (insert (Notice :title ~notice-title
                                                               :content (.format ~notice-content thought.vol.name)
                                                               :sendtime now
                                                               :deadtime deadtime
                                                               :sender 0) id))))
             (success))))))

(auth-thought-api "audit"
                  Categ.CLASS
                  "报名审核"
                  signup-audit
                  None
                  True
                  WAITING-FOR-SIGNUP-AUDIT
                  NOT-A-SIGNUP
                  []
                  WAITING-FOR-FIRST-AUDIT
                  "报名审核"
                  "您对{}的报名已通过团支书审核")

(auth-thought-api "first"
                  Categ.CLASS
                  "感想初审"
                  first-audit
                  None
                  True
                  WAITING-FOR-FIRST-AUDIT
                  NO-FIRST-AUDIT
                  []
                  WAITING-FOR-FINAL-AUDIT
                  "感想初审"
                  "您在义工{}提交的感想已通过团支书审核")

(auth-thought-api "accept"
                  Categ.AUDITOR
                  "感想终审" 
                  accept-thought
                  [AcceptThought #^int reward]
                  False
                  WAITING-FOR-FINAL-AUDIT
                  NO-FINAL-AUDIT
                  [:reward reward]
                  ACCEPTED
                  "感想终审"
                  "您在义工{}提交的感想已通过审计部审核")

(auth-thought-api "repulse"
                  Categ.AUDITOR
                  "打回感想"
                  repulse-thought
                  [RepulseThought #^str reason]
                  False
                  WAITING-FOR-FINAL-AUDIT
                  NO-FINAL-AUDIT
                  [:reason reason]
                  DRAFT
                  "打回感想"
                  "您在义工{}提交的感想已被审计部打回")

(defapi [:rule "/thought/picture/fetch/<int:vol-id>"
         :models [Picture]
         :returns (of list str)
         :doc "获取一个义工中所有的图片"]
  fetch-pictures []
  (success (map (itemgetter "identifier") 
                (Picture.query.filter-by :vol-id vol-id))))

(defstruct LocalPicture
  #^str type
  #^str base64)

(defapi [:rule "/thought/picture/upload/local"
         :method "POST"
         :params UploadPictures
         :doc "从本地上传图片"]
  upload-pictures [#^(of list LocalPicture) pics]
  (for [pic pics]
    (let [path (os.path.join STATIC-FOLDER "pics" (+ (md5ify (:base64 pic)) "." (:type pic)))]
      (when (not (os.path.exists path))
        (with [f (open path "wb")]
              (f.write (try
                         (b64decode (:base64 pic))
                         (except [binascii.Error]
                                 (return (error ErrorCode.BASE64-PARSING-ERROR)))))))))
  (success))

(defapi [:rule "/thought/picture/upload/imagebed"
         :method "POST"
         :params FetchPictures
         :doc "从图床拉取图片"]
  fetch-pictures-from-imagebed [#^(of list str) urls #^int vol-id]
  (try
    (success (lfor url urls
                   (let [content (. requests (get url) content)
                         hash (md5ify content)
                         extension (+ hash "." (. url (split ".") [-1]))] 
                     (when (is (Picture.query.get hash) None)
                       (with [f (open (os.path.join STATIC-FOLDER "pics" data "." extension) "wb")]
                             (f.write content)))
                     identifier)))
    (except [requests.exceptions.RequestException]
            (error ErrorCode.PICTURE-UPLOAD-FAILED))))