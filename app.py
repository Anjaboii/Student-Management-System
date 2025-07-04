from flask import Flask, request, jsonify
from student_model import get_all_students, add_student
from flask_cors import CORS

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

if __name__ == '__main__':
    app.run(debug=True)
