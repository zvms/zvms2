from zvms.routelib import *
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