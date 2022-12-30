from zvms.routelib import *

Class = Object(
    name=String
)

NoticeBody = Object(
    title=String,
    content=String,
    deadtime=String
)

Notice = Extends(NoticeBody,
    type=Int,
    target=Union(Int, Null)
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

ModPwd = Object(
    old=String,
    new=String
)

ChangeClass = Object(
    cls=Int,
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

Users = Object(
    users=Array(
        Object(
            id=Int,
            name=String,
            cls=Int,
            auth=Int,
            pwd=String
        )
    )
)

User = Object(
    name=String,
    cls=Int,
    auth=Int
)