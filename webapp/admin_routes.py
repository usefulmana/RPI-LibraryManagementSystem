from app import db, ma, app, cross_origin, request, jsonify
from datetime import datetime, timedelta
from config_parser import Parser
import json
from werkzeug.security import generate_password_hash


class Admin(db.Model):
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