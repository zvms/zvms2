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
    categ=None
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
    categ=Categ.TEACHER,
    params=ChangeClass
)

route(
    rule='/user/<int:id>/delete',
    method='POST',
    impl_func=zvms.impls.user.delete_user,
    categ=Categ.SYSTEM
)

route(
    rule='/user/create',
    method='POST',
    impl_func=zvms.impls.user.create_user,
    categ=Categ.SYSTEM,
    params=Users
)

route(
    rule='/user/<int:id>',
    method='PUT',
    impl_func=zvms.impls.user.modify_user,
    categ=Categ.SYSTEM,
    params=User
)