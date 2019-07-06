from app import db, ma, app, cross_origin, request, jsonify
from datetime import datetime, timedelta
from config_parser import Parser
import json


class BorrowedBooks(db.Model):
    __tablename__ = "borrowed_books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Enum('borrowed', 'returned'))
    borrow_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    user_return_date = db.Column(db.Date)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, book_id, user_id, borrow_date, return_date, user_return_date, status):
        self.status = status
        self.book_id = book_id
        self.user_id = user_id
        self.borrow_date = borrow_date
        self.user_return_date = user_return_date
        self.return_date = return_date


class BorrowedBooksSchema(ma.Schema):
    class Meta:
        fields = ('id', 'book_id', 'user_id', 'borrow_date', 'return_date', 'user_return_date', 'status')


borrowed_book_schema = BorrowedBooksSchema()
borrowed_books_schema = BorrowedBooksSchema(many=True)


def days_to_return_book(borrow_date):
    with open('config.json') as file:
        data = json.load(file)
    return borrow_date + timedelta(days=Parser.get_instance().days_to_return)


@app.route('/borrow/<book_id>/user/<user_id>', methods=['POST'])
@cross_origin()
def borrow_book(book_id, user_id):
    status = "borrowed"
    borrow_date = datetime.now()
    return_date = days_to_return_book(borrow_date)
    user_return_date = None
    borrow = BorrowedBooks(book_id, user_id, borrow_date, return_date, user_return_date, status)
    db.session.add(borrow)
    db.session.commit()

    return borrowed_book_schema.jsonify(borrow)


@app.route('/return/<borrow_id>', methods=['PUT'])
@cross_origin()
def return_book(borrow_id):
    borrow = BorrowedBooks.query.get(borrow_id)
    borrow.status = "returned"
    borrow.user_return_date = datetime.now()
    db.session.commit()

    return borrowed_book_schema.jsonify(borrow)


@app.route('/borrow/user/<user_id>', methods=['GET'])
@cross_origin()
def get_all_undue_borrow_of_a_user(user_id):
    borrow = BorrowedBooks.query.filter(BorrowedBooks.status == 'borrowed').filter(
        BorrowedBooks.user_id == user_id).all()
    result = borrowed_books_schema.dump(borrow)

    return jsonify(result)


@app.route('/borrow/user/<user_id>/all', methods=['GET'])
@cross_origin()
def get_borrow_history_of_a_user(user_id):
    borrow = BorrowedBooks.query.filter(BorrowedBooks.user_id == user_id).all()
    result = borrowed_books_schema.dump(borrow)

    return jsonify(result)
