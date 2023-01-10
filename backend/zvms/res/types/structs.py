import typing


NoticeBody = typing.TypedDict('NoticeBody', {
    'title': str,
    'content': str,
    'deadtime': str
})
Notice = typing.TypedDict('Notice', {
    'title': str,
    'content': str,
    'deadtime': str,
    'type': int,
    'targets': typing.Sequence[int]
})
Report = typing.TypedDict('Report', {
    'content': str
})
VolunteerRecordClass = typing.TypedDict('VolunteerRecordClass', {
    'id': int,
    'max': int
})
VolunteerRecord = typing.TypedDict('VolunteerRecord', {
    'name': str,
    'description': str,
    'time': str,
    'type': int,
    'reward': int,
    'classes': typing.Sequence[VolunteerRecordClass]
})
UserOfUsers = typing.TypedDict('UserOfUsers', {
    'id': int,
    'name': str,
    'cls': int,
    'auth': int,
    'pwd': str
})
Users = typing.TypedDict('Users', {
    'users': typing.Sequence[UserOfUsers]
})
User = typing.TypedDict('User', {
    'name': str,
    'cls': int,
    'auth': int
})
