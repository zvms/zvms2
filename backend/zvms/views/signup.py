from zvms.typing.structs import *
from zvms.impls.signup import *
from zvms.routelib import route
from zvms.res import Categ

route(
    impl=list_signup,
    rule='/signup/list/<int:cls>',
    method='GET',
    params=Any,
    auth=Categ.ANY
)

route(
    impl=audit_signup,
    rule='/signup/<int:volId>/<int:stuId>/audit',
    method='POST',
    params=Any,
    auth=Categ.CLASS | Categ.TEACHER
)

route(
    impl=signup,
    rule='/signup/<int:volId>',
    method='POST',
    params=Signup,
    auth=Categ.ANY
)

route(
    impl=rollback,
    rule='/signup/<int:volId>/<int:stuId>/rollback',
    method='POST',
    params=Any,
    auth=Categ.ANY
)