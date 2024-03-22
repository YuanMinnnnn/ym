from flask import Flask, request, jsonify, Blueprint
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
    username = data.get('username')
    password = data.get('password')
    realname = data.get('realname')
    age = data.get('age')
    mail = data.get('mail')

    try:
        cur.execute('''INSERT INTO users (username, password, realname, age, mail) 
                        VALUES (?, ?, ?, ?, ?)''', (username, password, realname, age, mail))
        conn.commit()
        return jsonify({'status': 'success', 'message': 'User registered successfully'})
    except Exception as e:
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