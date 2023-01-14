from enum import Enum


class VolType(Enum):
    INSIDE: 1
    OUTSIDE: 2
    LARGE: 3

class Status(Enum):
    WAITING_FOR_SIGNUP_AUDIT: 1
    UNSUBMITTED: 2
    WAITING_FOR_FIRST_AUDIT: 3
    WAITING_FOR_FINAL_AUDIT: 4
    ACCEPTED: 5
    REJECTED: 6

class NoticeType(Enum):
    USER_NOTICE: 1
    CLASS_NOTICE: 2
    SCHOOL_NOTICE: 3
