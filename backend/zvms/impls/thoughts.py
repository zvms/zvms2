from base64 import b64decode
import sys
import hashlib

from zvms.models import *
from zvms.util import *
from zvms.res import *

def md5ify(raw):
    md5 = hashlib.md5()
    md5.update(raw.encode())
    return md5.hexdigest()

#[GET] /thoughts
def search_thoughts(**kwargs):
    conds = [StuVol.status != STATUS.WAITING_FOR_SIGNUP_AUDIT]
    filter_ = lambda _: True
    try:
        if 'c' in kwargs:
            c = int(kwargs['c'])
            if 'S' in kwargs:
                S = int(kwargs['S'])
                filter_ = lambda sv: filter_cls(sv) and filter_status(sv)
            else:
                filter_ = filter_cls
        if 'S' in kwargs:
            S = int(kwargs['S'])
            filter_ = filter_status()
        if 's' in kwargs:
            conds.append(StuVol.stu_id == int(kwargs['s']))
        if 'v' in kwargs:
            conds.append(StuVol.vol_id == int(kwargs['v']))
    except ValueError:
        return error('请求接口错误: 非法的URL参数')
    def filter_cls(sv):
        return User.query.get(sv.stu_id).cls_id == c
    def filter_status(sv):
        return Volunteer.query.get(sv.vol_id).status == S
    def process_query(query):
        ret = list(apply(select)(query, 'status', stu_id='stuId', vol_id='volId',
                                 stu_name='stuName', vol_name='volName'))
        print(ret)
        if not ret:
            return error('未查询到相关数据')
        return success('获取成功', ret)
    return process_query(filter(filter_, StuVol.query.filter(*conds)))

#[GET] /thoughts/<int:stuId>/<int:volId>
def get_thought_info(stuId, volId, token_data):
    thought = StuVol.query.get_or_error((stuId, volId))
    if thought.status == STATUS.WAITING_FOR_SIGNUP_AUDIT:
        return error('未查询到相关数据')
    ret = {}
    if thought.reason is not None:
        ret['reason'] = thought.reason
    if thought.reward is not None:
        ret['reward'] = thought.reward
    if thought.pics is not None and thought.thought is not None:
        ret['pics'] = thought.pics
        ret['thought'] = thought.thought
    return success('获取成功', ret)

Thought = Object(
    thought=String,
    pics=Array(String)
)

#[PATCH] /thoughts/<int:stuId>/<int:volId>
def update_thought(token_data, stuId, volId, **kwargs):
    thought = StuVol.query.get_or_error((stuId, volId))
    auth = token_data['auth']
    def submit_thought():
        if not Thought(kwargs):
            return interface_error(Thought, kwargs)
        thought.thought = kwargs['thought']
        if sys.platform == 'win32':
            statis_folder = 'C:\zvms_backend'
        elif sys.platform == 'linux':
            statis_folder = '/tmp/zvms_backend'
        for pic in kwargs['pics']:
            pic = b64decode(pic)
            hash = md5ify(pic)
            if Picture.query.filter_by(stu_id=stuId, vol_id=volId, hash=hash).first():
                continue
            with open(f'{statis_folder}/pics/{hash}.jpg') as f:
                f.write(pic)
            Picture(
                stu_id=kwargs['stu_id'],
                vol_id=kwargs['vol_id'],
                hash=hash
            ).insert()
        return success('提交成功')
    if 'status' in kwargs:
        match kwargs['status']:
            case STATUS.UNSUBMITTED:
                if 'reason' not in kwargs or not isinstance(kwargs['reason'], str):
                    return error('请求接口错误: "reason"参数')
                if not AUTH.AUDITOR.authorized(auth):
                    return error('权限不足')
                thought.update(reason=kwargs['reason'], status=STATUS.UNSUBMITTED)
            case STATUS.WAITING_FOR_FIRST_AUDIT:
                if (AUTH.TEACHER | AUTH.CLASS).authorized(auth):
                    auth_cls(User.query.get(stuId), token_data)
                    thought.status = STATUS.WAITING_FOR_FINAL_AUDIT
                else:
                    auth_self(stuId, token_data, '不能提交其他人的感想')
                    thought.status = STATUS.WAITING_FOR_FIRST_AUDIT
                submit_thought()
            case STATUS.ACCEPTED | STATUS.REJECTED:
                if not AUTH.AUDITOR.authorized(auth):
                    return error('权限不足')
                thought.status = kwargs['status']
            case STATUS.WAITING_FOR_FINAL_AUDIT:
                if not (AUTH.TEACHER | AUTH.CLASS).authorized(auth):
                    return error('权限不足')
                thought.status = kwargs['status']
            case _:
                return error('请求接口错误: 无效的感想状态')
        return success('审核成功')
    else:
        auth_self(thought.stu_id, token_data, '不能修改其他人的感想')
        submit_thought()