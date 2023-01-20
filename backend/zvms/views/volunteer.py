from zvms.typing.structs import *
from zvms.impls.volunteer import *
from zvms.routelib import route
from zvms.res import Categ

route(
    impl=search_volunteers,
    rule='/volunteer/search',
    method='GET',
    params=SearchVolunteers,
    auth=Categ.ANY
)

route(
    impl=get_volunteer_info,
    rule='/volunteer/<int:id>',
    method='GET',
    params=Any,
    auth=Categ.ANY
)

route(
    impl=create_volunteer,
    rule='/volunteer/create',
    method='POST',
    params=Volunteer,
    auth=Categ.ANY
)

route(
    impl=modify_volunteer,
    rule='/volunteer/<int:id>/modify',
    method='POST',
    params=Volunteer,
    auth=Categ.ANY
)

route(
    impl=delete_volunteer,
    rule='/volunteer/<int:id>/delete',
    method='POST',
    params=Any,
    auth=Categ.ANY
)

route(
    impl=audit_volunteer,
    rule='/volunteer/<int:id>/audit',
    method='POST',
    params=Any,
    auth=Categ.CLASS | Categ.TEACHER
)