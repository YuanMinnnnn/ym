from flask import Flask, request, jsonify, Blueprint
from wx_models import User, Health_Record
from applications.extensions import db
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('/home/li/桌面/pear-admin-flask/pear.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
                password TEXT,
                    realname TEXT,
                        age INTEGER,
                            mail TEXT
            )''')
conn.commit()

cur.execute('''CREATE TABLE IF NOT EXISTS health_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
                bp REAL,
                    bg REAL,
                        bf REAL,
                            height REAL,
                                weight REAL,
                                    bmi REAL,
                                        FOREIGN KEY(user_id) REFERENCES users(id)
            )''')
conn.commit()

# 创建一个蓝图对象
wx_blueprint = Blueprint('wx', __name__)
@wx_blueprint.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '')
    realname = data.get('realname', '')
    password = data.get('password', '')
    age = data.get('age', None)
    mail = data.get('mail', None)

    if username and password and realname and age and mail:
        if User.query.filter_by(username=username).first():
            return jsonify({'status': 'error', 'message': 'Username already exists.'}), 400
        user = User(username=username, realname=realname, password=password, age=age, mail=mail)
        db.session.add(user)
        try:
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Register successfully.'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 500

@wx_blueprint.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return jsonify({'status': 'success', 'message': 'Login successfully.'})
    else:
	    return jsonify({'status': 'error', 'message': 'Incorrect username or password.'}), 401

@wx_blueprint.route('/api/healthRecord', methods=['POST'])
def add_health_record():
    data = request.get_json()
    user_id = data.get('user_id', None)
    bp = data.get('bp', None)
    bg = data.get('bg', None)
    bf = data.get('bf', None)
    height = data.get('height', None)
    weight = data.get('weight', None)
    bmi = data.get('bmi', None)
    if user_id and bp and bg and bf and height and weight and bmi:
        record = HealthRecord(user_id=user_id, bp=bp, bg=bg, bf=bf, height=height, weight=weight, bmi=bmi)
        db.session.add(record)
        try:
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Add health record successfully.'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 500
                                            
@app.route('/api/userDataList', methods=['GET'])
def get_user_data_list():
    try:
        cur.execute('''SELECT * FROM users''')
        rows = cur.fetchall()
        user_data_list = [{'username': row[1], 'realname': row[3], 'age': row[4], 'mail': row[5]} for row in rows]
        return jsonify({'status': 'success', 'userDataList': user_data_list})
    except Ellipsis as e:     
        return jsonify({'status': 'error', 'message': str(e)}), 500
                                                                                            
if __name__ == '__main__':
    app.run(debug=True)