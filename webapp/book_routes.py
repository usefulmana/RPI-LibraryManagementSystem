from app import db, ma, app, cross_origin, request, jsonify


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    ISBN = db.Column(db.Text)
    published_date = db.Column(db.Date)
    borrowed_books = db.relationship('BorrowedBooks')

    def __init__(self, title, author, ISBN, published_date):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.published_date = published_date


class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "author", "ISBN", "published_date")


book_Schema = BookSchema()
books_Schema = BookSchema(many=True)


@app.route('/books', methods=['POST'])
@cross_origin()
def add_book():
    """
    Use this route to add a new book
    :return: a JSON with the book's information
    """
    title = request.json['title']
    author = request.json['author']
    ISBN = request.json['ISBN']
    published_date = request.json['published_date']
    new_book = Book(title, author, ISBN, published_date)
    db.session.add(new_book)
    db.session.commit()

    return book_Schema.jsonify(new_book)


@app.route('/books', methods=['GET'])
@cross_origin()
def get_all_books():
    """
    Get all books from the database
    :return: JSON with list of all books
    """
    all_books = Book.query.all()
    result = books_Schema.dump(all_books)
    return jsonify(result)


# @app.route('/books/byTitle/<title>', methods=['GET'])
# @cross_origin()
# def get_books_by_title(title):
#     books = Book.query.filter(Book.title.like("%{}%".format(title))).all()
#     result = books_Schema.dump(books)
#     return jsonify(result)
#
#
# @app.route('/books/byAuthor/<author>', methods=['GET'])
# @cross_origin()
# def get_books_by_author(author):
#     books = Book.query.filter(Book.author.like("%{}%".format(author))).all()
#     result = books_Schema.dump(books)
#     return jsonify(result)
#
#
# @app.route('/books/byISBN/<ISBN>', methods=['GET'])
# @cross_origin()
# def get_books_by_ISBN(ISBN):
#     books = Book.query.filter(Book.ISBN.like("%{}%".format(ISBN))).all()
#     result = books_Schema.dump(books)
#     return jsonify(result)


@app.route('/books/<id>', methods=['GET'])
@cross_origin()
def get_book_by_id(id):
    """
    Get a book based on its id
    :param id: id of the target book
    :return:
    """
    book = Book.query.get(id)
    return book_Schema.jsonify(book)


@app.route('/books/<id>', methods=['DELETE'])
@cross_origin()
def delete_book(id):
    """
    Delete a book based on its id
    :param id: id of target book
    :return:
    """
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return book_Schema.jsonify(book)


@app.route('/books/others/<query>', methods=['GET'])
@cross_origin()
def search_book_by_query(query):
    """
    Search books based on a query
    :param query: user entered query
    :return:
    """
    books = Book.query.filter(
        Book.author.like("%{}%".format(query)) | Book.ISBN.like("%{}%".format(query)) | Book.title.like(
            "%{}%".format(query))).all()
    result = books_Schema.dump(books)
    return jsonify(result)
