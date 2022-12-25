from zvms.routelib import *

NoticeBody = Object(
    title=String,
    content=String,
    deadtime=String
)

Notice = Extends(NoticeBody,
    type=Int,
    target=Option(Int, Null)
)

Report = Object(
    report=String
)

Signup = Object(
    volId=Int
)

Login = Object(
    id=Int,
    pwd=String
)

Volunteer = Object(
    name=String,
    description=String,
    time=String,
    type=Int,
    reward=Int,
    classes=Array(Object(
        id=Int,
        max=Int
    ))
)