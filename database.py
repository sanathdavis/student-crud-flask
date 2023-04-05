from flask import Flask
import sqlite3
from flask import request, jsonify

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

# create a new database file or connect to an existing one
conn = sqlite3.connect('students.db')

# create a new table named 'students' with the required fields
conn.execute('''
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    dob DATE,
    amount_due REAL
)
''')

# commit the changes to the database
conn.commit()

# close the connection to the database
conn.close()
