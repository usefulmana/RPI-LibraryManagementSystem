from app import app, db, ma, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from analytics import Analytics
import pandas as pd
from matplotlib import pyplot as plt

jwt = JWTManager(app)


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def serialize(self):
        return {
            'username': self.username,
            'password': self.password
        }


class AdminSchema(ma.Schema):
    class Meta:
        fields = ('username',)


admin_Schema = AdminSchema()


@app.route('/admin', methods=['POST'])
def create_admin():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    username = data['username']
    new_admin = Admin(username, hashed_password)
    db.session.add(new_admin)
    db.session.commit()

    return admin_Schema.jsonify(new_admin)


@app.route('/admin', methods=['PUT'])
def update_admin_info():
    username = request.json['username']
    password = request.json['password']
    new_password = request.json['new_password']
    user = Admin.query.filter(Admin.username == username).first()
    if not user:
        return jsonify({"error": "No such username exists"})
    else:
        if check_password_hash(user.serialize['password'], password):
            user.password = generate_password_hash(new_password, method='sha256')
            db.session.commit()
        else:
            return jsonify({"error": "Invalid password!"})
    return admin_Schema.jsonify(user)


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = Admin.query.filter(Admin.username == username).first()
    if not user:
        return jsonify({"error": "No such username exists"})
    else:
        if check_password_hash(user.serialize['password'], password):
            access_token = create_access_token(identity={"username": user.serialize["username"]})
            result = access_token
        else:
            result = jsonify({"error": "Invalid password!"})
        return result


@app.route('/daily_plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    Analytics.get_instance().get_statistics_for_a_day()
    data = pd.read_csv('daily.csv')
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.bar(xs, ys)
    return fig


@app.route('/weekly_plot')
def weekly_plot():
    pass