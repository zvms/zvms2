from zvms.routelib import *
import zvms.impls.thoughts

route(
    rule='/thoughts',
    method='GET',
    impl_func=zvms.impls.thoughts.search_thoughts,
)

route(
    rule='/thoughts/<int:stuId>/<int:volId>',
    method='PATCH',
    impl_func=zvms.impls.thoughts.update_thought
)