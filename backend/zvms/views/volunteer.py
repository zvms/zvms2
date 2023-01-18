from zvms.routelib import *
from zvms.res import *
from zvms.typing.structs import Volunteer
import zvms.impls.volunteer

route(
    rule='/volunteer/search',
    method='GET',
    impl_func=zvms.impls.volunteer.search_volunteers
)

route(
    rule='/volunteer/<int:id>',
    method='GET',
    impl_func=zvms.impls.volunteer.get_volunteer_info,
)

route(
    rule='/volunteer/create',
    method='POST',
    impl_func=zvms.impls.volunteer.create_volunteer,
    params=Volunteer
)

route(
    rule='/volunteer/<int:id>/modify',
    method='POST',
    impl_func=zvms.impls.volunteer.modify_volunteer,
    params=Volunteer
)

route(
    rule='/volunteers/<int:id>',
    method='POST',
    impl_func=zvms.impls.volunteer.delete_volunteer
)

route(
    rule='/volunteer/<int:id>/audit',
    method='POST',
    impl_func=zvms.impls.volunteer.audit_volunteer,
    auth=~Categ.STUDENT
)