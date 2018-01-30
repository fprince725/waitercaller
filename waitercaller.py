from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask import Flask
from flask import render_template
from mockdbhelper import MockDBHelper as DBHelper
from passwordhelper import PasswordHelper
from flask import redirect
from flask import url_for
from flask import request
from user import User
import config

DB = DBHelper()
PH = PasswordHelper()


app = Flask(__name__)
app.secret_key = 'UjygY3+NNw5whdA0P5QDRxebfNnNldvFASpAlH4ygGka1y6DIM60ssdXTmRqIfO5lXk8kjZIkcuCXrcGCIkcecI5u+xiOK1jZkX'
login_manager = LoginManager(app)


@app.route("/")
def home():
	return render_template("home.html")

@app.route("/account")
@login_required
def account():
	tables = DB.get_tables(current_user.get_id())
	return render_template("account.html", tables=tables)

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
	return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
	return render_template("dashboard.html")

@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
	table_name = request.form.get("tablenumber")
	tableid = DB.add_table(table_name, current_user.get_id())
	new_url = config.base_url + "newrequest/" + tableid
	DB.update_table(tableid,new_url)
	return redirect(url_for("account"))

@app.route("/account/deletetable")
@login_required
def account_deletetable():
	table_id = request.args.get("tableid")
	DB.delete_table(table_id)
	return redirect(url_for("account"))

if __name__=='__main__':
	app.run()
