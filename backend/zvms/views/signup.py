from zvms.routelib import *
from zvms.res import *
from zvms.typing.structs import Signup
import zvms.impls.signup

route(
    rule='/signup/list/<int:cls>',
    method='GET',
    impl_func=zvms.impls.signup.list_signup
)

route(
    rule='/signup/<int:volId>',
    method='POST',
    impl_func=zvms.impls.signup.signup,
    params=Signup,
)

route(
    rule='/signup/<int:volId>/<int:stuId>/audit',
    method='POST',
    impl_func=zvms.impls.signup.audit_signup,
    auth=Categ.CLASS | Categ.TEACHER
)

route(
    rule='/signup/<int:volId>/<int:stuId>/rollback',
    method='POST',
    impl_func=zvms.impls.signup.rollback
)