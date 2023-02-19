def create_app():
    from flask import Flask
    from flask_cors import CORS

    from zvms.res import STATIC_FOLDER

    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={r"/*", "*"})
    app.config.from_pyfile('config.py')
    app.static_folder = STATIC_FOLDER

    app.test_request_context().push()

    @app.errorhandler(404)
    def handle_404(e):
        return {'type': 'ERROR', 'message': 'Not Found'}, 404

    @app.errorhandler(500)
    def handle_500(e):
        return {'type': 'ERROR', 'message': 'Internal Server Error'}, 500

    import zvms.tokenlib as tk
    import zvms.views
    from zvms.apilib import Api
    from zvms.models import db

    tk.init_app(app)
    Api.init_app(app)
    db.init_app(app)