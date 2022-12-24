from zvms.routelib import *
from zvms.res import *
import zvms.impls.volunteer

route(
    rule='/volunteers',
    method='GET',
    impl_func=zvms.impls.volunteer.search_volunteers
)

route(
    rule='/volunteers/<int:id>',
    method='GET',
    impl_func=zvms.impls.volunteer.get_volunteer_info,
)

route(
    rule='/volunteers',
    method='POST',
    impl_func=zvms.impls.volunteer.create_volunteer,
    params=Object(
        name=String,
        description=String,
        time=String,
        type=Int,
        reward=Int
    ),
    auth=AUTH.MANAGER | AUTH.TEACHER
)

route(
    rule='/volunteers/<int:id>',
    method='PUT',
    impl_func=zvms.impls.volunteer.update_volunteer,
    params=Object(
        name=String,
        description=String,
        time=String,
        type=Int,
        reward=Int
    ),
    auth=AUTH.MANAGER | AUTH.TEACHER
)

route(
    rule='/volunteers/<int:id>',
    method='DELETE',
    impl_func=zvms.impls.volunteer.delete_volunteer,
    auth=AUTH.MANAGER | AUTH.TEACHER
)