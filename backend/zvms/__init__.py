from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

import sys

app = Flask(__name__)
with open('app.cfg') as f:
    app.config['SQLALCHEMY_DATABASE_URI'], \
    app.config['SECRET_KEY'] = map(lambda s: s[:-1], f)
CORS(app, supports_credentials=True, resources={r"/*", "*"})
if sys.platform == 'win32':
    app.static_folder = 'C:\zcvms-backend'
elif sys.platform == 'linux':
    app.static_folder = '/tmp/zvms-backend'

app.test_request_context().push()
db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)

import zvms.views
from zvms.tokenlib import init_app

init_app(app)