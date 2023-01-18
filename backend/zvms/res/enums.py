from enum import *


class VolType(IntEnum):
    INSIDE = 1
    OUTSIDE = 2
    LARGE = 3

class VolStatus(IntEnum):
    UNAUDITED = 1
    AUDITED = 2

class ThoughtStatus(IntEnum):
    WAITING_FOR_SIGNUP_AUDIT = 1
    UNSUBMITTED = 2
    DRAFT = 3
    WAITING_FOR_FIRST_AUDIT = 4
    WAITING_FOR_FINAL_AUDIT = 5
    ACCEPTED = 6
    REJECTED = 7

class NoticeType(IntEnum):
    USER_NOTICE = 1
    CLASS_NOTICE = 2
    SCHOOL_NOTICE = 3
