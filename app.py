from flask import Flask
import sqlite3
from flask import request, jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/test')
def test():
    return 'Test!'


def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create


@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO students (first_name, last_name, dob, amount_due)
        VALUES (?, ?, ?, ?)
    ''', (data['first_name'], data['last_name'], data['dob'], data['amount_due']))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 201

# For Read


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    student = conn.execute(
        'SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
    conn.close()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(dict(student)), 200

# For Update


@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''
        UPDATE students SET first_name = ?, last_name = ?, dob = ?, amount_due = ?
        WHERE student_id = ?
    ''', (data['first_name'], data['last_name'], data['dob'], data['amount_due'], student_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 200

# For Delete


@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 200

# For Show all records


@app.route('/students', methods=['GET'])
def get_all_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    student_list = []
    for student in students:
        student_list.append(dict(student))
    return jsonify(student_list), 200


if __name__ == '__main__':
    app.run(debug=True)
