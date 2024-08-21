import os
from flask import Flask, jsonify, request, make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'password')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE', 'your_database')

mysql = MySQL(app)

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/users', methods=['GET'])
def get_users():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Users")
        users = cur.fetchall()
        cur.close()
        return jsonify(users), 200
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/users', methods=['POST'])
def add_user():
    try:
        name = request.json['name']
        age = request.json['age']
        
        if not name or not age:
            return make_response(jsonify({'error': 'Name and age are required'}), 400)
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Users (Fname, Age) VALUES (%s, %s)", (name, age))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'User added successfully'}), 201
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        name = request.json.get('name')
        age = request.json.get('age')

        if not name or not age:
            return make_response(jsonify({'error': 'Name and age are required'}), 400)

        cur = mysql.connection.cursor()
        cur.execute("UPDATE Users SET Fname = %s, Age = %s WHERE Uid = %s", (name, age, id))
        mysql.connection.commit()
        cur.close()
        if cur.rowcount == 0:
            return make_response(jsonify({'error': 'User not found'}), 404)
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Users WHERE Uid = %s", (id,))
        mysql.connection.commit()
        cur.close()
        if cur.rowcount == 0:
            return make_response(jsonify({'error': 'User not found'}), 404)
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)), debug=True)
