from flask import Flask


def create_app():
    # 플라스크 인스턴스 생성
    app = Flask(__name__)

    # crud 앱으로 부터 views를 import한다.
    from apps.crud import views as crud_views

    # register_blueprints를 이용해서 views의 crud를 앱에 등록한다.
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app
