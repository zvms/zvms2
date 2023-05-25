(import os
        zvms.apilib *
        zvms.res [START-TTYD
                  STOP-TTYD
                  ErrorCode])

(require zvms.apilib *)

(defapi [:rule "/system/ttyd/restart"
         :method "POST"
         :auth Categ.SYSTEM
         :doc "重启TTYD"]
  restart-ttyd []
  (if (is START-TTYD None)
    (error ErrorCode.TTYD-NOT-SUPPORTED)
    (do (os.system STOP-TTYD)
        (if (= (os.system START-TTYD) 0)
          (success ErrorCode.TTYD-RESTART)
          (error ErrorCode.TTYD-FAILS)))))

(defapi [:rule "/system/restart"
         :method "POST"
         :auth Categ.SYSTEM
         :doc "重启后端"]
  restart-backend []
  (raise ZvmsExit))