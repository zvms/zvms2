from zvms.routelib import *
from zvms.res import AUTH
from zvms.views.structs import Notice, NoticeBody
import zvms.impls.notices

route(
    rule='/notices',
    method='GET',
    impl_func=zvms.impls.notices.search_notices
)

route(
    rule='/notices',
    method='POST',
    impl_func=zvms.impls.notices.send_notice,
    params=Notice,
    auth=AUTH.MANAGER | AUTH.TEACHER
)

route(
    rule='/notices/<int:id>',
    method='DELETE',
    impl_func=zvms.impls.notices.delete_notice,
    auth=AUTH.MANAGER | AUTH.TEACHER
)

route(
    rule='/notices/<int:id>',
    method='PUT',
    impl_func=zvms.impls.notices.update_notice,
    auth=AUTH.MANAGER | AUTH.TEACHER,
    params=NoticeBody
)