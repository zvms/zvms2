from zvms.typing.structs import *
from zvms.impls.notice import *
from zvms.routelib import route
from zvms.res import Categ

route(
    impl=search_notices,
    rule='/notice/search',
    method='GET',
    params=Any,
    auth=Categ.ANY
)

route(
    impl=send_user_notice,
    rule='/notice/send/user',
    method='POST',
    params=Notice,
    auth=Categ.MANAGER | Categ.TEACHER
)

route(
    impl=send_class_notice,
    rule='/notice/send/class',
    method='POST',
    params=Notice,
    auth=Categ.MANAGER | Categ.TEACHER
)

route(
    impl=send_school_notice,
    rule='/notice/send/school',
    method='POST',
    params=NoticeBody,
    auth=Categ.MANAGER | Categ.TEACHER
)

route(
    impl=delete_notice,
    rule='/notice/<int:id>/delete',
    method='POST',
    params=Any,
    auth=Categ.MANAGER | Categ.TEACHER
)

route(
    impl=modify_notice,
    rule='/notice/<int:id>/modify',
    method='POST',
    params=NoticeBody,
    auth=Categ.MANAGER | Categ.TEACHER
)