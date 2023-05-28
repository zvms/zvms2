(import enum [IntEnum IntFlag]
        sys)

(eval-when-compile
 (import zvms.util [flatten1]))

(defmacro sequential-enum [name #* fields]
  `(defclass ~name [IntEnum]
     (setv ~@(flatten1 (gfor [i n] (enumerate fields 1) #(n i))))))

(sequential-enum ErrorCode
                 ERROR-404
                 ERROR-500
                 NOT-AUTHORIZED
                 TOKEN-NOT-FOUND
                 INTERFACE-ERROR
                 RESPONSE-ERROR
                 NO-RELEVANT-DATA
                 USER-NOT-FOUND
                 TTYD-NOT-SUPPORTED
                 TTYD-RESTART
                 TTYD-FAILS
                 LOGIN-FREQUENTLY
                 INCORRECT-PASSWORD
                 BAD-PASSWORD
                 INCORRECT-OLD-PASSWORD
                 NO-ACCESS-TO-OTHER-CLASSES
                 CLASS-NOT-FOUND
                 VOLUNTEER-MEMBERS-OVERFLOWN
                 VOLUNTEER-NOT-FOUND
                 VOLUNTEER-NOT-AUDITED
                 VOLUNTEER-FINISHED
                 STUDENT-ALREADY-JOINED
                 CLASS-NOT-PERMITTED
                 VOLUNTEER-LIMITS-EXCEEDED
                 CANT-BE-SUBMITTED
                 NO-DUPLICATED-SUBMIT
                 PICTURE-UPLOAD-FAILED
                 BASE64-PARSING-ERROR)

(sequential-enum VolType
                 INSIDE
                 OUTSIDE
                 LARGE)

(sequential-enum VolStatus
                 UNAUDITED 
                 AUDITED 
                 REJECTED 
                 FINISHED 
                 DEPRECATED)

(sequential-enum ThoughtStatus
                 WAITING-FOR-SIGNUP-AUDIT
                 DRAFT
                 WAITING-FOR-FIRST-AUDIT
                 WAITING-FOR-FINAL-AUDIT
                 ACCEPTED
                 SPECIAL)

(sequential-enum NoticeType
                 USER-NOTICE
                 CLASS-NOTICE
                 SCHOOL-NOTICE)

(defclass Categ [IntFlag]
  (setv NONE 1
        CLASS 2
        MANAGER 4
        AUDITOR 8
        SYSTEM 16
        INSPECTOR 32
        ANY 63))

(defn authorized [#^Categ auth #^Categ needed]
  (& (| Categ.SYSTEM auth) needed))

(setv PORT 11451
      STATIC-FOLDER (match sys.platform
                      "win32" "C:\\zvms_backend"
                      "linux" "/tmp/zvms_backend")
      START-TTYD r"start powershell C:\Users\Public\workspace\ttyd\start.ps1"
      STOP-TTYD r"taskkill /im ttyd.exe /f"
      MAIN-MENU-NOTICE r"C:\Users\Public\workspace\public_notice.txt")