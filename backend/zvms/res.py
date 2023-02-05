from enum import IntEnum, IntFlag
import sys

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
    REJECTED = 6

class NoticeType(IntEnum):
    USER_NOTICE = 1
    USER = 1
    CLASS_NOTICE = 2
    CLS = 2
    SCHOOL_NOTICE = 3
    SCHOOL = 3

class Categ(IntFlag):
    NONE = 1
    STUDENT = 2
    TEACHER = 4
    CLASS = 8
    MANAGER = 16
    AUDITOR = 32
    SYSTEM = 64
    ANY = 127

    def authorized(self, auth):
        return (Categ.SYSTEM | self) & auth