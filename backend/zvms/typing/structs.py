from zvms.typing.checker import *
from zvms.res import VolType

Class = Object(
    name=String(5)
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

Thought = Object(
    thought=String(1024),
    pictures=Array(String())
)

Login = Object(
    id=Int,
    pwd=String(32)
)

ModPwd = Object(
    old=String(32),
    new=String(32)
)

ChangeClass = Object(
    cls=Int
)

User = Object(
    name=String(5),
    cls=Int,
    categ=Int
)

Users = Object(
    users=Array(Extends(User,
        id=Int
    ))
)

Volunteer = Object(
    name=String(32),
    description=String(1024),
    time=String(20),
    type=Literal(VolType.INSIDE, VolType.OUTSIDE, VolType.LARGE),
    reward=Int,
    classes=Array(Object(
        id=Int,
        max=Int
    ))
)