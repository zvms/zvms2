from zvms.models import *
from zvms.utils import *
from zvms.res import *

#[GET] /notices
def search_notices(token_data, **kwargs):
    conds = []
    try:
        if 'f' in kwargs:
            conds.append(Notice.sender == int(kwargs['f']))
        if 't' in kwargs:
            conds.append(Notice.id.in_(UserNotice.query.filter_by(
                user_id=int(kwargs['t'])).select_value('notice_id')))
        if 'c' in kwargs:
            conds.append(Notice.id.in_(ClassNotice.query.filter_by(
                cls_id=int(kwargs['c'])).select_value('notice_id')))
        if 's' in kwargs:
            conds.append(Notice.id.in_(SchoolNotice.query.select_value('notice_id')))
    except ValueError:
        return error('请求接口错误: 非法的URL参数')
    def process_query(query):
        ret = list(query.select('id', 'title', 'content', 'sender', 'deadtime'))
        for i in ret:
            i['deadtime'] = str(i['deadtime'])
        if not ret:
            return error('未查询到相关数据')
        return success('获取成功', ret)
    if not conds:
        return process_query(Notice.query)
    return process_query(Notice.query.filter(*conds))

#[POST] /notices
def send_notice(title, content, deadtime, type, targets, token_data):
    try_parse_time(deadtime)
    id = Notice(title=title, content=content, deadtime=deadtime,
                sender=token_data['id']).insert().id
    if targets is None and type != NOTICE_TYPE.SCHOOL_NOTICE:
        return error('请求接口错误: 必须指定目标')
    match type:
        case NOTICE_TYPE.USER_NOTICE:
            for i in targets:
                if User.query.get_or_error(i, '未找到目标用户').auth == AUTH.STUDENT and not (token_data['auth'] & AUTH.SYSTEM):
                    return error('不能对普通学生发通知')
                UserNotice(user_id=i, notice_id=id).insert()
        case NOTICE_TYPE.CLASS_NOTICE:
            for i in targets:
                Class.query.get_or_error(i, '未找到目标班级')
                ClassNotice(cls_id=i, notice_id=id).insert()
        case NOTICE_TYPE.SCHOOL_NOTICE:
            SchoolNotice(notice_id=id).insert()
        case _:
            return error('未知的目标类型')
    return success('发送成功')

#[DELETE] /users/<int:id>
def delete_notice(id, token_data):
    notice = Notice.query.get_or_error(id)
    auth_self(notice.sender, token_data, '权限不足: 不能删除其他人的通知')
    Notice.query.filter_by(id=id).delete()
    SchoolNotice.query.filter_by(notice_id=id).delete()
    ClassNotice.query.filter_by(notice_id=id).delete()
    UserNotice.query.filter_by(notice_id=id).delete()
    return success('删除成功')

#[PUT] /notices/<int:id>
def update_notice(id, title, content, deadtime, token_data):
    notice = Notice.query.get_or_error(id)
    auth_self(notice.sender, token_data, '权限不足: 不能修改其他人的通知')
    try_parse_time(deadtime)
    notice.update(
        title=title,
        content=content,
        deadtime=deadtime
    )
    return success('修改成功')