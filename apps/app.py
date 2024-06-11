from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# sqlalchemy를 인스턴스화 함
db = SQLAlchemy()


def create_app():
    # 플라스크 인스턴스 생성
    app = Flask(__name__)

    # 앱의 컨피그 설정을 함
    app.config.from_mapping(
        SECRET_KEY="2AZSMss3p5QPbcY2hBsJ",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATION=False,
        # sql 로그를 콘솔에 출력하도록 설정함.
        SQLALCHEMY_ECHO=True,
    )

    # sqlalchemy와 앱을 연계함
    db.init_app(app)

    # migrate와 앱을 연계함
    Migrate(app, db)

    # crud 앱으로 부터 views를 import한다.
    from apps.crud import views as crud_views

    # register_blueprints를 이용해서 views의 crud를 앱에 등록한다.
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app
