from zvms.routelib import *
import zvms.impls.users

route(
    rule='/users/login',
    method='POST',
    impl_func=zvms.impls.users.login,
    params=Object(id=Int, pwd=String),
    auth=None
)

route(
    rule='/users/logout',
    method='POST',
    impl_func=zvms.impls.users.logout
)

route(
    rule='/users/<int:id>',
    method='GET',
    impl_func=zvms.impls.users.get_user_info
)

route(
    rule='/users/mod-pwd',
    method='PATCH',
    impl_func=zvms.impls.users.modify_password
)

route(
    rule='/users/change-class',
    method='PATCH',
    impl_func=zvms.impls.users.change_class,
    auth=AUTH.TEACHER
)