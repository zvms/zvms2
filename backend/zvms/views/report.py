from zvms.typing.structs import *
from zvms.impls.report import *
from zvms.routelib import route
from zvms.res import Categ

route(
    impl=report,
    rule='/report',
    method='POST',
    params=Report,
    auth=Categ.ANY
)