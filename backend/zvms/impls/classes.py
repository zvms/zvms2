from zvms.models import Class
from zvms.res import *
from zvms.util import *

#[GET] /classes
def list_classes(token_data):
    return success('获取成功', list(Class.query.select('id', 'name')))

#[GET] /classes/<int:id>
def get_class_info(id, token_data):
    cls = Class.query.get_or_error(id)
    members = cls.members
    def filter_(auth):
        return list(apply(select)(filter(lambda m: (m.auth & auth), members), 'id', 'name'))
    return success('获取成功',
        teachers=filter_(AUTH.TEACHER),
        students=filter_(AUTH.STUDENT)
    )