import logging
import os
from email_validator import validate_email, EmailNotValidError
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message
from flask import (
    Flask,
    render_template,
    url_for,
    # current_app,
    # g,
    request,
    redirect,
    flash,
    make_response,
    session,
)

app = Flask(__name__)

app.config["SECRET_KEY"] = "1234qwer"

app.logger.setLevel(logging.DEBUG)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

toolbar = DebugToolbarExtension(app)
mail = Mail(app)


@app.route("/")
def index():
    return "Hello Flaskbook!"


@app.route("/hello")
def hello():
    return "Hello World!!!"


@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)


# with app.test_request_context():
#     print(url_for("index"))
#     print(url_for("hello"))
#     print(url_for("show_name", name="AK", page=1))


@app.route("/contact")
def contact():
    # 응답객체를 취득한다.
    response = make_response(render_template("contact.html"))
    # 쿠키를 설정한다.
    response.set_cookie("flaskbook key", "flaskbook value")
    # 세션을 설정한다.
    session["username"] = "AK"
    return response


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # form의 속성을 활용해 폼의 값을 취득한다.
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["decription"]

        # 입력체크
        is_valid = True

        if not username:
            flash("사용자명은 필수 입니다.")
            is_valid = False

        if not email:
            flash("이메일 주소는 필수입니다.")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("이메일 주소의 형식으로 입력해 주세요")
            is_valid = False

        if not description:
            flash("문의 내용은 필수 입니다.")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        # 이메일을 보낸다. 나중에 구현
        send_email(
            email,
            "문의 감사드립니다.",
            "contact_mail",
            username=username,
            description=description,
        )

        # contact 엔드포인트로 리다이렉트 함.
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")


def send_email(to, subject, template, **kwargs):
    # 메일을 송신하는 함수
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
