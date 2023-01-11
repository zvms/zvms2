from enum import IntFlag, IntEnum
import sys

if sys.platform == 'win32':
    STATIC_FOLDER = 'C:\zcvms-backend'
elif sys.platform == 'linux':
    STATIC_FOLDER = '/tmp/zvms-backend'

class AUTH(IntFlag):
    NONE    = 0b0000001
    STUDENT = 0b0000010
    TEACHER = 0b0000100
    CLASS   = 0b0001000
    MANAGER = 0b0010000
    AUDITOR = 0b0100000
    SYSTEM  = 0b1000000
    ALL     = 0b1111111

    def authorized(self, that):
        return (self | AUTH.SYSTEM) & that

class VOL_TYPE(IntEnum):
    INSIDE = 1
    OUTSIDE = 2
    LARGE = 3

class STATUS(IntEnum):
    WAITING_FOR_SIGNUP_AUDIT = 1
    UNSUBMITTED = 2
    WAITING_FOR_FIRST_AUDIT = 3
    WAITING_FOR_FINAL_AUDIT = 4
    ACCEPTED = 5
    REJECTED = 6

class NOTICE_TYPE(IntEnum):
    USER_NOTICE = 1
    CLASS_NOTICE = 2
    SCHOOL_NOTICE = 3