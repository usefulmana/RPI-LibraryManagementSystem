# from app import db, ma, app, cross_origin, request, jsonify
# from datetime import datetime, timedelta
# from config_parser import Parser
# import json
#
#
# class ReturnedBooks(db.Model):
#     __tablename__ = "returned_books"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     return_date = db.Column(db.Date)
#     borrow_id = db.Column(db.Integer, db.ForeignKey('borrowed_books.id'))
#
#     def __init__(self, borrow_id, return_date):
#         self.return_date = return_date
#         self.borrow_id = borrow_id
#
#
# class ReturnedBooksSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'return_date', 'borrowed_id')
#
#
# returned_book_schema = ReturnedBooksSchema()
# returned_books_schema = ReturnedBooksSchema(many=True)
#
#
# @app.route('/return/<borrow_id>', methods=['POST'])
# @cross_origin()
# def return_book(borrow_id):
#     return_date = datetime.now()
#     new_returned_book = ReturnedBooks(borrow_id, return_date)
#     db.session.add(new_returned_book)
#     db.session.commit()
#
#     return returned_book_schema.jsonify(new_returned_book)