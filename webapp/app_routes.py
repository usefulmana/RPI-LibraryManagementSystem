from app import app, db, ma, render_template, request, make_response, jsonify, redirect, url_for, g
import jwt
from config_parser import Parser
import datetime
from functools import wraps
# from admin_routes import Admin
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#
#         if not token:
#             return jsonify({'message': 'Token is missing!'}), 401
#
#         try:
#             data = jwt.decode(token, Parser.get_instance().secret)
#             current_user = Admin.query.filter_by(Admin.username == data['username']).first()
#         except:
#             return jsonify({'message': 'Token is invalid!'}), 401
#
#         return f(current_user, *args, **kwargs)
#
#     return decorated
#
#
# def auth_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         user = Admin.query.filter_by(username=auth.username).first()
#         if auth and auth.username == user.username and check_password_hash(user.password, auth.password):
#             token = jwt.encode(
#                 {'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10)},
#                 Parser.get_instance().secret)
#             return f(*args, **kwargs)
#         return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
#     return decorated


# @app.route('/login')
# def login():
#     auth = request.authorization
#
#     if not auth or not auth.username or not auth.password:
#         return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
#
#     user = Admin.query.filter_by(username=auth.username).first()
#
#     if not user:
#         return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
#
#     if check_password_hash(user.password, auth.password):
#         token = jwt.encode(
#             {'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
#             Parser.get_instance().secret)
#         print(user.username)
#         return jsonify({'token': token.decode('UTF-8')})
#
#     return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
class Admin(UserMixin, db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    admin = db.Column(db.Boolean)

    def __init__(self, username, password, admin):
        self.username = username
        self.password = password
        self.admin = admin


class AdminSchema(ma.Schema):
    class Meta:
        fields = ('username',)


admin_Schema = AdminSchema()


@app.route('/admin', methods=['POST'])
def create_admin():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    username = data['username']
    new_admin = Admin(username, hashed_password, True)
    db.session.add(new_admin)
    db.session.commit()

    return admin_Schema.jsonify(new_admin)


@login_manager.user_loader
def load_user(username):
    return Admin.query.filter(Admin.username == username).first()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField('Remember me')


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))

        return '<h1>Invalid username or password</h1>'
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')


@app.route('/view/daily_plot.png')
def generate_daily_report():
    pass


@app.route('/view/weekly_plot.png')
def generate_weekly_report():
    pass


@app.route('/search')
def search():
    pass
