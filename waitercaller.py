from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask import Flask
from flask import render_template
from mockdbhelper import MockDBHelper as DBHelper
from passwordhelper import PasswordHelper
from bitlyhelper import BitlyHelper
from flask import redirect
from flask import url_for
from flask import request
from user import User
import config
import datetime
from forms import RegistrationForm
from forms import LoginForm

DB = DBHelper()
PH = PasswordHelper()
BH = BitlyHelper()


app = Flask(__name__)
app.secret_key = 'UjygY3+NNw5whdA0P5QDRxebfNnNldvFASpAlH4ygGka1y6DIM60ssdXTmRqIfO5lXk8kjZIkcuCXrcGCIkcecI5u+xiOK1jZkX'
login_manager = LoginManager(app)


@app.route("/")
def home():
	registrationform = RegistrationForm()
	return render_template("home.html", registrationform=registrationform, loginform=LoginForm())

@app.route("/account")
@login_required
def account():
	tables = DB.get_tables(current_user.get_id())
	return render_template("account.html", tables=tables)

@app.route("/login", methods=["POST"])
def login():
	form = LoginForm(request.form)
	if form.validate():
		stored_user = DB.get_user(form.email.data)
		if stored_user and PH.validate_password(form.password.data, stored_user['salt'], stored_user['hashed']):
			user = User(form.email.data)
			login_user(user)
			return redirect(url_for("account"))
		form.email.errors.append("Email or password invalid")
		return render_template("home.html", loginform=form, registrationform=RegistrationForm())
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
	requests = DB.get_requests(current_user.get_id())
	now = datetime.datetime.now()
	requests = DB.get_requests(current_user.get_id())
	for req in requests:
		deltaseconds = (now - req['time']).seconds
		req['wait_minutes'] = "{}.{}".format((deltaseconds/60),
			str(deltaseconds % 60).zfill(2))
	return render_template("dashboard.html", requests = requests)

@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
	table_name = request.form.get("tablenumber")
	tableid = DB.add_table(table_name, current_user.get_id())
	new_url = config.base_url + "newrequest/" + tableid
	short_url = BH.shorten_url(new_url)
	DB.update_table(tableid,short_url)
	return redirect(url_for("account"))

@app.route("/account/deletetable")
@login_required
def account_deletetable():
	table_id = request.args.get("tableid")
	DB.delete_table(table_id)
	return redirect(url_for("account"))

@app.route("/newrequest/<tid>")
def new_request(tid):
	DB.add_request(tid, datetime.datetime.now())
	return "Your request has been logged and your waiter will be with you shortly."

@app.route("/dashboard/resolve")
@login_required
def dashboard_resolve():
	request_id = request.args.get("request_id")
	DB.delete_request(request_id)
	return redirect(url_for("dashboard"))


@app.route("/register", methods=["POST"])
def register():
	form = RegistrationForm(request.form)
	if form.validate():
		if DB.get_user(form.email.data):
			form.email.errors.append("Email address already registered")
			return render_template('home.html', registrationform=form, loginform=LoginForm())
		salt = PH.get_salt()
		hashed = PH.get_hash(form.password2.data.encode('utf-8') + salt)
		DB.add_user(form.email.data, salt, hashed)
		return render_template("home.html", registrationform=form, loginform=LoginForm(), onloadmessage="Registration successful. Please log in.")
	return render_template("home.html", registrationform=form, loginform=LoginForm())

if __name__=='__main__':
	app.run()
