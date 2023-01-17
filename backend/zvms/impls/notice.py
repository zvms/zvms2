from zvms.models import *
from zvms.util import *
from zvms.res import *


def search_notices(token_data, **kwargs):
    '[GET] /notic/search'
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
            conds.append(Notice.id.in_(
                SchoolNotice.query.select_value('notice_id')))
    except ValueError:
        return error(400, '请求接口错误: 非法的URL参数')

    def process_query(query):
        ret = list(query.select('id', 'title',
                   'content', 'sender', 'deadtime'))
        for i in ret:
            i['deadtime'] = str(i['deadtime'])
        if not ret:
            return error(404, '未查询到相关数据')
        return success('获取成功', ret)
    if not conds:
        return process_query(Notice.query)
    return process_query(Notice.query.filter(*conds))


def _save_notice(title, content, deadtime, token_data):
    try_parse_time(deadtime)
    return Notice(
        title=title,
        content=content,
        deadtime=deadtime,
        sender=token_data['id']
    ).insert().id


def send_user_notice(title, content, deadtime, targets, token_data):
    '[POST] /notice/send/user'
    id = _save_notice(title, content, deadtime, token_data)
    for i in targets:
        if User.query.get_or_error(i, '未找到目标用户').categ == Categ.STUDENT and not (token_data['categ'] & Categ.SYSTEM):
            return error(403, '不能对普通学生发通知')
        UserNotice(user_id=i, notice_id=id).insert()
    return success('发送成功')


def send_class_notice(title, content, deadtime, targets, token_data):
    '[POST] /notice/send/class'
    id = _save_notice(title, content, deadtime, token_data)
    for i in targets:
        Class.query.get_or_error(i, '未找到目标班级')
        ClassNotice(cls_id=i, notice_id=id).insert()
    return success('发送成功')

def send_school_notice(title, content, deadtime, token_data):
    '[POST] /notice/send/school'
    SchoolNotice(
        notice_id=_save_notice(title, content, deadtime, token_data)
    ).insert()
    return success('发送成功')


def delete_notice(id, token_data):
    '[POST] /notice/<int:id>/delete'
    notice = Notice.query.get_or_error(id)
    auth_self(notice.sender, token_data, '权限不足: 不能删除其他人的通知')
    Notice.query.filter_by(id=id).delete()
    return success('删除成功')


def modify_notice(id, title, content, deadtime, token_data):
    '[POST] /notic/<int:id>/modify'
    notice = Notice.query.get_or_error(id)
    auth_self(notice.sender, token_data, '权限不足: 不能修改其他人的通知')
    try_parse_time(deadtime)
    notice.update(
        title=title,
        content=content,
        deadtime=deadtime
    )
    return success('修改成功')
