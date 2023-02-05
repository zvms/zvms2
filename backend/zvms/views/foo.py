from enum import IntEnum
from functools import wraps

from flask import Blueprint, request, render_template as _render_template, session, redirect
from sqlalchemy import Column, Integer, Text, desc

from zvms import db
from zvms.util import *
from zvms.models import *
from zvms.res import *

Foo = Blueprint('Foo', __name__)

TITLE = {
    1: ('初级粉丝', 'green'),
    5: ('中级粉丝', 'green'),
    15: ('高级粉丝', 'green'),
    30: ('正式会员', 'blue'),
    50: ('正式会员', 'blue'),
    100: ('核心会员', 'blue'),
    200: ('核心会员', 'blue'),
    500: ('铁杆会员', 'blue'),
    1000: ('铁杆会员', 'blue'),
    2000: ('知名人士', 'yellow'),
    3000: ('知名人士', 'yellow'),
    6000: ('人气楷模', 'yellow'),
    10000: ('人气楷模', 'yellow'),
    18000: ('意见领袖', 'yellow'),
    30000: ('意见领袖', 'yellow'),
    60000: ('进阶元老', 'yellow'),
    100000: ('资深元老', 'yellow'),
    300000: ('荣耀元老', 'yellow')
}

@Foo.app_template_filter('title')
def title(exp):
    print(exp)
    for k, v in TITLE.items():
        if k >= exp:
            print(k, v)
            return f'<h6 style="color: {v[1]}">{v[0]}</h6>'

class Attitude(IntEnum):
    NEUTUAL = 1
    LIKE = 2
    DISLIKE = 3
    FAVOURITE = 4

class Tie(ModelMixIn, db.Model):
    id = Column(Integer, primary_key=True, auto_increment=True)
    title = Column(Text)
    content = Column(Text)
    sender = Column(Integer)
    parent = Column(Integer)

    @property
    def seen(self):
        return UserTie.query.filter_by(tie_id=self.id).count()

    @property
    def likes(self):
        return (UserTie.query.filter(UserTie.tie_id == self.id, UserTie.attitude.in_(Attitude.LIKE, Attitude.FAVOURITE)).count() - 
            UserTie.query.filter_by(tie_id=self.id, attitude=Attitude.DISLIKE))

    @property
    def sender_name(self):
        return User.query.get(self.sender_id)

class UserTie(ModelMixIn, db.Model):
    user_id = Column(Integer, primary_key=True)
    tie_id = Column(Integer, primary_key=True)
    attitude = Column(Integer)

def render_template(template, **context):
    return _render_template(
        template,
        username=session['username'],
        userid=session['userid'],
        userexp=session['userexp'],
        usercls=session['usercls'],
        **context
    )

def loginrequired(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'userid' not in session:
            return redirect('/tieba/login', error='未登录')
        return func(*args, **kwargs)
    return wrapper

@Foo.route('/tieba/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user = User.query.filter_by(
                id=int(request.form.get('id')),
                pwd=md5ify(request.form.get('pwd'))
            ).first()
        except ValueError:
            return _render_template('login.html', error='用户名或密码错误')
        if user is None or user.auth & Categ.TEACHER or user.exp < 0:
            return _render_template('login.html', error='用户名或密码错误')
        session['username'] = user.name
        session['userid'] = user.id
        session['userexp'] = user.exp
        session['usercls'] = user.cls.name
        return redirect('/tieba/home')
    return _render_template('login.html')

@Foo.route('/tieba/logout')
@loginrequired
def logout():
    session.pop('userid')
    return redirect('/tieba/login')

@Foo.route('/tieba')
@Foo.route('/tieba/home')
@Foo.route('/tieba/home/<int:page>')
@loginrequired
def home(page=1):
    ties = Tie.query.filter_by(parent=None).order_by(desc(Tie.id)).paginate(page=page, per_page=10)
    return render_template(
        'home.html',
        enumerate=enumerate,
        total = ties.total,
        page=page,
        ties=select(ties, 'id', 'title', 'content', 'seen', 'likes', 'sender', 'sender_name')
    )

@Foo.route('/tieba/favourites')
@loginrequired
def favourites():
    return ''