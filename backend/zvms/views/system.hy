(import os
        zvms.apilib *
        zvms.res [START-TTYD
                  STOP-TTYD])

(require zvms.apilib *)

(defapi [:rule "/system/ttyd/restart"
         :method "POST"
         :auth Categ.SYSTEM
         :doc "重启TTYD"]
  restart-ttyd []
  (if (is START-TTYD None)
    (error "TTYD 不受支持")
    (do (os.system STOP-TTYD)
        (if (= (os.system START-TTYD) 0)
          (success "TTYD重启成功")
          (error "TTYD重启失败")))))

(defapi [:rule "/system/restart"
         :method "POST"
         :auth Categ.SYSTEM
         :doc "重启后端"]
  restart-backend []
  (raise ZvmsExit))