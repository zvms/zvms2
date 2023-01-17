from zvms.routelib import route
from zvms.typing.structs import Report
import zvms.impls.report

route(
    rule='/report',
    method='POST',
    impl_func=zvms.impls.report.report,
    params=Report,
    categ=None
)