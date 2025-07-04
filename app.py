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
CORS(app)

@app.route('/')
def home():
    return "🎓 Student Management API is running!"

@app.route('/students', methods=['GET'])
def fetch_students():
    return jsonify(get_all_students())

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    add_student(data)
    return jsonify({"message": "Student added successfully"}), 201

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    return jsonify(get_student_by_id(student_id))

@app.route('/students/<int:student_id>', methods=['PUT'])
def update(student_id):
    data = request.json
    return jsonify(update_student(student_id, data['name'], data['age'], data['grade']))

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete(student_id):
    return jsonify(delete_student(student_id))

# NEW: Search endpoint
@app.route('/students/search', methods=['GET'])
def search_students():
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    
    # Get all students
    all_students = get_all_students()
    matching_students = []
    
    # Search through students
    for student in all_students:
        # Search in name, age, and grade (convert to string for searching)
        if (query.lower() in str(student.get('name', '')).lower() or 
            query.lower() in str(student.get('age', '')).lower() or 
            query.lower() in str(student.get('grade', '')).lower() or
            query in str(student.get('id', ''))):
            matching_students.append(student)
    
    return jsonify({
        'students': matching_students,
        'total': len(matching_students),
        'query': query
    })

if __name__ == '__main__':
    app.run(debug=True)