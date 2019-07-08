import requests

req = requests.post('http://127.0.0.1:5000/borrow/{}/user/{}'.format(book_id, user_id))