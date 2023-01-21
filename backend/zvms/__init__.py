from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from zvms.res import STATIC_FOLDER

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*", "*"})
app.static_folder = STATIC_FOLDER
app.config.from_pyfile('config.py')

app.test_request_context().push()
db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)

@app.errorhandler(404)
def handle_404(e):
    return {'type': 'ERROR', 'message': 'Not Found'}, 404

@app.errorhandler(500)
def handle_500(e):
    return {'type': 'ERROR', 'message': 'Internal Server Error'}, 500

import zvms.tokenlib as tk
import zvms.views

tk.init_app(app)
