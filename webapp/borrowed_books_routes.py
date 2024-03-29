from app import db, ma, app, cross_origin, request, jsonify
from datetime import datetime, timedelta
from config_parser import Parser
import book_routes
import json


class BorrowedBooks(db.Model):
    __tablename__ = "borrowed_books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    borrow_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    borrow_status = db.Column(db.Text)
    return_status = db.Column(db.Text)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Text)

    def __init__(self, book_id, user_id, borrow_date, due_date, return_date, borrow_status, return_status, event_id):
        self.book_id = book_id
        self.user_id = user_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = return_date
        self.borrow_status = borrow_status
        self.return_status = return_status
        self.event_id = event_id


class BorrowedBooksSchema(ma.Schema):
    class Meta:
        fields = ('id', 'book_id', 'user_id', 'borrow_date', 'due_date', 'return_date', 'borrow_status', 'return_status'
                  , 'event_id')


borrowed_book_schema = BorrowedBooksSchema()
borrowed_books_schema = BorrowedBooksSchema(many=True)


def days_to_return_book(borrow_date):
    """
    A mini JSON parser to extract how many days should a borrowed book be returned
    :param borrow_date: the date in which the book is borrowed
    :return: a new date with added days
    """
    with open('config.json') as file:
        data = json.load(file)
    return borrow_date + timedelta(days=Parser.get_instance().days_to_return)


@app.route('/borrow/<book_id>/user/<user_id>', methods=['POST'])
@cross_origin()
def borrow_book(book_id, user_id):
    """
    Use this route to execute a borrow_a_book transaction
    :param book_id: target book's id
    :param user_id: target user's id
    :param event_id: google calendar
    :return: a JSON containing transaction's information
    """
    borrowed_book = book_routes.Book.query.get(book_id)
    borrow_history = BorrowedBooks.query.filter(BorrowedBooks.book_id == book_id, BorrowedBooks.user_id == user_id,
                                                BorrowedBooks.return_status == None).first()
    if borrowed_book.quantity <= 0:
        return jsonify({"message": "Out of stock"}), 400
    elif borrow_history is not None:
        return jsonify({"message": "Current user has already borrowed this book and has not returned it!"}), 400
    else:
        borrow_date = datetime.now()
        due_date = days_to_return_book(borrow_date)
        borrow_status = "borrowed"
        return_status = None
        return_date = None
        event_id = None
        borrowed_book.quantity -= 1
        # Create a new row
        borrow = BorrowedBooks(book_id, user_id, borrow_date, due_date, return_date, borrow_status, return_status,
                               event_id)
        db.session.add(borrow)
        db.session.commit()
        return borrowed_book_schema.jsonify(borrow)


@app.route('/borrow/<borrow_id>/event/<event_id>', methods=['PUT'])
@cross_origin()
def put_event_id_into_borrow_information(borrow_id, event_id):
    borrow = BorrowedBooks.query.get(borrow_id)
    if borrow is None:
        return jsonify({"message": "ID does not exists!"})
    else:
        borrow.event_id = event_id
        db.session.commit()

        return borrowed_book_schema.jsonify()


@app.route('/return/<borrow_id>', methods=['PUT'])
@cross_origin()
def return_book(borrow_id):
    """
    use this route when user want to return the book
    :param borrow_id: target borrow_a_book's id
    :return: a json containing information regarding this transaction
    """
    borrow = BorrowedBooks.query.get(borrow_id)
    if borrow is None:
        return jsonify({"message": "No such ID exists!"}), 400
    else:
        if borrow.return_status == "returned":
            return jsonify({"message": "Already returned"}), 400
        else:
            # switch return status to return
            borrow.return_status = "returned"
            # switch return date to current time
            borrow.return_date = datetime.now()
            borrowed_book = book_routes.Book.query.get(borrow.book_id)
            borrowed_book.quantity += 1
            db.session.commit()

            return borrowed_book_schema.jsonify(borrow)


@app.route('/borrow/<borrow_id>')
@cross_origin()
def get_borrow_from_id(borrow_id):
    """
    Get borrow_a_book info
    :param borrow_id: borrow_a_book's id
    :return: json with borrow_a_book's information
    """
    borrow = BorrowedBooks.query.get(borrow_id)
    if borrow is None:
        return jsonify({"message": "ID does not exists!"})
    else:
        return borrowed_book_schema.jsonify(borrow)


@app.route('/borrow/user/<user_id>', methods=['GET'])
@cross_origin()
def get_all_undue_borrow_of_a_user(user_id):
    """
    use this route to get all undue book of a user
    :param user_id:  target user's id
    :return: A JSON containing all undue books of a user
    """
    borrow = BorrowedBooks.query.filter(BorrowedBooks.user_id == user_id, BorrowedBooks.return_status == None).all()
    print(borrow)
    if len(borrow) == 0:
        return jsonify([{"message": "No undue books!"}])
    else:
        result = borrowed_books_schema.dump(borrow)

        return jsonify(result)


@app.route('/borrow/user/<user_id>/all', methods=['GET'])
@cross_origin()
def get_borrow_history_of_a_user(user_id):
    """
    Get borrow_a_book & return history of a user
    :param user_id: target user's id
    :return: A JSON with the list of borrow_a_book & return of the target user
    """
    borrow = BorrowedBooks.query.filter(BorrowedBooks.user_id == user_id).all()
    if len(borrow) == 0:
        return jsonify([{"message": "Borrow history is empty!"}])
    else:
        result = borrowed_books_schema.dump(borrow)

        return jsonify(result)
