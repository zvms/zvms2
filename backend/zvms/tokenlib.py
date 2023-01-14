from zvms import db
from zvms.models import Log
import jwt

key: str


def init_app(app):
    global key
    key = app.config['SECRET_KEY']


def exists(data):
    return Log.query.get(int(data['logid']))


def remove(token):
    Log.query.filter_by(id=token['logid']).delete()
    db.session.commit()


def generate(**data):
    log = Log().insert()
    db.session.commit()
    return jwt.encode(data | {'logid': log.id}, key=key)


def read(token):
    return jwt.decode(token.encode(), key=key, algorithms='HS256')
