from zvms.routelib import *
import zvms.impls.report

route(
    rule='/report',
    method='POST',
    impl_func=zvms.impls.report.report,
    params=Object(report=String),
    auth=None
)