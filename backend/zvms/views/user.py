from zvms.routelib import route
from zvms.typing.structs import Login, ModPwd, ChangeClass, User, Users
from zvms.res import Categ
import zvms.impls.user

route(
    rule='/user/check',
    method='GET',
    impl_func=zvms.impls.user.check
)

route(
    rule='/user/login',
    method='POST',
    impl_func=zvms.impls.user.login,
    params=Login,
    auth=None
)

route(
    rule='/user/logout',
    method='POST',
    impl_func=zvms.impls.user.logout
)

route(
    rule='/user/search',
    method='GET',
    impl_func=zvms.impls.user.search_users
)

route(
    rule='/user/<int:id>',
    method='GET',
    impl_func=zvms.impls.user.get_user_info
)

route(
    rule='/user/mod-pwd',
    method='POST',
    impl_func=zvms.impls.user.modify_password,
    params=ModPwd,
)

route(
    rule='/user/change-class',
    method='POST',
    impl_func=zvms.impls.user.change_class,
    auth=Categ.TEACHER,
    params=ChangeClass
)

route(
    rule='/user/<int:id>/delete',
    method='POST',
    impl_func=zvms.impls.user.delete_user,
    auth=Categ.SYSTEM
)

route(
    rule='/user/create',
    method='POST',
    impl_func=zvms.impls.user.create_user,
    auth=Categ.SYSTEM,
    params=Users
)

route(
    rule='/user/<int:id>',
    method='PUT',
    impl_func=zvms.impls.user.modify_user,
    auth=Categ.SYSTEM,
    params=User
)