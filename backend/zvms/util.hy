(import datetime [datetime])

(defn inexact-now []
  (.replace (datetime.now) :microsecond 0))