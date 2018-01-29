from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask import Flask
from flask import render_template
from mockdbhelper import MockDBHelper as DBHelper
from passwordhelper import PasswordHelper
from flask import redirect
from flask import url_for
from flask import request
from user import User

DB = DBHelper()
PH = PasswordHelper()


app = Flask(__name__)
app.secret_key = 'UjygY3+NNw5whdA0P5QDRxebfNnNldvFASpAlH4ygGka1y6DIM60ssdXTmRqIfO5lXk8kjZIkcuCXrcGCIkcecI5u+xiOK1jZkX'
login_manager = LoginManager(app)


@app.route("/")
def home():
	return render_template("home_1.html")

@app.route("/account")
@login_required
def account():
	return render_template("account.html")

@app.route("/login", methods=["POST"])
def login():
	email = request.form.get("email")
	password = request.form.get("password")
	stored_user = DB.get_user(email)
	if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
		user = User(email)
		login_user(user)
		return redirect(url_for("account"))
	return home()

@login_manager.user_loader
def load_user(user_id):
	user_password = DB.get_user(user_id)
	if user_password:
		return User(user_id)	

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home_1"))

@app.route("/dashboard")
@login_required
def dashboard():
	return render_template("dashboard.html")

if __name__=='__main__':
	app.run()
