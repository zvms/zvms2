from zvms.typing.structs import *
from zvms.impls.class_ import *
from zvms.routelib import route
from zvms.res import Categ

route(
    impl=list_classes,
    rule='/class/list',
    method='GET',
    params=Any,
    auth=Categ.ANY
)

route(
    impl=get_class_info,
    rule='/class/<int:id>',
    method='GET',
    params=Any,
    auth=Categ.ANY
)

route(
    impl=delete_class,
    rule='/class/<int:id>/delete',
    method='POST',
    params=Any,
    auth=Categ.SYSTEM
)

route(
    impl=create_class,
    rule='/class/create',
    method='POST',
    params=Class,
    auth=Categ.SYSTEM
)

route(
    impl=modify_class,
    rule='/class/<int:id>/modify',
    method='POST',
    params=Class,
    auth=Categ.SYSTEM
)