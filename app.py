from flask import Flask, jsonify, flash
from flask_cors import CORS
from student_model import get_all_students

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Enable CORS for API routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def index():
    return "Welcome to Student Management System API"

@app.route('/api/students', methods=['GET'])
def api_get_students():
    try:
        students = get_all_students()
        return jsonify(students)
    except Exception as e:
        # Log or flash error if needed
        flash(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
