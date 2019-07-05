from app import app, render_template, request, make_response, jsonify
import jwt
from config_parser import Parser
import datetime
from functools import wraps


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'rmit3' and auth.password == '123456':
            token = jwt.encode(
                {'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                Parser.get_instance().secret)
            return f(*args, **kwargs)
        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return '<h1>403, Token is missing!</h1>'

        try:
            data = jwt.decode(token, Parser.get_instance().secret)
        except:
            return '<h1>403, Token is invalid!</h1>'
        return f(*args, **kwargs)
    return decorated


@app.route('/')
# @basic_auth.
@auth_required
def index():
    return render_template('home.html')


@app.route('/logout')
def logout():
    pass


@app.route('/view/daily_plot.png')
def generate_daily_report():
    pass


@app.route('/view/weekly_plot.png')
def generate_weekly_report():
    pass


@app.route('/search')
@token_required
def search():
    pass
