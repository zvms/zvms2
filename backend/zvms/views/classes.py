from zvms.routelib import *
from zvms.views.structs import Class
import zvms.impls.classes

route(
    rule='/classes',
    method='GET',
    impl_func=zvms.impls.classes.list_classes
)

route(
    rule='/classes/<int:id>',
    method='GET',
    impl_func=zvms.impls.classes.get_class_info
)

route(
    rule='/classes',
    method='POST',
    impl_func=zvms.impls.classes.create_class,
    auth=Categ.SYSTEM,
    params=Class
)

route(
    rule='/classes/<int:id>',
    method='DELETE',
    impl_func=zvms.impls.classes.delete_class,
    auth=Categ.SYSTEM
)

route(
    rule='/classes/<int:id>',
    method='PUT',
    impl_func=zvms.impls.classes.modify_class,
    auth=Categ.SYSTEM
)