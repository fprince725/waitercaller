from flask import Flask

app = Flask(__name__)


@app.route("/")
def home(error_message=None):
	return "Under construction"

if __name__=='__main__':
	app.run()
