from flask import Flask, render_template, url_for, current_app, g, request, redirect

app = Flask(__name__)

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
    return render_template("contact.html")

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # 이메일을 보낸다. 나중에 구현

        # contact 엔드포인트로 리다이렉트 함.
        return redirect(url_for("contact_complete"))
    
    return render_template("contact_complete.html")
