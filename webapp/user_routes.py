from app import db, ma,app, cross_origin, request


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(255), unique=True)
    name = db.Column(db.Text)
    borrowed_books = db.relationship('BorrowedBooks', lazy='dynamic', load_on_pending=True)

    def __init__(self, email, name):
        self.user_email = email
        self.name = name


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', "user_email", "name")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/users', methods=['POST'])
@cross_origin()
def add_user():
    """
    Add new user to the database
    :return: A JSON with new user's information
    """
    user_email = request.json['user_email']
    name = request.json['name']
    new_user = Users(user_email, name)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


@app.route('/users/byEmail/<email>', methods=['GET'])
@cross_origin()
def get_user_by_email(email):
    """
    Get information of a user based on his/her email
    :param email: target user's email
    :return: a JSON containing the target's user information
    """
    user = Users.query.filter(Users.user_email == email).first()
    return user_schema.jsonify(user)