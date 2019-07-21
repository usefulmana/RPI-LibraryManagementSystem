
def get_all_books():
    return "http://127.0.0.1:5000/books"


def get_books_by_search_query(query):
    return 'http://127.0.0.1:5000/books/others/{}'.format(query.strip())


def get_book_by_id(book_id):
    return 'http://127.0.0.1:5000/books/{}'.format(book_id)


def borrow_a_book_route(book_id, user_id):
    return 'http://127.0.0.1:5000/borrow/{}/user/{}'.format(book_id, user_id)


def return_a_book_route(borrow_id):
    return 'http://127.0.0.1:5000/return/{}'.format(borrow_id)


def add_a_user():
    return 'http://127.0.0.1:5000/users'


def get_a_user_from_email(user_email):
    return 'http://127.0.0.1:5000/users/byEmail/{}'.format(user_email)


def get_undue_books_list_of_a_user(user_id):
    return 'http://127.0.0.1:5000/borrow/user/{}'.format(user_id)


def add_event_id(borrow_id, event_id):
    return 'http://127.0.0.1:5000/borrow/{}/event/{}'.format(borrow_id, event_id)


