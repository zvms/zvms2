from zvms.typing.structs import *
from zvms.impls.user import *
from zvms.routelib import route
from zvms.res import Categ

route(
    impl=check,
    rule='/user/check',
    method='GET',
    params=Any,
    auth=Categ.ANY
)

route(
    impl=login,
    rule='/user/login',
    method='POST',
    params=Login,
    auth=Categ.ANY
)

route(
    impl=logout,
    rule='/user/logout',
    method='POST',
    params=Any,
    auth=Categ.ANY
)

route(
    impl=search_users,
    rule='/user/search',
    method='GET',
    params=Any,
    auth=Categ.ANY
)

route(
    impl=get_user_info,
    rule='/user/<int:id>',
    method='GET',
    params=Any,
    auth=Categ.ANY
)

route(
    impl=modify_password,
    rule='/user/mod-pwd',
    method='POST',
    params=ModPwd,
    auth=Categ.ANY
)

route(
    impl=change_class,
    rule='/user/change-class',
    method='POST',
    params=ChangeClass,
    auth=Categ.ANY
)

route(
    impl=create_user,
    rule='/user/create',
    method='POST',
    params=Users,
    auth=Categ.SYSTEM
)

route(
    impl=modify_user,
    rule='/user/<int:id>/modify',
    method='POST',
    params=User,
    auth=Categ.SYSTEM
)

route(
    impl=delete_user,
    rule='/user/<int:id>/delete',
    method='POST',
    params=Any,
    auth=Categ.SYSTEM
)