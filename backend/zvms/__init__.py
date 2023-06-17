from zvms.apilib import ZvmsExit

def create_app():
    import json

    from flask import Flask, request
    from flask_cors import CORS

    from zvms.res import STATIC_FOLDER
    from zvms.models import Report, User

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
    
    @app.route('/user/from-ip/<ip>')
    def from_ip(ip):
        return json.dumps(zvms.views.user.ips.get(ip))

    import zvms.tokenlib as tk
    import zvms.views
    import zvms.views.notice
    import zvms.views.system
    import zvms.views.user
    from zvms.apilib import Api
    from zvms.models import db

    zvms.views.notice.load_public_notice()

    tk.init_app(app)
    Api.init_app(app)
    db.init_app(app)

    return app