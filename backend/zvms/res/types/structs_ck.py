from zvms.util import *


NoticeBody = Object(
    title=String,
    content=String,
    deadtime=String
)
Notice = Object(
    title=String,
    content=String,
    deadtime=String,
    type=Int,
    targets=Array(Int)
)
Report = Object(
    content=String
)
VolunteerRecordClass = Object(
    id=Int,
    max=Int
)
VolunteerRecord = Object(
    name=String,
    description=String,
    time=String,
    type=Int,
    reward=Int,
    classes=Array(VolunteerRecordClass)
)
UserOfUsers = Object(
    id=Int,
    name=String,
    cls=Int,
    auth=Int,
    pwd=String
)
Users = Object(
    users=Array(UserOfUsers)
)
User = Object(
    name=String,
    cls=Int,
    auth=Int
)
