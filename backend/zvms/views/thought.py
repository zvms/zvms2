from base64 import b64decode
import datetime
import hashlib
import os.path

import requests

from zvms.models import *
from zvms.util import *
from zvms.res import *
from zvms.apilib import Api


@Api(rule='/thought/student/<int:id>', params='SearchStudentThoughts', response='SearchThoughtsResponse')
def list_student_thoughts(id: int, **kwargs):
    '''搜索学生感想'''

    conds=[StuVol.stu_id == id]
    try:
        if 'status' in kwargs:
            conds.append(StuVol.status == int(kwargs['status']))
    except ValueError:
        return error('传入的数据错误: 非法的URL参数')
    def process_query(query):
        return success('获取成功', list_or_error(query.select(
            'status',
            stuId='stu_id',
            volId='vol_id',
            stuName='stu_name',
            volName='vol_name',
            volTime=('vol_time', str)
        )))
    return process_query(StuVol.query.filter(*conds))


@Api(rule='/thought/search', params='SearchThoughts', response='SearchThoughtsResponse')
def search_thoughts(**kwargs):
    '''搜索感想'''
    conds = [StuVol.status != ThoughtStatus.WAITING_FOR_SIGNUP_AUDIT]
    def filter_(_): return True

    def filter_cls(sv):
        return User.query.get(sv.stu_id).cls_id == cls
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
        return error('传入的数据错误: 非法的URL参数')

    def process_query(query):
        return success('获取成功', list_or_error(query.select(
            'status',
            stuId='stu_id',
            volId='vol_id',
            stuName='stu_name',
            volName='vol_name',
            volTime='vol_time'
        )))
    return process_query(filter(lambda sv: filter_(sv) and sv.vol.status == VolStatus.AUDITED, StuVol.query.filter(*conds)))


@Api(rule='/thought/<int:volId>/<int:stuId>', response='ThoughtInfoResponse')
def get_thought_info(volId: int, stuId: int, token_data):
    '''获取一个感想的详细信息'''
    thought = StuVol.query.get_or_error((volId, stuId))
    if thought.status == ThoughtStatus.WAITING_FOR_SIGNUP_AUDIT:
        return error('未查询到相关数据')
    return success('获取成功', {k: v for k, v in thought.select(
        'status',
        'reason',
        'reward',
        'pics',
        'thought',
        everRepulsed = 'ever_repulsed'
    ).items() if v is not None})


def md5ify(raw: bytes):
    md5 = hashlib.md5()
    md5.update(raw)
    return md5.hexdigest()


def _save_thought(volId: int, stuId: int, thought: str, pictures, status):
    _thought = StuVol.query.get((volId, stuId))
    # if not _thought:
    #     StuVol(
    #         vol_id=volId,
    #         stu_id=stuId,
    #         status=status,
    #         thought=thought,
    #         reward=-1,
    #         reason='',
    #     ).insert()
    # else:
    match _thought.status:
        case ThoughtStatus.DRAFT:
            pass
        case ThoughtStatus.WAITING_FOR_SIGNUP_AUDIT:
            raise ZvmsError('该感想不可提交')
        case _:
            raise ZvmsError('不可重复提交')
    _thought.update(
        status=status,
        thought=thought
    )
    hashes = set()
    for pic in pictures:
        if 'hash' in pic:
            hash = pic['hash']
            exists = Picture.query.filter_by(vol_id = volId,stu_id =  stuId, hash = hash).count()>0
        else:
            hash = md5ify(pic['base64'].encode())
            exists = Picture.query.filter_by(vol_id = volId,stu_id =  stuId, hash = hash).count()>0
            if not exists:
                with open(os.path.join(STATIC_FOLDER, 'pics', f'{hash}.{pic["type"]}'), 'wb') as f:
                    f.write(b64decode(pic['base64']))
        if not exists:
            Picture(
                vol_id=volId,
                stu_id=stuId,
                hash=hash,
                extension=pic['type']
            ).insert()
        hashes.add(hash)
    Picture.query.filter_by(stu_id=stuId, vol_id=volId).filter(Picture.hash.not_in(hashes)).delete()



def _auth_thought(stuId: int, operation: str, token_data):
    if (Categ.TEACHER | Categ.CLASS) & token_data['auth']:
        auth_cls(User.query.get_or_error(stuId).cls_id, token_data, f'权限不足: 不能{operation}其他班级的感想')
        return True
    else:
        auth_self(stuId, token_data, f'权限不足: 不能{operation}其他人的感想')
        return False
    

@Api(rule='/thought/<int:volId>/<int:stuId>/save', method='POST', params='Thought')
def save_thought(token_data, volId: int, stuId: int, thought: str, pictures):
    '''保存感想草稿'''
    _auth_thought(stuId, '修改', token_data)
    _save_thought(volId, stuId, thought, pictures, ThoughtStatus.DRAFT)
    return success('保存成功')


@Api(rule='/thought/<int:volId>/<int:stuId>/submit', method='POST', params='Thought')
def submit_thought(token_data, volId: int, stuId: int, thought: int, pictures):
    '''提交感想'''
    is_common = not _auth_thought(stuId, '提交', token_data)
    # 临时由WAITING_FOR_FIRST_AUDIT修改为WAITING_FOR_FINAL_AUDIT
    _save_thought(volId, stuId, thought, pictures, ThoughtStatus.WAITING_FOR_FINAL_AUDIT if is_common else ThoughtStatus.WAITING_FOR_FINAL_AUDIT)
    return success('提交成功')


@Api(rule='/thought/<int:volId>/<int:stuId>/audit/first', method='POST', auth=Categ.CLASS | Categ.TEACHER)
def first_audit(token_data, volId: int, stuId: int):
    '''初审感想(班内)'''
    auth_cls(User.query.get(stuId), token_data)
    thought = StuVol.query.get((volId, stuId))
    if thought.status != ThoughtStatus.WAITING_FOR_FIRST_AUDIT:
        return error('该感想不可初审')
    thought.update(
        status=ThoughtStatus.WAITING_FOR_FINAL_AUDIT
    )
    UserNotice(
        user_id=thought.stu_id,
        notice_id=Notice(
            title='感想终审',
            content=f'您在义工{thought.vol.name}提交的感想已通过团支书审核, 请等待审计部审核后发放时长',
            sendtime=datetime.datetime.now(),
            deadtime=datetime.datetime.now() + datetime.timedelta(days=10),
            sender=0
        ).insert().id
    ).insert()
    return success('审核成功')


@Api(rule='/thought/<int:volId>/<int:stuId>/audit/final', method='POST', auth=Categ.AUDITOR, params='Accept')
def final_audit(token_data, reward: int, volId: int, stuId: int):
    '''终审感想(义管会)'''
    thought = StuVol.query.get((volId, stuId))
    if thought.status != ThoughtStatus.WAITING_FOR_FINAL_AUDIT:
        return error('该感想不可终审')
    thought.update(
        reward=reward,
        status=ThoughtStatus.ACCEPTED,
        reason='',
        ever_repulsed = False
    )
    UserNotice(
        user_id=thought.stu_id,
        notice_id=Notice(
            title='感想终审',
            content=f'您在义工{thought.vol.name}提交的感想已通过审计部审核, 获得{reward}分钟义工时间',
            sendtime=datetime.datetime.now(),
            deadtime=datetime.datetime.now() + datetime.timedelta(days=10),
            sender=0
        ).insert().id
    ).insert()
    return success('审核成功')


@Api(rule='/thought/<int:volId>/<int:stuId>/repulse', method='POST', params='Repulse')
def repulse_thought(token_data, volId: int, stuId: int, reason: str):
    '''打回感想'''
    auth_cls(User.query.get(stuId), token_data)
    thought = StuVol.query.get_or_error((volId, stuId))
    if thought.status not in (ThoughtStatus.WAITING_FOR_FINAL_AUDIT, ThoughtStatus.WAITING_FOR_FIRST_AUDIT):
        return error('该感想不可打回')
    thought.update(
        status=ThoughtStatus.DRAFT,
        reason=reason,
        ever_repulsed=True
    )
    UserNotice(
        user_id=thought.stu_id,
        notice_id=Notice(
            title='感想终审',
            content=f'您在义工{thought.vol.name}提交的感想已被审计部打回, 可以在义工列表中点击该义工, 修改感想后重新提交',
            sendtime=datetime.datetime.now(),
            deadtime=datetime.datetime.now() + datetime.timedelta(days=10),
            sender=0
        ).insert().id
    ).insert()
    return success('打回成功')


@Api(rule='/thought/<int:volId>/<int:stuId>/fetch-picture', method='POST', params='FetchPicture', response='PictureResponse')
def fetch_picture(token_data, volId: int, stuId: int, url: str):
    '''拉取感想图片'''
    try:
        pic_data = requests.get(url).content
        pic_type = url.split('.')[-1]
        hash = md5ify(pic_data)
        if Picture.query.filter_by(stu_id=stuId, vol_id=volId,hash=hash).count()==0:
            with open(os.path.join(STATIC_FOLDER, 'pics', f'{hash}.{pic_type}'), 'wb') as f:
                f.write(pic_data)
            Picture(
                vol_id=volId,
                stu_id=stuId,
                hash=hash,
                extension=pic_type
            ).insert()
        return success('图片上传成功', {
            'hash': hash,
            'type': pic_type
        })
    except requests.exceptions.RequestException:
        return error('图片上传失败')
