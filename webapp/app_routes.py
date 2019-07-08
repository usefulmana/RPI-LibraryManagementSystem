from app import app, db, ma, request, jsonify, render_template, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
from flask import send_file

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

# This route should be disabled to prevent additional account creation
# @app.route('/admin', methods=['POST'])
# def create_admin():
#     data = request.get_json()
#     hashed_password = generate_password_hash(data['password'], method='sha256')
#     username = data['username']
#     new_admin = Admin(username, hashed_password)
#     db.session.add(new_admin)
#     db.session.commit()
#
#     return admin_Schema.jsonify(new_admin)


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


@app.route('/weekly')
def get_weekly_plot():
    filename = 'images/weekly.png'
    return send_file(filename, mimetype='image/png')


@app.route('/daily')
def get_daily_plot():
    filename = 'images/daily.png'
    return send_file(filename, mimetype='image/png')
# @app.route('/daily', methods=['GET'])
# def daily_plot():
#     # Do not delete 2 lines below
#     ana = Analytics.get_instance()
#     ana.get_statistics_for_a_day()
#
#     plot_barplot('daily.csv', 'daily.png')
#     return jsonify({"message": "Image generated"})
#
#
# @app.route('/weekly', methods=['GET'])
# def weekly_plot():
#     # Do not delete the 2 lines below. it generate the data
#     ana = Analytics.get_instance()
#     ana.get_statistics_for_a_week()
#
#     plot_barplot('weekly.csv', 'weekly.png')
#     return jsonify({"message": "Image generated"})
#
#
# def plot_barplot(file, output_file):
#     """
#         Generate bar plot, can be used for both daily and weekly
#         if the table has the same columns ['date', 'borrows', 'returns']
#     :param file: path to CSV file
#     :return: pop up figure
#     """
#     sns.set()
#     daily_df = pd.read_csv(file)
#     daily_df = pd.melt(daily_df, id_vars='date', var_name='type', value_name='count')
#
#     with sns.color_palette('husl'):
#         fig, ax = plt.subplots(1)
#         sns.barplot(x='date', y='count', hue='type', data=daily_df, ax=ax)
#     plt.savefig('front-end/public/images/' + output_file)