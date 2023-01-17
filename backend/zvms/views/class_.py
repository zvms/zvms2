from zvms.routelib import *
from zvms.typing.structs import Class
import zvms.impls.class_

route(
    rule='/class/list',
    method='GET',
    impl_func=zvms.impls.class_.list_classes
)

route(
    rule='/class/<int:id>',
    method='GET',
    impl_func=zvms.impls.class_.get_class_info
)

route(
    rule='/class/create',
    method='POST',
    impl_func=zvms.impls.class_.create_class,
    categ=Categ.SYSTEM,
    params=Class
)

route(
    rule='/class/<int:id>/delete',
    method='POST',
    impl_func=zvms.impls.class_.delete_class,
    categ=Categ.SYSTEM
)

route(
    rule='/class/<int:id>/modify',
    method='POST',
    impl_func=zvms.impls.class_.modify_class,
    categ=Categ.SYSTEM
)