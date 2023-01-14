import zvms.views
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from zvms.res import STATIC_FOLDER
from zvms.tokenlib import init_app

app = Flask(__name__)
with open('app.cfg') as f:
    app.config['SQLALCHEMY_DATABASE_URI'], \
        app.config['SECRET_KEY'] = map(lambda s: s[:-1], f)
CORS(app, supports_credentials=True, resources={r"/*", "*"})
app.static_folder = STATIC_FOLDER

app.test_request_context().push()
db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)


init_app(app)
