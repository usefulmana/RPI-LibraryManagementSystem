from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for, g


app = Flask(__name__)
app.config.from_pyfile('config.py')
cors = CORS(app)
ma = Marshmallow()
db = SQLAlchemy(app)
from book_routes import *
from user_routes import *
from borrowed_books_routes import *
from app_routes import *

"""
Where the Flask REST API congregates, all the configs and routes are imported here.
"""
if __name__ == '__main__':
    db.create_all()
    app.run()







