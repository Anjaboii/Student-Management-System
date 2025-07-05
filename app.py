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

# Comprehensive CORS configuration
CORS(app, 
     origins=[
         'https://studentmanagement-1.netlify.app',  # Your Netlify domain
         'http://localhost:3000',                     # Local development
         'http://127.0.0.1:5500',                    # Live Server
         'http://localhost:5500'                     # Alternative Live Server port
     ],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'],
     supports_credentials=True)

# Handle preflight requests
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "https://studentmanagement-1.netlify.app")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization")
        response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
        return response

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://studentmanagement-1.netlify.app')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

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
    import os
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'  # Railway needs this
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host=host, port=port)