
import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# Connect to the database
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Get all students using /student
@app.route('/student')
def get_student():
    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# Get one student using student_id
@app.route('/student/<student_id>')
def get_student_by_id(student_id):
    conn = get_db_connection()

    student = conn.execute(
        'SELECT * FROM students WHERE student_id = ?',
        (student_id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({'error': 'Student not found'}), 404

    return jsonify(dict(student))


# Get all students using /students
@app.route('/students')
def get_students():
    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# Step 7: Get one student using database ID
@app.route('/students/<int:id>')
def get_student_by_database_id(id):
    conn = get_db_connection()

    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({'error': 'Student not found'}), 404

    return jsonify(dict(student))


# Greeting API
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student').strip()

    if not name:
        name = 'Student'

    return jsonify({
        'message': f'Hello, {name}!'
    })


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
