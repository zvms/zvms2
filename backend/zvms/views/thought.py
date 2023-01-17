from zvms.routelib import *
from zvms.typing.structs import Thought
import zvms.impls.thought

route(
    rule='/thought/search',
    method='GET',
    impl_func=zvms.impls.thought.search_thoughts,
)

route(
    rule='/thought/<int:volId>/<int:stuId>',
    method='GET',
    impl_func=zvms.impls.thought.get_thought_info,
)

route(
    rule='/thought/<int:volId>/<int:stuId>/save',
    method='POST',
    impl_func=zvms.impls.thought.save_thought,
    params=Thought,
    categ=Categ.STUDENT
)

route(
    rule='/thought/<int:volId>/<int:stuId>/submit',
    method='POST',
    impl_func=zvms.impls.thought.submit_thought,
    params=Thought,
    categ=Categ.STUDENT
)

route(
    rule='/thought/<int:volId>/<int:stuId>/audit/first',
    method='POST',
    impl_func=zvms.impls.thought.first_audit,
    categ=(Categ.TEACHER | Categ.CLASS)
)

route(
    rule='/thought/<int:volId>/<int:stuId>/audit/final',
    method='POST',
    impl_func=zvms.impls.thought.final_audit,
    categ=Categ.AUDITOR
)

route(
    rule='/thought/<int:volId>/<int:stuId>/audit/repulse',
    method='POST',
    impl_func=zvms.impls.thought.repulse,
    categ=(Categ.TEACHER | Categ.CLASS | Categ.AUDITOR)
)