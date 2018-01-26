from flask_login import LoginManager
from flask_login import login_required
from flask import Flask
from flask import render_template

app = Flask(__name__)
login_manager = LoginManager(app)


@app.route("/")
def home():
	return render_template("home.html")

@app.route("/account")
@login_required
def account():
	return "logged in"

if __name__=='__main__':
	app.run()
