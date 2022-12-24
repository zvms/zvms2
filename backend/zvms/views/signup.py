from zvms.routelib import *
from zvms.res import *
import zvms.impls.signup

route(
    rule='/signup',
    method='GET',
    impl_func=zvms.impls.signup.list_signup
)

route(
    rule='/signup/<int:stuId>',
    method='POST',
    impl_func=zvms.impls.signup.signup
)

route(
    rule='/signup/<int:stuId>/<int:volId>',
    method='PATCH',
    impl_func=zvms.impls.signup.audit_signup,
    auth=AUTH.CLASS | AUTH.TEACHER
)