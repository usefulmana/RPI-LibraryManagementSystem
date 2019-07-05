from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
app = Flask(__name__)

HOST = "35.198.230.96"
USER = "pi"
PASSWORD = "GATech321"
DATABASE = "piot_a2"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)