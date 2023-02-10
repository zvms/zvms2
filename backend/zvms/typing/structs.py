from zvms.typing.checker import *
from zvms.res import VolType, VolStatus, ThoughtStatus

Class = Object(
    name=String(5)
)

SingleClass = Object(
    id=Int,
    name=String()
)

SingleUserWithoutAuth = Object(
    id=Int,
    name=String()
)

SingleUser = Extends(SingleUserWithoutAuth,
    auth=Int
)

ListClassesResponse = Array(SingleClass)

ClassInfoResponse = Object(
    name=String(),
    students=Array(SingleUser),
    teachers=Array(SingleUser)
)

UserLoginResponse = Object(
    token=String()
)

SearchUsersResponse = Array(SingleUser)

UserInfoResponse = Object(
    name=String(),
    cls=Int,
    auth=Int,
    clsName=String()
)

VolunteerTimeResponse = Object(
    inside=Int,
    outside=Int,
    large=Int
)

SingleNotice = Object(
    id=Int,
    title=String(),
    content=String(),
    sender=Int,
    deadtime=String(),
    senderName=String()
)

SearchNoticesResponse = Array(SingleNotice)

SingleSignup = Object(
    volId=Int,
    volName=String(),
    stuId=Int,
    stuName=String(),
)

ListSignupResponse = Array(SingleSignup)

SingleVolunteer = Object(
    id=Int,
    name=String(),
    time=String(),
    status=Int
)

SearchVolunteersResponse = Array(SingleVolunteer)

VolunteerInfoResponse = Object(
    name=String(),
    description=String(),
    time=String(),
    type=Int,
    reward=Int,
    joiners=Array(SingleUserWithoutAuth),
    holder=Int,
    holderName=String()
)

SearchNotices = Optional(
    sender=Int,
    user=Int,
    cls=Int,
    school=Any
)

NoticeBody = Object(
    title=String(32),
    content=String(1024),
    deadtime=String(19)
)

Notice = Extends(NoticeBody,
    targets=Array(Int)
)

Report = Object(
    report=String()
)

Signup = Object(
    students=Array(Int)
)

SearchThoughts = Optional(
    cls=Int,
    status=Literal(
        ThoughtStatus.ACCEPTED,
        ThoughtStatus.UNSUBMITTED,
        ThoughtStatus.DRAFT,
        ThoughtStatus.WAITING_FOR_FINAL_AUDIT,
        ThoughtStatus.WAITING_FOR_FINAL_AUDIT
    ),
    student=Int,
    Volunteer=Int
)

Thought = Object(
    thought=String(1024),
    pictures=Array(String())
)

Login = Object(
    id=Int,
    pwd=String(32)
)

SearchUsers = Optional(
    name=String(),
    cls=Int,
    auth=Int
)

ModPwd = Object(
    old=String(32),
    neo=String(32)
)

ChangeClass = Object(
    cls=Int
)

User = Object(
    name=String(5),
    cls=Int,
    auth=Int
)

OneUser = Extends(User,
    id=Int
)

Users = Object(
    users=Array(OneUser)
)

ClassVol = Object(
    id=Int,
    max=Int
)

SearchVolunteers = Optional(
    holder=Int,
    student=Int,
    cls=Int,
    name=String(),
    status=Literal(VolStatus.UNAUDITED, VolStatus.AUDITED)
)

Volunteer = Object(
    name=String(32),
    description=String(1024),
    time=String(20),
    type=Literal(VolType.INSIDE, VolType.OUTSIDE, VolType.LARGE),
    reward=Int,
    classes=Array(ClassVol)
)

Repulse = Object(
    reason=String(1024)
)