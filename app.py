from flask import Flask, request, jsonify
from flask_cors import CORS

from student_model import (
    get_all_students,
    add_student,
    get_student_by_id,
    update_student,
    delete_student
)

app = Flask(__name__)

# Allow CORS from your frontend domain (change URL accordingly)
CORS(app, origins=['https://studentmanagement-1.netlify.app'])

@app.route('/')
def home():
    return "🎓 Student Management API is running!"

@app.route('/api/students', methods=['GET'])
def fetch_students():
    return jsonify(get_all_students())

@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json()
    add_student(data)
    return jsonify({"message": "Student added successfully"}), 201

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = get_student_by_id(student_id)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update(student_id):
    data = request.json
    result = update_student(student_id, data['name'], data['age'], data['grade'])
    return jsonify(result)

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete(student_id):
    result = delete_student(student_id)
    return jsonify(result)

@app.route('/api/students/search', methods=['GET'])
def search_students():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    all_students = get_all_students()
    matching_students = [
        s for s in all_students if
        query.lower() in str(s.get('name', '')).lower() or
        query.lower() in str(s.get('age', '')).lower() or
        query.lower() in str(s.get('grade', '')).lower() or
        query in str(s.get('id', ''))
    ]
    return jsonify({
        'students': matching_students,
        'total': len(matching_students),
        'query': query
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
