from base64 import b64decode
import sys
import hashlib
import os.path

from zvms.models import *
from zvms.util import *
from zvms.res import *
from zvms.apilib import api


@api(rule='/thought/search', params='SearchThoughts')
def search_thoughts(**kwargs):
    conds = [StuVol.status != ThoughtStatus.WAITING_FOR_SIGNUP_AUDIT]
    def filter_(_): return True

    def filter_cls(sv):
        return User.query.get(sv.stu_id).cls_id == filter_cls
    try:
        if 'cls' in kwargs:
            cls = int(kwargs['cls'])
            filter_ = filter_cls
        if 'status' in kwargs:
            conds.append(StuVol.status == int(kwargs['status']))
        if 'student' in kwargs:
            conds.append(StuVol.stu_id == int(kwargs['student']))
        if 'volunteer' in kwargs:
            conds.append(StuVol.vol_id == int(kwargs['volunteer']))
    except ValueError:
        return error('请求接口错误: 非法的URL参数')

    def process_query(query):
        return success('获取成功', list_or_error(select(query, 'status', stu_id='stuId', vol_id='volId', stu_name='stuName', vol_name='volName')))
    return process_query(filter(filter_, StuVol.query.filter(*conds)))


@api(rule='/thought/<int:volId>/<int:stuId>')
def get_thought_info(volId, stuId, token_data):
    thought = StuVol.query.get_or_error((volId, stuId))
    if thought.status == ThoughtStatus.WAITING_FOR_SIGNUP_AUDIT:
        return error('未查询到相关数据')
    ret = {}
    if thought.reason is not None:
        ret['reason'] = thought.reason
    if thought.reward is not None:
        ret['reward'] = thought.reward
    if thought.thought is not None:
        ret['pics'] = list(thought.pics)
        ret['thought'] = thought.thought
    return success('获取成功', ret)


def md5ify(raw):
    md5 = hashlib.md5()
    md5.update(raw.encode())
    return md5.hexdigest()


def _submit_thought(volId, stuId, thought, pictures, status):
    _thought = StuVol.query.get((volId, stuId))
    if not _thought:
        StuVol(
            vol_id=volId,
            stu_id=stuId,
            status=status,
            thought=thought
        ).insert()
    else:
        match _thought.status:
            case ThoughtStatus.UNSUBMITTED | ThoughtStatus.DRAFT:
                pass
            case ThoughtStatus.WAITING_FOR_SIGNUP_AUDIT:
                raise ZvmsError('该感想不可提交')
            case _:
                raise ZvmsError('不可重复提交')
        _thought.update(
            status=status,
            thought=thought
        )
    hashes = list(map(md5ify, pictures))
    Picture.query.filter_by(stu_id=stuId, vol_id=volId).filter(Picture.hash.in_(hashes)).delete()
    for i, pic in enumerate(pictures):
        if not Picture.query.get((volId, stuId, hashes[i])):
            with open(os.path.join(STATIC_FOLDER, 'pics', f'{hashes[i]}.jpg'), 'wb') as f:
                f.write(b64decode(pic))
            Picture(
                vol_id=volId,
                stu_id=stuId,
                hash=hashes[i]
            ).insert()


def _auth_thought(stuId, operation, token_data):
    if (Categ.TEACHER | Categ.CLASS) & token_data['auth']:
        auth_cls(User.query.get_or_error(stuId), token_data, f'权限不足: 不能{operation}其他班级的感想')
        return True
    else:
        auth_self(stuId, token_data, f'权限不足: 不能{operation}其他人的感想')
        return False
    

@api(rule='/thought/<int:volId>/<int:stuId>/save', method='POST', params='Thought')
def save_thought(token_data, volId, stuId, thought, pictures):
    '[POST] /thought/<int:volId>/<int:stuId>/save'
    _auth_thought(stuId, '修改', token_data)
    _submit_thought(volId, stuId, thought, pictures, ThoughtStatus.DRAFT)
    return success('保存成功')


@api(rule='/thought/<int:volId>/<int:stuId>/submit', method='POST', params='Thought')
def submit_thought(token_data, volId, stuId, thought, pictures):
    is_common = not _auth_thought(stuId, '提交', token_data)
    _submit_thought(volId, stuId, thought, pictures, ThoughtStatus.WAITING_FOR_FIRST_AUDIT if is_common else ThoughtStatus.WAITING_FOR_FINAL_AUDIT)
    return success('提交成功')


@api(rule='/thought/<int:volId>/<int:stuId>/audit/first', method='POST', auth=Categ.CLASS | Categ.TEACHER)
def first_audit(token_data, volId, stuId):
    auth_cls(User.query.get(stuId), token_data)
    thought = StuVol.query.get((volId, stuId))
    if thought.status != ThoughtStatus.WAITING_FOR_FIRST_AUDIT:
        return error('该感想不可初审')
    thought.update(
        status=ThoughtStatus.WAITING_FOR_FINAL_AUDIT
    )
    return success('审核成功')


@api(rule='/thought/<int:volId>/<int:stuId>/audit/final', method='POST', auth=Categ.AUDITOR)
def final_audit(token_data, volId, stuId):
    thought = StuVol.query.get((volId, stuId))
    if thought.status != ThoughtStatus.WAITING_FOR_FINAL_AUDIT:
        return error('该感想不可终审')
    thought.update(
        status=ThoughtStatus.ACCEPTED
    )
    return success('审核成功')


@api(rule='/thought/<int:volId>/<int:stuId>/repulse', method='POST', params='Repulse')
def repulse(token_data, volId, stuId, reason):
    '[POST] /thought/<int:volId>/<int:stuId>/audit/repulse'
    auth_cls(User.query.get(stuId), token_data)
    thought = StuVol.query.get_or_error((volId, stuId))
    if thought.status not in (ThoughtStatus.WAITING_FOR_FINAL_AUDIT, ThoughtStatus.WAITING_FOR_FIRST_AUDIT):
        return error('该感想不可打回')
    thought.update(
        status=ThoughtStatus.UNSUBMITTED,
        reason=reason
    )
    return success('打回成功')