(import zvms.apilib *
        zvms.util [inexact-now])

(require zvms.apilib *
         zvms.util [select
                    select-many])

(defapi [:rule "/issue/new"
         :method "POST"
         :params Issue
         :doc "发送反馈"]
  send-issue [#^str content]
  (insert (Issue
           :time (inexact-now)
           :author (:id token-data)
           :content content))
  (success "反馈成功"))

(defstruct FetchIssuesResponse
  #^int author
  #^str content
  #^str time
  #^str author-name)

(defapi [:rule "/issue/fetch"
         :returns FetchIssuesResponse
         :auth Categ.MANAGER
         :doc "获取反馈"] 
  fetch-issues []
  (success "获取成功" (select-many Issue.query
                               author
                               content
                               time with str
                               author as author-name with (fn [id] (. User query (get id) name)))))