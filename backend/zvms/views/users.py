from zvms.routelib import route
from zvms.views.structs import Login, ModPwd, ChangeClass, Users, User
from zvms.res import Categ
import zvms.impls.users

route(
    rule='/check',
    method='GET',
    impl_func=zvms.impls.users.check
)

route(
    rule='/users/login',
    method='POST',
    impl_func=zvms.impls.users.login,
    params=Login,
    auth=None
)

route(
    rule='/users/logout',
    method='POST',
    impl_func=zvms.impls.users.logout
)

route(
    rule='/users',
    method='GET',
    impl_func=zvms.impls.users.search_users
)

route(
    rule='/users/<int:id>',
    method='GET',
    impl_func=zvms.impls.users.get_user_info
)

route(
    rule='/users/mod-pwd',
    method='PATCH',
    impl_func=zvms.impls.users.modify_password,
    params=ModPwd,
)

route(
    rule='/users/change-class',
    method='PATCH',
    impl_func=zvms.impls.users.change_class,
    auth=Categ.TEACHER,
    params=ChangeClass
)

route(
    rule='/users/<int:id>',
    method='DELETE',
    impl_func=zvms.impls.users.delete_user,
    auth=Categ.SYSTEM
)

route(
    rule='/users',
    method='POST',
    impl_func=zvms.impls.users.create_users,
    auth=Categ.SYSTEM,
    params=Users
)

route(
    rule='/users/<int:id>',
    method='PUT',
    impl_func=zvms.impls.users.modify_user,
    auth=Categ.SYSTEM,
    params=User
)