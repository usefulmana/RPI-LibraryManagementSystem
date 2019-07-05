from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
from flask import Flask, request
import datetime

app = Flask(__name__)
cors = CORS(app)
ma = Marshmallow()
HOST = "35.198.230.96"
USER = "pi"
PASSWORD = "GAtech321"
DATABASE = "piot_a2"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    published_date = db.Column(db.Date)
    # borrowed_books = db.relationship('BorrowedBooks', backref='book_id')

    def __init__(self, title, author, published_date):
        self.title = title
        self.author = author
        self.published_date = published_date


class BookSchema(ma.Schema):
    class Meta:
        fields = ("book_id", "title", "author", "published_date")


book_Schema = BookSchema()
books_Schema = BookSchema(many=True)


@app.route('/books', methods=['POST'])
@cross_origin()
def add_book():
    title = request.json['title']
    author = request.json['author']
    new_book = Book(title, author, datetime.datetime.now())
    db.session.add(new_book)
    db.session.commit()

    return book_Schema.jsonify(new_book)


@app.route('/books/<id>', method=['DELETE'])
@cross_origin()
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)



    db.session.commit()

    return book_Schema.jsonify(book)

db.create_all()
app.run(debug=True)
# class Users(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_email = db.Column(db.String(255), unique=True)
#     name = db.Column(db.Text)
#     books_borrowed = db.relationship('BorrowedBooks', backref='user_id')
#
#     def __init__(self, user_id, email, name):
#         self.id = user_id
#         self.user_email = email
#         self.name = name
#
#
# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ('user_id', "user_email", "name")
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



