from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from student_model import (
    get_all_students, add_student, get_student_by_id,
    update_student, delete_student
)
import os

app = Flask(__name__, static_folder='')  # Serve static files from project root
app.secret_key = 'your-secret-key'

# Enable CORS for API routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Serve frontend files from root folder

@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')

@app.route('/script.js')
def serve_script():
    return send_from_directory('', 'script.js')

@app.route('/style.css')
def serve_style():
    return send_from_directory('', 'style.css')

# --- API routes ---

@app.route('/api/students', methods=['GET'])
def api_get_students():
    try:
        students = get_all_students()
        return jsonify(students)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students', methods=['POST'])
def api_add_student():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'age', 'grade')):
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        student_id = add_student(data)
        return jsonify({'message': 'Student added', 'student_id': student_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['GET'])
def api_get_student(student_id):
    student = get_student_by_id(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student)

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def api_update_student(student_id):
    student = get_student_by_id(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'age', 'grade')):
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        update_student(student_id, data['name'], data['age'], data['grade'])
        return jsonify({'message': 'Student updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    student = get_student_by_id(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    try:
        delete_student(student_id)
        return jsonify({'message': 'Student deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
