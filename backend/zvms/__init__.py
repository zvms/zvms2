def create_app():
    import traceback

    from flask import Flask
    from flask_cors import CORS

    from zvms.res import STATIC_FOLDER
    from zvms.models import Report

    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={r"/*", "*"}, max_age=600)
    app.config.from_pyfile('config.py')
    app.static_folder = STATIC_FOLDER

    app.test_request_context().push()

    @app.errorhandler(404)
    def handle_404(e):
        return {'type': 'ERROR', 'message': '请求地址错误'}, 404

    @app.errorhandler(500)
    def handle_500(e):
        return {'type': 'ERROR', 'message': '服务器内部错误'}, 500

    import zvms.tokenlib as tk
    import zvms.views
    import zvms.views.notice
    from zvms.apilib import Api
    from zvms.models import db

    zvms.views.notice.load_public_notice()

    tk.init_app(app)
    Api.init_app(app)
    db.init_app(app)

    return app