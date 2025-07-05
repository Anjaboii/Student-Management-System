import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from student_model import (
    get_all_students,
    get_student_by_id,
    add_student,
    update_student,
    delete_student
)
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'f40f9a50df41e080ee1cc6b08c9e9842c038ddd8f391281d86d762fff87c21a1')
CORS(app, resources={r"/api/*": {"origins": "https://studentmanagement-1.netlify.app"}})

@app.route('/')
def index():
    return "Welcome to the Student Management System API"

@app.route('/api/students', methods=['GET'])
def api_get_students():
    try:
        students = get_all_students()
        return jsonify(students)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['GET'])
def api_get_student(student_id):
    try:
        student = get_student_by_id(student_id)
        if student:
            return jsonify(student)
        return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students', methods=['POST'])
def api_add_student():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'age', 'grade')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        rowcount = add_student(data)
        if rowcount:
            return jsonify({'message': 'Student added successfully'}), 201
        else:
            return jsonify({'error': 'Failed to add student'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def api_update_student(student_id):
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'age', 'grade')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        rowcount = update_student(student_id, data['name'], data['age'], data['grade'])
        if rowcount:
            return jsonify({'message': 'Student updated successfully'})
        else:
            return jsonify({'error': 'Student not found or no change'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    try:
        rowcount = delete_student(student_id)
        if rowcount:
            return jsonify({'message': 'Student deleted successfully'})
        else:
            return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
