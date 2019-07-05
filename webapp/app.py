from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config.from_pyfile('config.py')
cors = CORS(app)
ma = Marshmallow()
db = SQLAlchemy(app)
from book_routes import *
from user_routes import *

if __name__ == '__main__':
    db.create_all()
    app.run()


#
#
# class BorrowedBooks(db.Model):
#     __tablename__ = "borrowed_books"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     status = db.Column(db.Enum('borrowed', 'returned'))
#     borrow_date = db.Column(db.Date)
#     return_date = db.Column(db.Date)
#     book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#
#
# class BorrowedBooksSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'status', 'borrow_date', 'return_date', 'book_id', 'user_id')



