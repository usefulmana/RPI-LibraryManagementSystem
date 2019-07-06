from app import app, render_template, request, make_response, jsonify, redirect, url_for, g
import jwt
from config_parser import Parser
import datetime
from functools import wraps
from admin_routes import Admin
from werkzeug.security import check_password_hash


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, Parser.get_instance().secret)
            current_user = Admin.query.filter_by(Admin.username == data['username']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        user = Admin.query.filter_by(username=auth.username).first()
        if auth and auth.username == user.username and check_password_hash(user.password, auth.password):
            token = jwt.encode(
                {'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10)},
                Parser.get_instance().secret)
            return f(*args, **kwargs)
        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated


@app.route('/')
@auth_required
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = Admin.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            Parser.get_instance().secret)
        print(user.username)
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@app.route('/view/daily_plot.png')
@auth_required
def generate_daily_report():
    pass


@app.route('/view/weekly_plot.png')
@auth_required
def generate_weekly_report():
    pass


@app.route('/search')
@auth_required
def search():
    pass
