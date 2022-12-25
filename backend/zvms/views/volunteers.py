from zvms.routelib import *
from zvms.res import *
from zvms.views.structs import Volunteer
import zvms.impls.volunteers

route(
    rule='/volunteers',
    method='GET',
    impl_func=zvms.impls.volunteers.search_volunteers
)

route(
    rule='/volunteers/<int:id>',
    method='GET',
    impl_func=zvms.impls.volunteers.get_volunteer_info,
)

route(
    rule='/volunteers',
    method='POST',
    impl_func=zvms.impls.volunteers.create_volunteer,
    params=Volunteer,
    auth=AUTH.MANAGER | AUTH.TEACHER
)

route(
    rule='/volunteers/<int:id>',
    method='PUT',
    impl_func=zvms.impls.volunteers.update_volunteer,
    params=Volunteer,
    auth=AUTH.MANAGER | AUTH.TEACHER
)

route(
    rule='/volunteers/<int:id>',
    method='DELETE',
    impl_func=zvms.impls.volunteers.delete_volunteer,
    auth=AUTH.MANAGER | AUTH.TEACHER
)