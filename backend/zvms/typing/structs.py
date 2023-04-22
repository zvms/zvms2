from zvms.typing.checker import *
from zvms.res import VolType, VolStatus, ThoughtStatus

class Class(Object):
    name = Len(String, 1, 6)

class SingleClass(Object):
    id = Int
    name = String

class SingleUserWithoutAuth(Object):
    id = Int
    name = String

class SingleUser(SingleUserWithoutAuth):
    auth = Int

ListClassesResponse = Array(SingleClass())
    
class ClassInfoResponse(Object):
    name = String
    students=Array(SingleUser())
    teachers=Array(SingleUser())

class UserLoginResponse(Object):
    token = String
    id = Int

SearchUsersResponse = Array(SingleUser())

class UserInfoResponse(Object):
    name = String
    cls = Int
    auth = Int
    clsName = String

class PictureResponse(Object):
    hash = String
    type = String

class ThoughtInfoResponse(Object):
    status = Enum(ThoughtStatus)
    reason = String
    thought = String
    reward = Int
    pics = Array(PictureResponse())

class StudentThoughtsResponse(Object):
    accepted = Array(ThoughtInfoResponse())
    unsubmitted = Array(ThoughtInfoResponse())
    draft = Array(ThoughtInfoResponse())
    unaudited = Array(ThoughtInfoResponse())

class StudentStatResponse(Object):
    inside = Int
    outside = Int
    large = Int

class SingleNotice(Object):
    id = Int
    title = String
    content = String
    sender = Int
    sendtime = DateTime
    deadtime = DateTime
    senderName = String
    
SearchNoticesResponse = Array(SingleNotice())

class SingleSignup(Object):
    volId = Int
    volName = String
    stuId = Int
    stuName = String
    
ListSignupResponse = Array(SingleSignup())

class SingleVolunteer(Object):
    id = Int
    name = String
    time = String
    status = Int
    signable = Boolean
    joiners = Array(SingleUserWithoutAuth())
    holderName = String
    
SearchVolunteersResponse = Array(SingleVolunteer())

class VolunteerInfoResponse(Object):
    name = String
    description = String
    time = String
    status = Enum(VolStatus)
    type = Enum(VolType)
    reward = Int
    signable = Boolean
    joiners = Array(SingleUserWithoutAuth())
    holder = Int
    holderName = String

class SearchNotices(Optional):
    sender = Parsable(Int)
    receiver = Parsable(Int)
    cls = Parsable(Int)
    school = Parsable(Int)

class NoticeBody(Object):
    title = Len(String, 1, 33)
    content = Len(String, 1, 1025)
    deadtime = DateTime
    
class Notice(NoticeBody):
    targets = Array(Int)

class SchoolNotice(NoticeBody):
    anonymous = Boolean

class Report(Object):
    report = Len(String, 1, 256)

class SingleReport(Object):
    content = String
    reporter = Int
    reporterName = String
    time = String

FetchReportsResponse = Array(SingleReport())
    
class Signup(Object):
    students = Array(Int)
    
class SearchThoughts(Optional):
    cls = Parsable(Int)
    status = ParsableEnum(ThoughtStatus)
    student = Parsable(Int)
    volunteer = Parsable(Int)

class SingleThought(Object):
    volId = Int
    stuId = Int
    status = Enum(ThoughtStatus)
    stuName = String
    volName = String

SearchThoughtsResponse = Array(SingleThought())

class ExistedPicture(Object):
    hash = String
    type = Len(String, 3, 6)

class Base64Picture(Object):
    base64 = String
    type = Len(String, 3, 6)

Picture = Union(ExistedPicture(), Base64Picture())

class Thought(Object):
    thought = Len(String, 0, 1025)
    pictures = Array(Picture)

class Login(Object):
    id = String
    pwd = Len(String, 32, 33)

class SearchUsers(Optional):
    name = String
    cls = Parsable(Int)
    auth = Parsable(Int)
    
class ModPwd(Object):
    old = Len(String, 32, 33)
    neo = Len(String, 32, 33)

class User(Object):
    name = Len(String, 1, 6)
    cls = Int
    auth = Int

class OneUser(User):
    id = Int

class Users(Object):
    users = Array(OneUser())

class ClassVol(Object):
    id = Int
    max = Int
    
class SearchVolunteers(Optional):
    holder = Parsable(Int)
    student = Parsable(Int)
    cls = Parsable(Int)
    name = String
    status = ParsableEnum(VolStatus)
    signable = Parsable(Boolean)
    
class VolunteerBody(Object):
    name = Len(String, 1, 33)
    description = Len(String, 1, 1025)
    time = DateTime
    type = Enum(VolType)
    reward = Int

class Volunteer(VolunteerBody):
    classes = Array(ClassVol())

class AppointedVolunteer(VolunteerBody):
    joiners = Array(Int)

class Repulse(Object):
    reason = Len(String, 0, 65)

class Accept(Object):
    reward = Int

class FetchPicture(Object):
    url = String

class PublicNoticeNotNone(Object):
    title = String
    content = String

PublicNotice =  Nullable(PublicNoticeNotNone())