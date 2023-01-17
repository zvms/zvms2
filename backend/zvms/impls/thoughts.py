from base64 import b64decode
import sys
import hashlib

from zvms.models import *
from zvms.util import *
from zvms.res import *


def search_thoughts(**kwargs):
    '[GET] /thoughts'
    conds = [StuVol.status != Status.WAITING_FOR_SIGNUP_AUDIT]
    def filter_(_): return True

    def filter_cls(sv):
        return User.query.get(sv.stu_id).cls_id == c

    def filter_status(sv):
        return Volunteer.query.get(sv.vol_id).status == S
    try:
        if 'c' in kwargs:
            c = int(kwargs['c'])
            if 'S' in kwargs:
                S = int(kwargs['S'])
                def filter_(sv): return filter_cls(sv) and filter_status(sv)
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
        return error(400, '请求接口错误: 非法的URL参数')

    def process_query(query):
        return success('获取成功', list_or_error(select(query, 'status', stu_id='stuId', vol_id='volId', stu_name='stuName', vol_name='volName')))
    return process_query(filter(filter_, StuVol.query.filter(*conds)))


def get_thought_info(stuId, volId, token_data):
    '[GET] /thoughts/<int:stuId>/<int:volId>'
    thought = StuVol.query.get_or_error((stuId, volId))
    if thought.status == Status.WAITING_FOR_SIGNUP_AUDIT:
        return error(404, '未查询到相关数据')
    ret = {}
    if thought.reason is not None:
        ret['reason'] = thought.reason
    if thought.reward is not None:
        ret['reward'] = thought.reward
    if thought.pics is not None and thought.thought is not None:
        ret['pics'] = thought.pics
        ret['thought'] = thought.thought
    return success('获取成功', ret)


def update_thought(token_data, stuId, volId, **kwargs):
    '[PATCH] /thoughts/<int:stuId>/<int:volId>'

    Thought = Object(
        thought=String,
        pics=Array(String)
    )

    def md5ify(raw):
        md5 = hashlib.md5()
        md5.update(raw.encode())
        return md5.hexdigest()

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
            case Status.UNSUBMITTED:
                if 'reason' not in kwargs or not isinstance(kwargs['reason'], str):
                    return error(400, '请求接口错误: "reason"参数')
                if not Categ.AUDITOR.authorized(auth):
                    return error(403, '权限不足')
                thought.update(
                    reason=kwargs['reason'], status=Status.UNSUBMITTED)
            case Status.WAITING_FOR_FIRST_AUDIT:
                if (Categ.TEACHER | Categ.CLASS).authorized(auth):
                    auth_cls(User.query.get(stuId), token_data)
                    thought.status = Status.WAITING_FOR_FINAL_AUDIT
                else:
                    auth_self(stuId, token_data, '不能提交其他人的感想')
                    thought.status = Status.WAITING_FOR_FIRST_AUDIT
                submit_thought()
            case Status.ACCEPTED | Status.REJECTED:
                if not Categ.AUDITOR.authorized(auth):
                    return error(403, '权限不足')
                thought.status = kwargs['status']
            case Status.WAITING_FOR_FINAL_AUDIT:
                if not (Categ.TEACHER | Categ.CLASS).authorized(auth):
                    return error(403, '权限不足')
                thought.status = kwargs['status']
            case _:
                return error(400, '请求接口错误: 无效的感想状态')
        return success('审核成功')
    else:
        auth_self(thought.stu_id, token_data, '不能修改其他人的感想')
        submit_thought()
