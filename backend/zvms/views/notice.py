from zvms.routelib import *
from zvms.res import Categ
from zvms.typing.structs import Notice, NoticeBody
import zvms.impls.notice

route(
    rule='/notice/search',
    method='GET',
    impl_func=zvms.impls.notice.search_notices
)

route(
    rule='/notice/send/school',
    method='POST',
    impl_func=zvms.impls.notice.send_school_notice,
    params=NoticeBody
)

route(
    rule='/notice/send/user',
    method='POST',
    impl_func=zvms.impls.notice.send_user_notice,
    params=Notice,
    categ=Categ.MANAGER | Categ.TEACHER
)

route(
    rule='/notice/send/class',
    method='POST',
    impl_func=zvms.impls.notice.send_class_notice,
    params=Notice,
    categ=Categ.MANAGER | Categ.TEACHER
)

route(
    rule='/notice/<int:id>/delete',
    method='POST',
    impl_func=zvms.impls.notice.delete_notice,
    categ=Categ.MANAGER | Categ.TEACHER
)

route(
    rule='/notice/<int:id>/modify',
    method='POST',
    impl_func=zvms.impls.notice.modify_notice,
    categ=Categ.MANAGER | Categ.TEACHER,
    params=NoticeBody
)