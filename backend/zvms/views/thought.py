from zvms.typing.structs import *
from zvms.impls.thought import *
from zvms.routelib import route
from zvms.res import Categ

route(
    impl=search_thoughts,
    rule='/thought/search',
    method='GET',
    params=SearchThoughts,
    auth=Categ.ANY
)

route(
    impl=get_thought_info,
    rule='/thought/<int:volId>/<int:stuId>',
    method='GET',
    params=Any,
    auth=Categ.ANY
)

route(
    impl=save_thought,
    rule='/thought/<int:volId>/<int:stuId>/save',
    method='POST',
    params=Thought,
    auth=Categ.ANY
)

route(
    impl=submit_thought,
    rule='/thought/<int:volId>/<int:stuId>/submit',
    method='POST',
    params=Thought,
    auth=Categ.ANY
)

route(
    impl=first_audit,
    rule='/thought/<int:volId>/<int:stuId>/audit/first',
    method='POST',
    params=Any,
    auth=Categ.CLASS | Categ.TEACHER
)

route(
    impl=final_audit,
    rule='/thought/<int:volId>/<int:stuId>/audit/final',
    method='POST',
    params=Any,
    auth=Categ.AUDITOR
)

route(
    impl=repulse,
    rule='/thought/<int:volId>/<int:stuId>/repulse',
    method='POST',
    params=Repulse,
    auth=Categ.ANY
)