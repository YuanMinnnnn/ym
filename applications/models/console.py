# from flask import Flask, jsonify
# import sqlite3
# # from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# DATABASE = '/home/li/桌面/pear-admin-flask/pear.db'


# @app.route('/console/polling/')
# def polling():
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#     cursor.execute('SELECT username, bp, bg, bf, bmi FROM admin_record')
#     data = cursor.fetchall()
#     result = []
#     # for row in data:
#     #     result.append({
#     #         'username': row[0],
#     #         'bp': row[1],
#     #         'bg': row[2],
#     #         'bf': row[3],
#     #         'bmi': row[4]
#     #     })
#     conn.close()
#     return jsonify(result)

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, jsonify, request,Blueprint
# import sqlite3

# app = Flask(__name__)
# DATABASE = '/home/li/桌面/pear-admin-flask/pear.db'

# # 创建一个蓝图对象
# data_blueprint = Blueprint('data', __name__)

# # 在蓝图对象上注册路由
# @data_blueprint.route('/data')
# def get_data():
#     # 获取请求参数
#     username = request.args.get('username')
#     # 连接到 SQLite 数据库
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#     # if username:
#     #     # 如果提供了用户名，构建带有参数的查询语句
#     #     cursor.execute('SELECT username, bp, bg, bf, bmi FROM admin_record WHERE username = ?', (username,))
#     # else:
#         # 否则，执行无参数的查询语句
#     cursor.execute('SELECT username, bp, bg, bf, bmi FROM admin_record')
#     # 从数据库获取数据
#     data = cursor.fetchall()
#     conn.close()
    
#     # 返回具体的数值
#     return jsonify(data)  

# # 在应用中注册蓝图
# app.register_blueprint(data_blueprint)

# if __name__ == '__main__':
#     app.run(debug=True,port=8000)
# from flask import Flask, jsonify, request, Blueprint
# import sqlite3

# app = Flask(__name__)
# DATABASE = '/home/li/桌面/pear-admin-flask/pear.db'

# # 创建一个蓝图对象
# data_blueprint = Blueprint('data', __name__)

# # 在蓝图对象上注册路由
# @data_blueprint.route('/data')
# def get_data():
#     print("GET request received at /data")
#     # 获取请求参数
#     username = request.args.get('username')
#     # 连接到 SQLite 数据库
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#     # 构建带有参数的查询语句
#     query = 'SELECT username, bp, bg, bf, bmi FROM admin_record'
#     if username:
#         query += ' WHERE username = ?'
#         cursor.execute(query, (username,))
#     else:
#         cursor.execute(query)
#     # 从数据库获取数据
#     data = cursor.fetchall()
#     conn.close()

#     # 返回具体的数值
#     return jsonify(data)

# # 在应用中注册蓝图
# app.register_blueprint(data_blueprint)

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, jsonify, request, Blueprint
import sqlite3

app = Flask(__name__)
DATABASE = '/home/li/桌面/pear-admin-flask/pear.db'

# 创建一个蓝图对象
data_blueprint = Blueprint('data', __name__)

# 在蓝图对象上注册路由
@data_blueprint.route('/data', methods=['GET'])
def post_data():
    username = request.args.get('username')
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # 构建带有参数的查询语句
    query = 'SELECT username, bp, bg, bf, bmi FROM admin_record'
    if username:
        query += ' WHERE username = ?'
        cursor.execute(query, (username,))
    else:
        cursor.execute(query)
    # 从数据库获取数据
    data = cursor.fetchall()
    conn.close()

    # 将数据转换为 JSON 格式并返回
    response = []
    for row in data:
        response.append({
            'username': row[0],
            'bp': row[1],
            'bg': row[2],
            'bf': row[3],
            'bmi': row[4]
        })
    return jsonify(response)

# 在应用中注册蓝图
app.register_blueprint(data_blueprint)

if __name__ == '__main__':
    app.run(debug=True)